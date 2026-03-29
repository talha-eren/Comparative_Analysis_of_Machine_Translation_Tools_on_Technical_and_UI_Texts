"""Basit dosya tabanlı cache sistemi"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Any

class Cache:
    """Basit dosya tabanlı cache sistemi"""
    
    def __init__(self, cache_dir: str = "cache", ttl_seconds: int = 3600):
        """
        Args:
            cache_dir: Cache dizini
            ttl_seconds: Cache yaşam süresi (saniye)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(seconds=ttl_seconds)
    
    def _get_cache_key(self, text: str, translator: str, source_lang: str, target_lang: str) -> str:
        """
        Cache key oluştur
        
        Args:
            text: Metin
            translator: Çeviri aracı adı
            source_lang: Kaynak dil
            target_lang: Hedef dil
        
        Returns:
            Hash key
        """
        key_string = f"{translator}:{source_lang}:{target_lang}:{text}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, text: str, translator: str, source_lang: str = 'en', 
            target_lang: str = 'tr') -> Optional[str]:
        """
        Cache'den çeviri al
        
        Args:
            text: Kaynak metin
            translator: Çeviri aracı
            source_lang: Kaynak dil
            target_lang: Hedef dil
        
        Returns:
            Cached çeviri veya None
        """
        cache_key = self._get_cache_key(text, translator, source_lang, target_lang)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # TTL kontrolü
            cached_time = datetime.fromisoformat(data['timestamp'])
            if datetime.now() - cached_time > self.ttl:
                cache_file.unlink()
                return None
            
            return data['translation']
            
        except Exception as e:
            return None
    
    def set(self, text: str, translation: str, translator: str, 
            source_lang: str = 'en', target_lang: str = 'tr'):
        """
        Çeviriyi cache'e kaydet
        
        Args:
            text: Kaynak metin
            translation: Çeviri
            translator: Çeviri aracı
            source_lang: Kaynak dil
            target_lang: Hedef dil
        """
        cache_key = self._get_cache_key(text, translator, source_lang, target_lang)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            data = {
                'text': text,
                'translation': translation,
                'translator': translator,
                'source_lang': source_lang,
                'target_lang': target_lang,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"✗ Cache kaydetme hatası: {e}")
    
    def clear(self):
        """Tüm cache'i temizle"""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
    
    def get_stats(self) -> dict:
        """
        Cache istatistiklerini al
        
        Returns:
            İstatistikler dict
        """
        cache_files = list(self.cache_dir.glob("*.json"))
        
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            'total_entries': len(cache_files),
            'total_size_mb': total_size / 1024 / 1024,
            'cache_dir': str(self.cache_dir)
        }
