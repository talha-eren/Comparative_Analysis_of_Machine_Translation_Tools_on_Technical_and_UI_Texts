#!/usr/bin/env python3
"""
Flask Route Listesi

Tum kayitli endpoint'leri gosterir.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Proje kök dizinini bul
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / 'backend'))

# .env dosyasini yukle
env_path = PROJECT_ROOT / '.env'
load_dotenv(env_path)

# Flask app'i import et
from app import app

print("="*60)
print("Kayitli Flask Route'lar")
print("="*60)
print()

for rule in app.url_map.iter_rules():
    methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
    print(f"{methods:10s} {rule.rule}")

print()
print("="*60)
