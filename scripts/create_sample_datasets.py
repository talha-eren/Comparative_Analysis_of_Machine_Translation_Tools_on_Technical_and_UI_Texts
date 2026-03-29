#!/usr/bin/env python3
"""
Ornek Dataset Olusturma Scripti

Test icin kucuk ornek dataset'ler olusturur.
"""

import json
from pathlib import Path

# Proje kök dizinini bul
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"

# Ornek UI strings
UI_SAMPLES = [
    ("File", "Dosya"),
    ("Edit", "Duzenle"),
    ("View", "Gorunum"),
    ("Help", "Yardim"),
    ("Open File", "Dosya Ac"),
    ("Save As...", "Farkli Kaydet..."),
    ("Close", "Kapat"),
    ("Settings", "Ayarlar"),
    ("Preferences", "Tercihler"),
    ("About", "Hakkinda"),
    ("New Window", "Yeni Pencere"),
    ("Copy", "Kopyala"),
    ("Paste", "Yapistir"),
    ("Cut", "Kes"),
    ("Undo", "Geri Al"),
    ("Redo", "Yinele"),
    ("Select All", "Tumunu Sec"),
    ("Find", "Bul"),
    ("Replace", "Degistir"),
    ("Print", "Yazdir"),
]

# Ornek error messages
ERROR_SAMPLES = [
    ("File not found", "Dosya bulunamadi"),
    ("Access denied", "Erisim reddedildi"),
    ("Invalid input", "Gecersiz giris"),
    ("Connection timeout", "Baglanti zaman asimi"),
    ("Server error", "Sunucu hatasi"),
    ("Permission denied", "Izin reddedildi"),
    ("Out of memory", "Bellek yetersiz"),
    ("Network error", "Ag hatasi"),
    ("Invalid credentials", "Gecersiz kimlik bilgileri"),
    ("Database connection failed", "Veritabani baglantisi basarisiz"),
    ("Failed to load resource", "Kaynak yuklenemedi"),
    ("Syntax error in configuration", "Yapilandirmada sozdizimi hatasi"),
    ("Unable to connect to server", "Sunucuya baglanilemiyor"),
    ("Request timed out", "Istek zaman asimina ugradi"),
    ("Authentication failed", "Kimlik dogrulama basarisiz"),
]

# Ornek technical documentation
TECHNICAL_SAMPLES = [
    ("This function returns the current timestamp in milliseconds.", "Bu fonksiyon mevcut zaman damgasini milisaniye cinsinden dondurur."),
    ("Initialize the database connection pool with the specified parameters.", "Veritabani baglanti havuzunu belirtilen parametrelerle baslat."),
    ("The API endpoint accepts JSON payloads with authentication headers.", "API uç noktasi kimlik dogrulama basliklariyla JSON yuku kabul eder."),
    ("Configure the server to listen on port 8080 for incoming requests.", "Sunucuyu gelen istekler icin 8080 portunu dinleyecek sekilde yapilandir."),
    ("This method validates user input and sanitizes special characters.", "Bu yontem kullanici girisini dogrular ve ozel karakterleri temizler."),
    ("The cache expires after 3600 seconds of inactivity.", "Onbellek 3600 saniye etkinlik olmadiginda sona erer."),
    ("Enable SSL encryption for secure data transmission.", "Guvenli veri iletimi icin SSL sifrelemesini etkinlestir."),
    ("The system automatically creates backups every 24 hours.", "Sistem her 24 saatte bir otomatik yedekleme olusturur."),
    ("Use environment variables to configure application settings.", "Uygulama ayarlarini yapilandirmak icin ortam degiskenlerini kullanin."),
    ("This component renders a responsive navigation menu.", "Bu bilesen duyarli bir gezinme menusu olusturur."),
    ("The middleware intercepts requests before they reach the controller.", "Ara yazilim istekleri denetleyiciye ulasmadan once yakalar."),
    ("Deploy the application using Docker containers for consistency.", "Tutarlilik icin uygulamayi Docker konteynerlerini kullanarak dagit."),
    ("The algorithm has O(n log n) time complexity.", "Algoritmanin O(n log n) zaman karmasikligi vardir."),
    ("Implement rate limiting to prevent API abuse.", "API kotuve kullanimi onlemek icin hiz sinirlama uygula."),
    ("The service scales horizontally across multiple instances.", "Hizmet birden fazla ornek uzerinde yatay olarak olceklenir."),
]

def create_dataset(name, samples, category):
    """
    Dataset olustur ve kaydet
    """
    output_dir = DATA_RAW_DIR / name.lower()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"{name.lower()}_en_tr.json"
    
    segments = []
    for idx, (source, target) in enumerate(samples, 1):
        segment = {
            "id": f"{name.lower()}_{idx:06d}",
            "source_text": source,
            "target_text": target,
            "category": category,
            "subcategory": f"{category}_strings",
            "source_lang": "en",
            "target_lang": "tr",
            "source": name,
            "metadata": {
                "length": len(source),
                "has_placeholders": any(p in source for p in ['%s', '%d', '{', '}', '<', '>'])
            }
        }
        segments.append(segment)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] {name}: {len(segments)} segment olusturuldu")
    return output_file

def main():
    print("="*60)
    print("Ornek Dataset Olusturma")
    print("="*60)
    print()
    
    # UI dataset
    create_dataset("gnome", UI_SAMPLES, "ui")
    
    # Error dataset
    create_dataset("kde4", ERROR_SAMPLES, "error")
    
    # Technical dataset
    create_dataset("mozilla", TECHNICAL_SAMPLES, "technical")
    
    print("\n" + "="*60)
    print("Tum ornek dataset'ler olusturuldu!")
    print("="*60)
    print("\nNot: Bunlar test icin ornek dataset'lerdir.")
    print("Gercek OPUS dataset'leri icin manuel indirme gerekebilir.")

if __name__ == "__main__":
    main()
