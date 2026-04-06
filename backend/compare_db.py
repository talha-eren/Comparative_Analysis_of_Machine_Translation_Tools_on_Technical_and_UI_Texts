"""
SQLite: karsilastirma sonuclarini kalici olarak saklar.

Skor kolonlari BLEU ile doldurulur (ozet / en iyi arac mantigi ile uyumlu).
"""

from __future__ import annotations

import os
import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SCORE_METRIC = "bleu"


def _backend_dir() -> Path:
    return Path(__file__).resolve().parent


def get_db_path() -> Path:
    url = os.getenv("DATABASE_URL", "sqlite:///data/translations.db").strip()
    if url.startswith("sqlite:///"):
        raw = url.replace("sqlite:///", "", 1)
        p = Path(raw)
        if not p.is_absolute():
            p = _backend_dir() / p
        return p
    return _backend_dir() / "data" / "translations.db"


def connect() -> sqlite3.Connection:
    path = get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = connect()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS translation_comparisons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at REAL NOT NULL,
                text_en TEXT NOT NULL,
                text_tr TEXT,
                google_score REAL,
                deepl_score REAL,
                microsoft_score REAL,
                best_score REAL,
                best_translator TEXT,
                score_metric TEXT NOT NULL DEFAULT 'bleu',
                metrics_json TEXT,
                translations_json TEXT,
                reference_text TEXT,
                metric_mode TEXT,
                reference_source TEXT,
                category TEXT,
                source_lang TEXT,
                target_lang TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_translation_comparisons_created
                ON translation_comparisons(created_at DESC);
            """
        )
        # Eski veritabani surumleri icin kolon migration'lari
        existing = {row[1] for row in conn.execute("PRAGMA table_info(translation_comparisons)").fetchall()}
        required_columns = {
            "metrics_json": "TEXT",
            "translations_json": "TEXT",
            "reference_text": "TEXT",
            "metric_mode": "TEXT",
            "reference_source": "TEXT",
        }
        for col, col_type in required_columns.items():
            if col not in existing:
                conn.execute(f"ALTER TABLE translation_comparisons ADD COLUMN {col} {col_type}")
        conn.commit()
    finally:
        conn.close()


def _en_tr_pair(
    source_lang: str,
    target_lang: str,
    source_text: str,
    reference: Optional[str],
    translations: Dict[str, str],
    best_translator: Optional[str],
) -> Tuple[str, Optional[str]]:
    ref_or_best = reference
    if not ref_or_best and best_translator:
        ref_or_best = translations.get(best_translator)
    sl = (source_lang or "en").lower()
    tl = (target_lang or "tr").lower()
    if sl == "en" and tl == "tr":
        return source_text, ref_or_best
    if sl == "tr" and tl == "en":
        return ref_or_best or "", source_text
    return source_text, ref_or_best


def _best_from_metrics(metrics: Dict[str, Any]) -> Tuple[Optional[str], Optional[float]]:
    best_tool: Optional[str] = None
    best_val: Optional[float] = None
    for tool, m in metrics.items():
        if not isinstance(m, dict):
            continue
        v = m.get(SCORE_METRIC)
        if v is None:
            continue
        if best_val is None or v > best_val:
            best_val = v
            best_tool = tool
    return best_tool, best_val


def save_comparison(
    source_text: str,
    source_lang: str,
    target_lang: str,
    translations: Dict[str, str],
    metrics: Optional[Dict[str, Any]],
    reference: Optional[str] = None,
    category: Optional[str] = None,
    metric_mode: Optional[str] = None,
    reference_source: Optional[str] = None,
) -> Optional[int]:
    if not metrics:
        return None
    if category:
        category = category.strip().lower()
    best_tool, best_score = _best_from_metrics(metrics)
    text_en, text_tr = _en_tr_pair(
        source_lang, target_lang, source_text, reference, translations, best_tool
    )

    def _bleu(tool: str) -> Optional[float]:
        block = metrics.get(tool)
        if not isinstance(block, dict):
            return None
        v = block.get(SCORE_METRIC)
        return float(v) if v is not None else None

    conn = connect()
    try:
        cur = conn.execute(
            """
            INSERT INTO translation_comparisons (
                created_at, text_en, text_tr,
                google_score, deepl_score, microsoft_score,
                best_score, best_translator, score_metric,
                metrics_json, translations_json, reference_text, metric_mode, reference_source,
                category, source_lang, target_lang
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                time.time(),
                text_en or "",
                text_tr,
                _bleu("google"),
                _bleu("deepl"),
                _bleu("microsoft"),
                float(best_score) if best_score is not None else None,
                best_tool,
                SCORE_METRIC,
                json.dumps(metrics, ensure_ascii=False),
                json.dumps(translations, ensure_ascii=False),
                reference,
                metric_mode,
                reference_source,
                category,
                source_lang,
                target_lang,
            ),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def list_comparisons(limit: Optional[int] = 100, offset: int = 0) -> List[dict]:
    conn = connect()
    try:
        if limit is None:
            cur = conn.execute(
                """
                SELECT * FROM translation_comparisons
                ORDER BY id DESC
                """
            )
        else:
            cur = conn.execute(
                """
                SELECT * FROM translation_comparisons
                ORDER BY id DESC
                LIMIT ? OFFSET ?
                """,
                (limit, offset),
            )
        rows = []
        for row in cur.fetchall():
            item = dict(row)
            if item.get("metrics_json"):
                try:
                    item["metrics"] = json.loads(item["metrics_json"])
                except Exception:
                    item["metrics"] = None
            else:
                item["metrics"] = None
            if item.get("translations_json"):
                try:
                    item["translations"] = json.loads(item["translations_json"])
                except Exception:
                    item["translations"] = None
            else:
                item["translations"] = None
            rows.append(item)
        return rows
    finally:
        conn.close()


def count_comparisons() -> int:
    conn = connect()
    try:
        cur = conn.execute("SELECT COUNT(*) AS total FROM translation_comparisons")
        row = cur.fetchone()
        return int(row[0]) if row and row[0] is not None else 0
    finally:
        conn.close()
