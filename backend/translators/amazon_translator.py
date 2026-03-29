"""Amazon Translate API wrapper"""

import os
from typing import List, Optional
from .base_translator import BaseTranslator

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
    print("⚠ boto3 kurulu değil")

class AmazonTranslator(BaseTranslator):
    """Amazon Translate API wrapper sınıfı"""
    
    def __init__(self):
        super().__init__("Amazon Translate")
        
        if not BOTO3_AVAILABLE:
            print(f"✗ {self.name} kullanılamıyor: Kütüphane kurulu değil")
            return
        
        try:
            # AWS credentials kontrolü
            access_key = os.getenv('AWS_ACCESS_KEY_ID')
            secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
            region = os.getenv('AWS_REGION', 'us-east-1')
            
            if not access_key or not secret_key:
                print(f"⚠ {self.name}: AWS credentials ayarlanmamış")
                return
            
            # Client oluştur
            self.client = boto3.client(
                'translate',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )
            
            # Test çevirisi
            self._test_connection()
            
        except NoCredentialsError:
            print(f"✗ {self.name}: AWS credentials bulunamadı")
            self._is_available = False
        except Exception as e:
            print(f"✗ {self.name} başlatma hatası: {e}")
            self._is_available = False
    
    def _test_connection(self):
        """API bağlantısını test et"""
        try:
            result = self.client.translate_text(
                Text='test',
                SourceLanguageCode='en',
                TargetLanguageCode='tr'
            )
            
            if result and 'TranslatedText' in result:
                self._is_available = True
                print(f"✓ {self.name} hazır")
            
        except Exception as e:
            print(f"✗ {self.name} test hatası: {e}")
    
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
            result = self.client.translate_text(
                Text=text,
                SourceLanguageCode=source_lang,
                TargetLanguageCode=target_lang
            )
            
            return result['TranslatedText']
            
        except ClientError as e:
            print(f"✗ {self.name} API hatası: {e}")
            return None
        except Exception as e:
            print(f"✗ {self.name} çeviri hatası: {e}")
            return None
    
    def batch_translate(self, texts: List[str], source_lang: str = 'en', 
                       target_lang: str = 'tr') -> List[Optional[str]]:
        """
        Toplu metin çevirisi
        
        Not: Amazon Translate native batch desteği yok, tek tek çeviriyoruz
        
        Args:
            texts: Çevrilecek metinler listesi
            source_lang: Kaynak dil kodu
            target_lang: Hedef dil kodu
        
        Returns:
            Çevrilmiş metinler listesi
        """
        if not self._is_available:
            return [None] * len(texts)
        
        translations = []
        
        for text in texts:
            translation = self.translate(text, source_lang, target_lang)
            translations.append(translation)
        
        return translations
    
    def estimate_cost(self, char_count: int) -> float:
        """
        Maliyet tahmini
        
        Args:
            char_count: Karakter sayısı
        
        Returns:
            Tahmini maliyet (USD)
        """
        # Amazon Translate: $15 per 1M characters
        # Free tier: 2M characters/month (12 months)
        cost_per_million = 15.0
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
            response = self.client.list_languages()
            return [lang['LanguageCode'] for lang in response['Languages']]
        except Exception as e:
            print(f"✗ {self.name} dil listesi hatası: {e}")
            return []
