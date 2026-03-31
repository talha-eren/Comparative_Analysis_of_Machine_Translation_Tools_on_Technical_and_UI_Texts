#!/usr/bin/env python3
"""
Hizli Test Scripti

DeepL ile birkaç örnek çeviri yapar ve sonuçları gösterir.
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

from backend.translators.deepl_translator import DeepLTranslator
from backend.evaluators.bleu_scorer import calculate_bleu, calculate_chrf, calculate_ter
from backend.evaluators.meteor_scorer import calculate_meteor
from backend.evaluators.comet_scorer import calculate_comet

# Test örnekleri
TEST_CASES = [
    {
        "source": "Click the button to save your changes.",
        "reference": "Değişikliklerinizi kaydetmek için düğmeye tıklayın.",
        "category": "UI"
    },
    {
        "source": "File not found. Please check the path.",
        "reference": "Dosya bulunamadı. Lütfen yolu kontrol edin.",
        "category": "Error"
    },
    {
        "source": "This function initializes the database connection.",
        "reference": "Bu fonksiyon veritabanı bağlantısını başlatır.",
        "category": "Technical"
    },
    {
        "source": "The API endpoint returns JSON data.",
        "reference": "API uç noktası JSON verisi döndürür.",
        "category": "Technical"
    },
    {
        "source": "Settings saved successfully.",
        "reference": "Ayarlar başarıyla kaydedildi.",
        "category": "UI"
    }
]

def main():
    print("="*70)
    print("DeepL Hızlı Test")
    print("="*70)
    print()
    
    # DeepL'i başlat
    deepl = DeepLTranslator()
    
    if not deepl.is_available():
        print("[X] DeepL kullanılabilir değil!")
        print("API key'inizi .env dosyasında kontrol edin.")
        sys.exit(1)
    
    print("[OK] DeepL hazır!")
    print()
    
    # Her test örneğini çevir
    for idx, test in enumerate(TEST_CASES, 1):
        print(f"\n{'='*70}")
        print(f"Test {idx}/{len(TEST_CASES)} - {test['category']}")
        print(f"{'='*70}")
        
        source = test['source']
        reference = test['reference']
        
        print(f"\nKaynak:    {source}")
        print(f"Referans:  {reference}")
        
        # Çevir
        try:
            translation = deepl.translate(source, 'en', 'tr')
            print(f"DeepL:     {translation}")
            
            # Metrikleri hesapla
            if translation:
                bleu = calculate_bleu(translation, reference)
                chrf = calculate_chrf(translation, reference)
                ter = calculate_ter(translation, reference)
                meteor = calculate_meteor(translation, reference)
                comet = calculate_comet(source, translation, reference)
                
                print(f"\nMetrikler:")
                print(f"  BLEU:   {bleu:.3f}" if bleu else "  BLEU:   N/A")
                print(f"  chrF++: {chrf:.3f}" if chrf else "  chrF++: N/A")
                print(f"  TER:    {ter:.3f}" if ter else "  TER:    N/A")
                print(f"  METEOR: {meteor:.3f}" if meteor else "  METEOR: N/A")
                print(f"  COMET:  {comet:.3f}" if comet is not None else "  COMET:  N/A")
                
                # Kalite değerlendirmesi
                if bleu and bleu > 0.5:
                    print(f"\n✓ Yüksek kalite çeviri!")
                elif bleu and bleu > 0.3:
                    print(f"\n~ Orta kalite çeviri")
                else:
                    print(f"\n! Düşük kalite çeviri")
            
        except Exception as e:
            print(f"[X] Çeviri hatası: {e}")
    
    print(f"\n{'='*70}")
    print("Test Tamamlandı!")
    print("="*70)
    print("\nSonraki adımlar:")
    print("1. Frontend'i açın: http://localhost:5173")
    print("2. 'Compare' sayfasına gidin")
    print("3. Kendi metinlerinizi test edin!")
    print("4. Diğer API'leri ekleyin (GET_FREE_API_KEYS.md)")

if __name__ == "__main__":
    main()
