#!/usr/bin/env python3
"""
Auto-compare translations for the technical dataset and save scores to SQLite.

Defaults:
- Source -> target: en -> tr
- Dataset: data/processed/error_dWARN: unbabel-comet kurulu degilgory: technical
- Sample size: 500
"""

import argparse
import os
import random
import sys
import time
from pathlib import Path

# Project root
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from dotenv import load_dotenv

from compare_db import init_db, save_comparison
from evaluators import (
    calculate_bleu,
    calculate_chrf,
    calculate_ter,
    calculate_meteor,
    calculate_comet,
)
from translators import GoogleTranslator, DeepLTranslator, MicrosoftTranslator
from utils import load_dataset
from utils.rate_limiter import APIRateLimiter


def parse_args():
    parser = argparse.ArgumentParser(description="Auto-compare technical dataset")
    parser.add_argument("--sample-size", type=int, default=500, help="number of rows")
    parser.add_argument(
        "--dataset",
        type=str,
        default="data/processed/error_dataset.json",
        help="dataset path",
    )
    parser.add_argument(
        "--category",
        type=str,
        default="technical",
        help="category filter",
    )
    parser.add_argument(
        "--tools",
        nargs="+",
        default=["all"],
        help="google deepl microsoft all",
    )
    parser.add_argument("--seed", type=int, default=42, help="random seed")
    parser.add_argument("--sleep", type=float, default=0.1, help="sleep between calls")
    return parser.parse_args()


def initialize_translators(tool_names):
    all_translators = {
        "google": GoogleTranslator(),
        "deepl": DeepLTranslator(),
        "microsoft": MicrosoftTranslator(),
    }

    if "all" in tool_names:
        tool_names = list(all_translators.keys())

    translators = {
        name: translator
        for name, translator in all_translators.items()
        if name in tool_names and translator.is_available()
    }

    return translators


def main():
    args = parse_args()

    # Load environment
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        env_path = PROJECT_ROOT / "backend" / ".env"
    load_dotenv(env_path)

    # Init DB
    init_db()

    # Load dataset
    dataset_path = PROJECT_ROOT / args.dataset
    rows = load_dataset(str(dataset_path))

    if args.category:
        rows = [r for r in rows if r.get("category") == args.category]

    if not rows:
        print("[X] No rows found for given filters")
        sys.exit(1)

    random.seed(args.seed)
    sample = random.sample(rows, min(args.sample_size, len(rows)))

    translators = initialize_translators(args.tools)
    if not translators:
        print("[X] No translators available")
        sys.exit(1)

    limiter = APIRateLimiter()

    print("=" * 70)
    print("Auto Compare - Technical Dataset")
    print("=" * 70)
    print(f"Dataset: {dataset_path}")
    print(f"Category: {args.category}")
    print(f"Sample size: {len(sample)}")
    print(f"Tools: {', '.join(translators.keys())}")
    print("=" * 70)

    saved_count = 0

    for idx, segment in enumerate(sample, 1):
        source_text = (segment.get("source_text") or "").strip()
        reference = (segment.get("target_text") or "").strip()

        if not source_text:
            continue

        translations = {}
        metrics = {}

        for tool_name, translator in translators.items():
            limiter.get_limiter(tool_name, calls_per_second=5).wait()

            try:
                translation = translator.translate(source_text, "en", "tr")
            except Exception as exc:
                print(f"[!] {tool_name} error at {idx}: {exc}")
                translation = None

            if translation:
                translations[tool_name] = translation
                metrics[tool_name] = {
                    "bleu": calculate_bleu(translation, reference),
                    "meteor": calculate_meteor(translation, reference),
                    "ter": calculate_ter(translation, reference),
                    "chrf": calculate_chrf(translation, reference),
                    "comet": calculate_comet(source_text, translation, reference),
                }
            else:
                translations[tool_name] = None
                metrics[tool_name] = None

            time.sleep(args.sleep)

        if any(m for m in metrics.values() if isinstance(m, dict)):
            saved_id = save_comparison(
                source_text,
                "en",
                "tr",
                translations,
                metrics,
                reference=reference,
                category=args.category,
                metric_mode="reference",
                reference_source="dataset",
            )
            if saved_id is not None:
                saved_count += 1

        if idx % 25 == 0 or idx == len(sample):
            print(f"Progress: {idx}/{len(sample)} | saved: {saved_count}")

    print("=" * 70)
    print(f"Done. Saved rows: {saved_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()
