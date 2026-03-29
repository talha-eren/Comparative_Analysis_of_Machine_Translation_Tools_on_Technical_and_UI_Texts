"""Veri temizleme sınıfı"""

import re
from typing import List, Dict

class DataCleaner:
    """Veri temizleme ve normalizasyon sınıfı"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Metni temizle
        
        Args:
            text: Ham metin
        
        Returns:
            Temizlenmiş metin
        """
        # Başındaki/sonundaki boşlukları temizle
        text = text.strip()
        
        # Çoklu boşlukları tek boşluğa indir
        text = ' '.join(text.split())
        
        # Kontrol karakterlerini temizle
        text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
        
        return text
    
    @staticmethod
    def is_valid_segment(segment: Dict) -> bool:
        """
        Segment'in geçerli olup olmadığını kontrol et
        
        Args:
            segment: Segment dict
        
        Returns:
            Boolean
        """
        source = segment.get('source_text', '').strip()
        target = segment.get('target_text', '').strip()
        
        # Temel kontroller
        if not source or not target:
            return False
        
        # Uzunluk kontrolleri
        if len(source) < 5 or len(source) > 1000:
            return False
        
        if len(target) < 5 or len(target) > 1000:
            return False
        
        # Sadece sayı olmamalı
        if source.isdigit() or target.isdigit():
            return False
        
        # Çok fazla özel karakter olmamalı
        special_char_ratio = len(re.findall(r'[^\w\s]', source)) / len(source)
        if special_char_ratio > 0.5:
            return False
        
        return True
    
    @staticmethod
    def remove_duplicates(segments: List[Dict]) -> List[Dict]:
        """
        Duplikasyonları temizle
        
        Args:
            segments: Segment listesi
        
        Returns:
            Benzersiz segment listesi
        """
        seen = set()
        unique = []
        
        for segment in segments:
            key = (segment['source_text'], segment['target_text'])
            
            if key not in seen:
                seen.add(key)
                unique.append(segment)
        
        return unique
    
    @staticmethod
    def normalize_segments(segments: List[Dict]) -> List[Dict]:
        """
        Segment'leri normalize et
        
        Args:
            segments: Segment listesi
        
        Returns:
            Normalize edilmiş segment listesi
        """
        normalized = []
        
        for segment in segments:
            # Metinleri temizle
            segment['source_text'] = DataCleaner.clean_text(segment['source_text'])
            segment['target_text'] = DataCleaner.clean_text(segment['target_text'])
            
            # Uzunluğu güncelle
            segment['length'] = len(segment['source_text'])
            
            # Geçerli mi kontrol et
            if DataCleaner.is_valid_segment(segment):
                normalized.append(segment)
        
        return normalized
