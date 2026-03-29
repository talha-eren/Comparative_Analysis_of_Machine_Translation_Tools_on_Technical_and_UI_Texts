"""Google Cloud Translation API wrapper"""

import os
from typing import List, Optional
from .base_translator import BaseTranslator

try:
    from google.cloud import translate_v2 as translate
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    print("[!] google-cloud-translate kurulu degil")

class GoogleTranslator(BaseTranslator):
    """Google Cloud Translation API wrapper sınıfı"""
    
    def __init__(self):
        super().__init__("Google Translate")
        
        if not GOOGLE_AVAILABLE:
            print(f"[X] {self.name} kullanilamiyor: Kutuphane kurulu degil")
            return
        
        try:
            # Credentials kontrolü
            credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            if not credentials_path:
                print(f"[!] {self.name}: GOOGLE_APPLICATION_CREDENTIALS ayarlanmamis")
                return
            
            if not os.path.exists(credentials_path):
                print(f"[!] {self.name}: Credentials dosyasi bulunamadi: {credentials_path}")
                return
            
            # Client oluştur
            self.client = translate.Client()
            self._is_available = True
            print(f"[OK] {self.name} hazir")
            
        except Exception as e:
            print(f"[X] {self.name} baslatma hatasi: {e}")
            self._is_available = False
    
    def translate(self, text: str, source_lang: str = 'en', target_lang: str = 'tr') -> Optional[str]:
        """
        Tekil metin çevirisi
        
        Args:
            text: Çevrilecek metin
            source_lang: Kaynak dil kodu
            target_lang: Hedef dil kodu
        
        Returns:
            Çevrilmiş metin veya None
        """
        if not self._is_available:
            return None
        
        try:
            result = self.client.translate(
                text,
                source_language=source_lang,
                target_language=target_lang,
                format_='text'
            )
            
            return result['translatedText']
            
        except Exception as e:
            print(f"[X] {self.name} ceviri hatasi: {e}")
            return None
    
    def batch_translate(self, texts: List[str], source_lang: str = 'en', 
                       target_lang: str = 'tr') -> List[Optional[str]]:
        """
        Toplu metin çevirisi
        
        Args:
            texts: Çevrilecek metinler listesi
            source_lang: Kaynak dil kodu
            target_lang: Hedef dil kodu
        
        Returns:
            Çevrilmiş metinler listesi
        """
        if not self._is_available:
            return [None] * len(texts)
        
        try:
            # Google Translate API batch desteği (100 metin/istek)
            results = self.client.translate(
                texts,
                source_language=source_lang,
                target_language=target_lang,
                format_='text'
            )
            
            if isinstance(results, list):
                return [r['translatedText'] for r in results]
            else:
                return [results['translatedText']]
            
        except Exception as e:
            print(f"[X] {self.name} toplu ceviri hatasi: {e}")
            return [None] * len(texts)
    
    def estimate_cost(self, char_count: int) -> float:
        """
        Maliyet tahmini
        
        Args:
            char_count: Karakter sayısı
        
        Returns:
            Tahmini maliyet (USD)
        """
        # Google Translate: $20 per 1M characters
        # Free tier: 500,000 characters/month
        cost_per_million = 20.0
        return (char_count / 1_000_000) * cost_per_million
    
    def get_supported_languages(self) -> List[str]:
        """
        Desteklenen dilleri döndür
        
        Returns:
            Dil kodları listesi
        """
        if not self._is_available:
            return []
        
        try:
            results = self.client.get_languages()
            return [lang['language'] for lang in results]
        except Exception as e:
            print(f"[X] {self.name} dil listesi hatasi: {e}")
            return []
