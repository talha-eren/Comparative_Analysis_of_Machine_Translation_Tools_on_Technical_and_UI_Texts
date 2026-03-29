#!/usr/bin/env python3
"""
GitHub Veri Toplama Scripti

Bu script GitHub'dan Türk projelerinin i18n dosyalarını ve README'lerini toplar.

Kullanım:
    python scripts/download_github.py
    
Gerekli:
    - GitHub Personal Access Token (opsiyonel, rate limit için)
    - PyGithub kütüphanesi
"""

import os
import sys
import json
import time
from pathlib import Path
from github import Github, GithubException
from tqdm import tqdm

# Proje kök dizini
PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw" / "github"

# GitHub token (opsiyonel - rate limit artırır)
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', None)

# Aranacak dosya tipleri
I18N_PATTERNS = [
    'i18n/en.json',
    'i18n/tr.json',
    'locales/en.json',
    'locales/tr.json',
    'lang/en.json',
    'lang/tr.json',
    'translations/en.json',
    'translations/tr.json'
]

def search_turkish_projects(g, max_repos=50):
    """
    Türk geliştiricilerin popüler projelerini ara
    
    Args:
        g: Github instance
        max_repos: Maksimum repo sayısı
    
    Returns:
        List of repositories
    """
    print("Türk projeleri aranıyor...")
    
    queries = [
        'language:JavaScript stars:>100 location:Turkey',
        'language:TypeScript stars:>50 location:Turkey',
        'language:Python stars:>50 location:Turkey',
        'topic:i18n language:JavaScript',
        'topic:localization language:TypeScript',
        'i18n in:readme language:JavaScript stars:>50'
    ]
    
    repos = set()
    
    for query in queries:
        try:
            print(f"\nArama: {query}")
            results = g.search_repositories(query=query, sort='stars')
            
            for repo in results[:max_repos // len(queries)]:
                repos.add(repo)
                print(f"  ✓ {repo.full_name} ({repo.stargazers_count} ⭐)")
                
                if len(repos) >= max_repos:
                    break
                    
        except GithubException as e:
            print(f"  ✗ Arama hatası: {e}")
            continue
    
    return list(repos)

def find_i18n_files(repo):
    """
    Repo'da i18n dosyalarını bul
    
    Args:
        repo: Github repository object
    
    Returns:
        Dict with 'en' and 'tr' file contents
    """
    i18n_files = {'en': None, 'tr': None}
    
    try:
        # Root'taki yaygın i18n klasörlerini kontrol et
        common_paths = [
            'i18n', 'locales', 'lang', 'translations', 
            'src/i18n', 'src/locales', 'public/locales'
        ]
        
        for path in common_paths:
            try:
                contents = repo.get_contents(path)
                
                if isinstance(contents, list):
                    for content in contents:
                        if content.name in ['en.json', 'en-US.json', 'en_US.json']:
                            i18n_files['en'] = content
                        elif content.name in ['tr.json', 'tr-TR.json', 'tr_TR.json']:
                            i18n_files['tr'] = content
                
                if i18n_files['en'] and i18n_files['tr']:
                    return i18n_files
                    
            except GithubException:
                continue
        
    except Exception as e:
        print(f"    ✗ Dosya arama hatası: {e}")
    
    return i18n_files

def extract_parallel_texts(en_content, tr_content):
    """
    İngilizce ve Türkçe i18n dosyalarından paralel metinler çıkar
    
    Args:
        en_content: İngilizce dosya içeriği
        tr_content: Türkçe dosya içeriği
    
    Returns:
        List of parallel text pairs
    """
    try:
        en_data = json.loads(en_content.decoded_content.decode('utf-8'))
        tr_data = json.loads(tr_content.decoded_content.decode('utf-8'))
        
        pairs = []
        
        def extract_nested(en_dict, tr_dict, prefix=''):
            """Nested JSON'dan key-value çiftlerini çıkar"""
            for key, en_value in en_dict.items():
                full_key = f"{prefix}.{key}" if prefix else key
                
                if key in tr_dict:
                    tr_value = tr_dict[key]
                    
                    if isinstance(en_value, str) and isinstance(tr_value, str):
                        if en_value.strip() and tr_value.strip():
                            pairs.append({
                                'key': full_key,
                                'en': en_value.strip(),
                                'tr': tr_value.strip()
                            })
                    elif isinstance(en_value, dict) and isinstance(tr_value, dict):
                        extract_nested(en_value, tr_value, full_key)
        
        extract_nested(en_data, tr_data)
        return pairs
        
    except Exception as e:
        print(f"    ✗ JSON parse hatası: {e}")
        return []

def collect_from_github(max_repos=50, max_segments=5000):
    """
    GitHub'dan i18n dosyalarını topla
    
    Args:
        max_repos: Maksimum repo sayısı
        max_segments: Maksimum segment sayısı
    """
    print("\n" + "="*60)
    print("GitHub'dan Veri Toplama")
    print("="*60)
    
    # GitHub client oluştur
    if GITHUB_TOKEN:
        g = Github(GITHUB_TOKEN)
        print("✓ GitHub token kullanılıyor (yüksek rate limit)")
    else:
        g = Github()
        print("⚠ GitHub token yok (düşük rate limit)")
        print("  Token için: https://github.com/settings/tokens")
    
    # Rate limit kontrolü
    rate_limit = g.get_rate_limit()
    print(f"Rate limit: {rate_limit.core.remaining}/{rate_limit.core.limit}")
    
    if rate_limit.core.remaining < 100:
        print("⚠ Rate limit düşük! Bekleniyor...")
        reset_time = rate_limit.core.reset
        wait_seconds = (reset_time - time.time())
        if wait_seconds > 0:
            print(f"  {wait_seconds/60:.1f} dakika bekleniyor...")
            time.sleep(wait_seconds + 10)
    
    # Projeleri ara
    repos = search_turkish_projects(g, max_repos)
    print(f"\n✓ {len(repos)} repo bulundu")
    
    # Veri toplama
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    all_segments = []
    
    print("\ni18n dosyaları toplanıyor...")
    
    for repo in tqdm(repos, desc="Repolar"):
        try:
            print(f"\n{repo.full_name}:")
            
            # i18n dosyalarını bul
            i18n_files = find_i18n_files(repo)
            
            if i18n_files['en'] and i18n_files['tr']:
                print(f"  ✓ i18n dosyaları bulundu")
                
                # Paralel metinleri çıkar
                pairs = extract_parallel_texts(i18n_files['en'], i18n_files['tr'])
                
                if pairs:
                    print(f"  ✓ {len(pairs)} çeviri çifti bulundu")
                    
                    # Segment formatına dönüştür
                    for idx, pair in enumerate(pairs):
                        segment = {
                            "id": f"github_{repo.name}_{idx:04d}",
                            "source_text": pair['en'],
                            "target_text": pair['tr'],
                            "category": "ui",
                            "subcategory": "ui_string",
                            "source_lang": "en",
                            "target_lang": "tr",
                            "length": len(pair['en']),
                            "source": f"github_{repo.name}",
                            "metadata": {
                                "repo": repo.full_name,
                                "stars": repo.stargazers_count,
                                "key": pair['key'],
                                "has_placeholder": any(c in pair['en'] for c in ['%', '{', '}', '<', '>']),
                                "word_count": len(pair['en'].split())
                            }
                        }
                        all_segments.append(segment)
                        
                        if len(all_segments) >= max_segments:
                            break
            else:
                print(f"  - i18n dosyaları bulunamadı")
            
            if len(all_segments) >= max_segments:
                print(f"\n✓ Hedef segment sayısına ulaşıldı ({max_segments})")
                break
                
        except Exception as e:
            print(f"  ✗ Hata: {e}")
            continue
    
    # Sonuçları kaydet
    if all_segments:
        output_file = DATA_RAW_DIR / "github_i18n.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_segments, f, ensure_ascii=False, indent=2)
        
        print(f"\n{'='*60}")
        print(f"✓ Toplam {len(all_segments)} segment toplandı")
        print(f"✓ Kaydedildi: {output_file}")
        print(f"{'='*60}")
        
        # İstatistikler
        print("\nİstatistikler:")
        print(f"  - Toplam segment: {len(all_segments)}")
        print(f"  - Ortalama uzunluk: {sum(s['length'] for s in all_segments) / len(all_segments):.1f} karakter")
        print(f"  - Placeholder içeren: {sum(1 for s in all_segments if s['metadata']['has_placeholder'])}")
        print(f"  - Benzersiz repo: {len(set(s['metadata']['repo'] for s in all_segments))}")
    else:
        print("\n✗ Hiç segment toplanamadı")

def main_alternative():
    """
    GitHub API kullanmadan alternatif yöntem
    Popüler Türk projelerinin linklerini manuel olarak kullan
    """
    print("\n" + "="*60)
    print("Alternatif: Manuel Repo Listesi")
    print("="*60)
    
    # Popüler Türk projeleri (örnekler)
    popular_repos = [
        "aykutkardas/regexlearn.com",
        "acikkaynak/acikkaynak-website",
        "Trendyol/android-ui-components",
        "getir/getir-ui-kit"
    ]
    
    print("\nÖnerilen repolar:")
    for repo in popular_repos:
        print(f"  - https://github.com/{repo}")
    
    print("\nBu repoları manuel olarak klonlayıp i18n dosyalarını çıkarabilirsiniz.")

if __name__ == "__main__":
    try:
        collect_from_github(max_repos=50, max_segments=5000)
    except KeyboardInterrupt:
        print("\n\n✗ İşlem kullanıcı tarafından iptal edildi")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Beklenmeyen hata: {e}")
        print("\nAlternatif yöntem için:")
        main_alternative()
        sys.exit(1)
