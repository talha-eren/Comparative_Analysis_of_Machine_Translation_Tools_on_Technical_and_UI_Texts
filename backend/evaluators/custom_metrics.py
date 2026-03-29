"""Özel değerlendirme metrikleri"""

import re
from typing import List, Dict, Set

def calculate_terminology_consistency(translations: List[str], glossary: Dict[str, str]) -> float:
    """
    Terminoloji tutarlılığını hesapla
    
    Glossary'deki terimlerin çevirilerde doğru kullanılıp kullanılmadığını kontrol eder.
    
    Args:
        translations: Çeviri listesi
        glossary: Terim sözlüğü {kaynak_terim: hedef_terim}
    
    Returns:
        Tutarlılık skoru (0-1 arası)
    """
    if not glossary or not translations:
        return 1.0
    
    total_terms = 0
    correct_terms = 0
    
    for translation in translations:
        translation_lower = translation.lower()
        
        for source_term, target_term in glossary.items():
            if source_term.lower() in translation_lower:
                total_terms += 1
                if target_term.lower() in translation_lower:
                    correct_terms += 1
    
    if total_terms == 0:
        return 1.0
    
    return correct_terms / total_terms

def check_placeholder_preservation(source: str, translation: str) -> Dict[str, bool]:
    """
    Placeholder'ların korunup korunmadığını kontrol et
    
    Placeholder'lar: %s, %d, {variable}, <tag>, ${var}, {{var}}
    
    Args:
        source: Kaynak metin
        translation: Çeviri metni
    
    Returns:
        Kontrol sonuçları dict
    """
    # Placeholder pattern'leri
    patterns = {
        'percent': r'%[sd]',           # %s, %d
        'curly': r'\{[^}]+\}',         # {variable}
        'angle': r'<[^>]+>',           # <tag>
        'dollar_curly': r'\$\{[^}]+\}', # ${var}
        'double_curly': r'\{\{[^}]+\}\}' # {{var}}
    }
    
    results = {
        'all_preserved': True,
        'details': {}
    }
    
    for pattern_name, pattern in patterns.items():
        source_matches = set(re.findall(pattern, source))
        translation_matches = set(re.findall(pattern, translation))
        
        preserved = source_matches == translation_matches
        
        results['details'][pattern_name] = {
            'preserved': preserved,
            'source_count': len(source_matches),
            'translation_count': len(translation_matches),
            'missing': list(source_matches - translation_matches),
            'extra': list(translation_matches - source_matches)
        }
        
        if not preserved:
            results['all_preserved'] = False
    
    return results

def calculate_length_ratio(source: str, translation: str) -> float:
    """
    Uzunluk oranını hesapla
    
    İdeal oran dile göre değişir. Türkçe genelde İngilizceden %10-20 daha uzun.
    
    Args:
        source: Kaynak metin
        translation: Çeviri metni
    
    Returns:
        Uzunluk oranı (translation_length / source_length)
    """
    if not source:
        return 0.0
    
    return len(translation) / len(source)

def detect_untranslated_words(translation: str, source_lang_dict: Set[str]) -> List[str]:
    """
    Çevrilmemiş kelimeleri tespit et
    
    Args:
        translation: Çeviri metni
        source_lang_dict: Kaynak dil kelime seti (İngilizce kelimeler)
    
    Returns:
        Çevrilmemiş kelimeler listesi
    """
    if not source_lang_dict:
        return []
    
    # Çevirideki kelimeleri al
    translation_words = set(re.findall(r'\b\w+\b', translation.lower()))
    
    # Kaynak dilde olan ama çevrilmemiş kelimeler
    untranslated = []
    
    for word in translation_words:
        if word in source_lang_dict and len(word) > 3:
            untranslated.append(word)
    
    return untranslated

def calculate_special_char_preservation(source: str, translation: str) -> float:
    """
    Özel karakterlerin korunma oranını hesapla
    
    Args:
        source: Kaynak metin
        translation: Çeviri metni
    
    Returns:
        Korunma oranı (0-1 arası)
    """
    special_chars = set(re.findall(r'[^\w\s]', source))
    
    if not special_chars:
        return 1.0
    
    preserved_count = sum(1 for char in special_chars if char in translation)
    
    return preserved_count / len(special_chars)

def evaluate_translation_quality(source: str, translation: str, reference: str, 
                                glossary: Dict[str, str] = None) -> Dict:
    """
    Çeviri kalitesini çoklu metrikle değerlendir
    
    Args:
        source: Kaynak metin
        translation: Çeviri metni
        reference: Referans çeviri
        glossary: Terim sözlüğü (opsiyonel)
    
    Returns:
        Tüm metrik sonuçları
    """
    from .bleu_scorer import calculate_all_metrics as calc_bleu_metrics
    from .meteor_scorer import calculate_meteor
    
    results = {
        'automatic_metrics': calc_bleu_metrics(translation, reference),
        'meteor': calculate_meteor(translation, reference),
        'length_ratio': calculate_length_ratio(source, translation),
        'placeholder_preservation': check_placeholder_preservation(source, translation),
        'special_char_preservation': calculate_special_char_preservation(source, translation)
    }
    
    if glossary:
        results['terminology_consistency'] = calculate_terminology_consistency(
            [translation], glossary
        )
    
    return results
