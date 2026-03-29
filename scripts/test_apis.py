#!/usr/bin/env python3
"""
API Test Scripti

Tum ceviri API'lerini test eder ve durumlarini gosterir.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Proje kök dizinini bul
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

# .env dosyasini yukle
env_path = PROJECT_ROOT / '.env'
load_dotenv(env_path)

from backend.translators.google_translator import GoogleTranslator
from backend.translators.deepl_translator import DeepLTranslator
from backend.translators.microsoft_translator import MicrosoftTranslator
from backend.translators.amazon_translator import AmazonTranslator

# Test metni
TEST_TEXT = "Hello, this is a test."
TEST_SOURCE = "en"
TEST_TARGET = "tr"

def test_translator(translator, name):
    """
    Bir ceviriciyi test et
    """
    print(f"\n{'='*60}")
    print(f"Test: {name}")
    print(f"{'='*60}")
    
    # Kullanilabilirlik kontrolu
    if not translator.is_available():
        print(f"[X] {name} kullanilabilir degil")
        return False
    
    print(f"[OK] {name} kullanilabilir")
    
    # Ceviri testi
    try:
        result = translator.translate(TEST_TEXT, TEST_SOURCE, TEST_TARGET)
        
        if result:
            print(f"\nTest metni: {TEST_TEXT}")
            print(f"Ceviri: {result}")
            print(f"\n[OK] {name} basariyla calisıyor!")
            return True
        else:
            print(f"[X] {name} ceviri yapamadi")
            return False
            
    except Exception as e:
        print(f"[X] {name} hata: {e}")
        return False

def main():
    print("="*60)
    print("Ceviri API Test Scripti")
    print("="*60)
    print("\nTum API'ler test ediliyor...")
    
    results = {}
    
    # Google Translate
    google = GoogleTranslator()
    results['Google'] = test_translator(google, "Google Translate")
    
    # DeepL
    deepl = DeepLTranslator()
    results['DeepL'] = test_translator(deepl, "DeepL")
    
    # Microsoft
    microsoft = MicrosoftTranslator()
    results['Microsoft'] = test_translator(microsoft, "Microsoft Translator")
    
    # Amazon
    amazon = AmazonTranslator()
    results['Amazon'] = test_translator(amazon, "Amazon Translate")
    
    # Ozet
    print("\n" + "="*60)
    print("Test Ozeti")
    print("="*60)
    
    working_count = 0
    for name, status in results.items():
        status_text = "[OK] Calisıyor" if status else "[X] Calismiyor"
        print(f"{name:20s}: {status_text}")
        if status:
            working_count += 1
    
    print(f"\nToplam: {working_count}/{len(results)} API calisıyor")
    
    if working_count == 0:
        print("\n[!] Hicbir API calismiyor!")
        print("Lutfen API_SETUP_GUIDE.md dosyasina bakin.")
        sys.exit(1)
    elif working_count < len(results):
        print(f"\n[!] {len(results) - working_count} API yapilandirilmali")
        print("Detaylar icin API_SETUP_GUIDE.md dosyasina bakin.")
    else:
        print("\n[OK] Tum API'ler basariyla yapilandirildi!")

if __name__ == "__main__":
    main()
