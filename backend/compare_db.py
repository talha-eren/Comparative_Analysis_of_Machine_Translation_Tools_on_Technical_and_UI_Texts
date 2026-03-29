"""
SQLite: karsilastirma sonuclarini kalici olarak saklar.

Skor kolonlari BLEU ile doldurulur (ozet / en iyi arac mantigi ile uyumlu).
"""

from __future__ import annotations

import os
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
                amazon_score REAL,
                microsoft_score REAL,
                best_score REAL,
                best_translator TEXT,
                score_metric TEXT NOT NULL DEFAULT 'bleu',
                category TEXT,
                source_lang TEXT,
                target_lang TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_translation_comparisons_created
                ON translation_comparisons(created_at DESC);
            """
        )
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
) -> Optional[int]:
    if not metrics:
        return None
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
                google_score, deepl_score, amazon_score, microsoft_score,
                best_score, best_translator, score_metric, category, source_lang, target_lang
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                time.time(),
                text_en or "",
                text_tr,
                _bleu("google"),
                _bleu("deepl"),
                _bleu("amazon"),
                _bleu("microsoft"),
                float(best_score) if best_score is not None else None,
                best_tool,
                SCORE_METRIC,
                category,
                source_lang,
                target_lang,
            ),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def list_comparisons(limit: int = 100, offset: int = 0) -> List[dict]:
    conn = connect()
    try:
        cur = conn.execute(
            """
            SELECT * FROM translation_comparisons
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        )
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()
