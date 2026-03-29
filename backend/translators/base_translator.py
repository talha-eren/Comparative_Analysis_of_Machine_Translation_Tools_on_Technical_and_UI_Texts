"""Base translator sınıfı - tüm çeviri API'leri için ortak interface"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class BaseTranslator(ABC):
    """Tüm çeviri API'leri için temel sınıf"""
    
    def __init__(self, name: str):
        """
        Args:
            name: Çeviri aracının adı
        """
        self.name = name
        self._is_available = False
    
    @abstractmethod
    def translate(self, text: str, source_lang: str = 'en', target_lang: str = 'tr') -> Optional[str]:
        """
        Tekil metin çevirisi
        
        Args:
            text: Çevrilecek metin
            source_lang: Kaynak dil kodu
            target_lang: Hedef dil kodu
        
        Returns:
            Çevrilmiş metin veya None (hata durumunda)
        """
        pass
    
    @abstractmethod
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
        pass
    
    def is_available(self) -> bool:
        """
        API'nin kullanılabilir olup olmadığını kontrol et
        
        Returns:
            Boolean
        """
        return self._is_available
    
    def get_name(self) -> str:
        """
        Çeviri aracının adını döndür
        
        Returns:
            Araç adı
        """
        return self.name
    
    def estimate_cost(self, char_count: int) -> float:
        """
        Maliyet tahmini (USD)
        
        Args:
            char_count: Karakter sayısı
        
        Returns:
            Tahmini maliyet (USD)
        """
        return 0.0
    
    def get_supported_languages(self) -> List[str]:
        """
        Desteklenen dilleri döndür
        
        Returns:
            Dil kodları listesi
        """
        return []
