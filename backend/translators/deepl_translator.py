"""DeepL API wrapper"""

import os
from typing import List, Optional
from .base_translator import BaseTranslator

try:
    import deepl
    DEEPL_AVAILABLE = True
except ImportError:
    DEEPL_AVAILABLE = False
    print("[!] deepl kurulu degil")

def _deepl_lang_codes(source_lang: str, target_lang: str) -> tuple:
    """
    DeepL dil kodları (büyük harf). İngilizce hedef için EN-US kullan;
    düz 'EN' hedefi bazı API yanıtlarında hata üretebiliyor (özellikle geri çeviri TR→EN).
    Kaynakta EN genelde kabul edilir.
    """
    src = (source_lang or "en").upper()
    tgt = (target_lang or "en").upper()
    if tgt == "EN":
        tgt = "EN-US"
    return src, tgt


class DeepLTranslator(BaseTranslator):
    """DeepL API wrapper sınıfı"""
    
    def __init__(self):
        super().__init__("DeepL")
        
        if not DEEPL_AVAILABLE:
            print(f"[X] {self.name} kullanilamiyor: Kutuphane kurulu degil")
            return
        
        try:
            api_key = os.getenv('DEEPL_API_KEY')
            
            if not api_key:
                print(f"[!] {self.name}: DEEPL_API_KEY ayarlanmamis")
                return
            
            # Translator oluştur
            self.translator = deepl.Translator(api_key)
            self._is_available = True
            print(f"[OK] {self.name} hazir")
            
            # Kullanım bilgisi
            try:
                usage = self.translator.get_usage()
                if usage.character.limit:
                    remaining = usage.character.limit - usage.character.count
                    print(f"  Kalan karakter: {remaining:,} / {usage.character.limit:,}")
            except:
                pass
            
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
            source, target = _deepl_lang_codes(source_lang, target_lang)

            result = self.translator.translate_text(
                text,
                source_lang=source,
                target_lang=target
            )
            
            return result.text
            
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
            source, target = _deepl_lang_codes(source_lang, target_lang)

            # DeepL batch çeviri desteği
            results = self.translator.translate_text(
                texts,
                source_lang=source,
                target_lang=target
            )
            
            if isinstance(results, list):
                return [r.text for r in results]
            else:
                return [results.text]
            
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
        # DeepL: ~$25 per 1M characters (Pro)
        # Free tier: 500,000 characters/month
        cost_per_million = 25.0
        return (char_count / 1_000_000) * cost_per_million
    
    def check_usage(self):
        """
        Kullanım bilgilerini kontrol et
        
        Returns:
            Kullanım istatistikleri
        """
        if not self._is_available:
            return {}
        
        try:
            usage = self.translator.get_usage()
            
            return {
                'character_count': usage.character.count,
                'character_limit': usage.character.limit,
                'remaining': usage.character.limit - usage.character.count if usage.character.limit else None
            }
        except Exception as e:
            print(f"[X] {self.name} kullanim kontrolu hatasi: {e}")
            return {}
    
    def get_supported_languages(self) -> List[str]:
        """
        Desteklenen dilleri döndür
        
        Returns:
            Dil kodları listesi
        """
        if not self._is_available:
            return []
        
        try:
            # Hedef diller
            target_langs = self.translator.get_target_languages()
            return [lang.code.lower() for lang in target_langs]
        except Exception as e:
            print(f"[X] {self.name} dil listesi hatasi: {e}")
            return []
