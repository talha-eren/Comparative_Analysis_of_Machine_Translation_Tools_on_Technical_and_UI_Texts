"""
Mock Translator - Test amaçlı basit çevirici

API anahtarı olmadan test için kullanılır.
"""

from typing import List, Optional
from .base_translator import BaseTranslator
import time

class MockTranslator(BaseTranslator):
    """
    Test amaçlı mock translator
    Basit kelime-kelime çeviri simülasyonu yapar
    """
    
    # Basit sözlük
    DICTIONARY = {
        'file': 'dosya',
        'edit': 'düzenle',
        'view': 'görünüm',
        'help': 'yardım',
        'open': 'aç',
        'save': 'kaydet',
        'close': 'kapat',
        'settings': 'ayarlar',
        'error': 'hata',
        'warning': 'uyarı',
        'success': 'başarılı',
        'failed': 'başarısız',
        'loading': 'yükleniyor',
        'please': 'lütfen',
        'wait': 'bekleyin',
        'click': 'tıklayın',
        'button': 'düğme',
        'menu': 'menü',
        'window': 'pencere',
        'dialog': 'iletişim kutusu',
        'the': '',
        'a': '',
        'an': '',
        'to': '',
        'for': '',
        'and': 've',
        'or': 'veya',
        'not': 'değil',
        'is': '',
        'are': '',
        'was': '',
        'were': '',
    }
    
    def __init__(self):
        super().__init__("Mock Translator")
        self._is_available = True
    
    def translate(self, text: str, source_lang: str = 'en', target_lang: str = 'tr') -> Optional[str]:
        """
        Basit mock çeviri
        """
        if not text:
            return None
        
        # Simüle edilmiş gecikme
        time.sleep(0.1)
        
        # Kelime-kelime çeviri
        words = text.lower().split()
        translated_words = []
        
        for word in words:
            # Noktalama işaretlerini temizle
            clean_word = word.strip('.,!?;:')
            punct = word[len(clean_word):] if len(word) > len(clean_word) else ''
            
            # Sözlükten çevir
            translated = self.DICTIONARY.get(clean_word, clean_word)
            if translated:
                translated_words.append(translated + punct)
        
        result = ' '.join(translated_words)
        
        # Boş sonuç dönmesin
        if not result.strip():
            return f"[Mock çeviri: {text}]"
        
        return result
    
    def batch_translate(self, texts: List[str], source_lang: str = 'en', 
                       target_lang: str = 'tr') -> List[Optional[str]]:
        """
        Toplu çeviri
        """
        return [self.translate(text, source_lang, target_lang) for text in texts]
    
    def is_available(self) -> bool:
        """
        Her zaman kullanılabilir
        """
        return True
    
    def estimate_cost(self, char_count: int) -> float:
        """
        Mock translator ücretsiz
        """
        return 0.0
    
    def get_supported_languages(self) -> List[str]:
        """
        Desteklenen diller
        """
        return ['en', 'tr']
