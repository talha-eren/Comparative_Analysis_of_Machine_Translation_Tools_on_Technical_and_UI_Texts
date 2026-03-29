"""Microsoft Azure Translator API wrapper"""

import os
import uuid
import requests
from typing import List, Optional
from .base_translator import BaseTranslator

class MicrosoftTranslator(BaseTranslator):
    """Microsoft Azure Translator API wrapper sınıfı"""
    
    def __init__(self):
        super().__init__("Microsoft Translator")
        
        try:
            self.key = os.getenv('AZURE_TRANSLATOR_KEY')
            self.region = os.getenv('AZURE_TRANSLATOR_REGION', 'global')
            self.endpoint = os.getenv('AZURE_TRANSLATOR_ENDPOINT', 
                                     'https://api.cognitive.microsofttranslator.com')
            
            if not self.key:
                print(f"[!] {self.name}: AZURE_TRANSLATOR_KEY ayarlanmamis")
                return
            
            # Test isteği
            self._test_connection()
            
        except Exception as e:
            print(f"[X] {self.name} baslatma hatasi: {e}")
            self._is_available = False
    
    def _test_connection(self):
        """API baglantisını test et"""
        try:
            path = '/translate'
            constructed_url = self.endpoint + path
            
            params = {
                'api-version': '3.0',
                'from': 'en',
                'to': 'tr'
            }
            
            headers = {
                'Ocp-Apim-Subscription-Key': self.key,
                'Ocp-Apim-Subscription-Region': self.region,
                'Content-type': 'application/json',
                'X-ClientTraceId': str(uuid.uuid4())
            }
            
            body = [{'text': 'test'}]
            
            response = requests.post(constructed_url, params=params, 
                                    headers=headers, json=body, timeout=5)
            
            if response.status_code == 200:
                self._is_available = True
                print(f"[OK] {self.name} hazir")
            else:
                print(f"[X] {self.name} baglanti hatasi: {response.status_code}")
                
        except Exception as e:
            print(f"[X] {self.name} test hatasi: {e}")
    
    def translate(self, text: str, source_lang: str = 'en', target_lang: str = 'tr') -> Optional[str]:
        """
        Tekil metin cevirisi
        
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
            path = '/translate'
            constructed_url = self.endpoint + path
            
            params = {
                'api-version': '3.0',
                'from': source_lang,
                'to': target_lang
            }
            
            headers = {
                'Ocp-Apim-Subscription-Key': self.key,
                'Ocp-Apim-Subscription-Region': self.region,
                'Content-type': 'application/json',
                'X-ClientTraceId': str(uuid.uuid4())
            }
            
            body = [{'text': text}]
            
            response = requests.post(constructed_url, params=params, 
                                    headers=headers, json=body, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result[0]['translations'][0]['text']
            else:
                print(f"[X] {self.name} API hatasi: {response.status_code}")
                return None
            
        except Exception as e:
            print(f"[X] {self.name} ceviri hatasi: {e}")
            return None
    
    def batch_translate(self, texts: List[str], source_lang: str = 'en', 
                       target_lang: str = 'tr') -> List[Optional[str]]:
        """
        Toplu metin cevirisi
        
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
            path = '/translate'
            constructed_url = self.endpoint + path
            
            params = {
                'api-version': '3.0',
                'from': source_lang,
                'to': target_lang
            }
            
            headers = {
                'Ocp-Apim-Subscription-Key': self.key,
                'Ocp-Apim-Subscription-Region': self.region,
                'Content-type': 'application/json',
                'X-ClientTraceId': str(uuid.uuid4())
            }
            
            # Microsoft max 100 text/request
            body = [{'text': text} for text in texts[:100]]
            
            response = requests.post(constructed_url, params=params, 
                                    headers=headers, json=body, timeout=60)
            
            if response.status_code == 200:
                results = response.json()
                return [r['translations'][0]['text'] for r in results]
            else:
                print(f"[X] {self.name} API hatasi: {response.status_code}")
                return [None] * len(texts)
            
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
        # Microsoft Translator: $10 per 1M characters
        # Free tier: 2M characters/month
        cost_per_million = 10.0
        return (char_count / 1_000_000) * cost_per_million
