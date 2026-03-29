"""Özel değerlendirme metrikleri"""

import math
import re
from difflib import SequenceMatcher
from typing import List, Dict, Optional, Set

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

def _clamp_01(value: float) -> float:
    """Skoru 0-1 aralığında sınırla."""
    return max(0.0, min(1.0, value))

def _tokenize(text: str) -> List[str]:
    """Basit ve dil bağımsız tokenizasyon."""
    if not text:
        return []
    return re.findall(r"\b\w+\b", text.lower())

def _length_adequacy(source: str, translation: str) -> float:
    """Kaynak/hedef uzunluk uyumuna göre yeterlilik skoru (0-1)."""
    src_tokens = _tokenize(source)
    trg_tokens = _tokenize(translation)

    if not src_tokens and not trg_tokens:
        return 1.0
    if not src_tokens or not trg_tokens:
        return 0.0

    ratio = len(trg_tokens) / len(src_tokens)
    # 1.0 etrafındaki log sapmasını cezalandırarak hem kısa hem uzun metinlerde dengeli skor üret.
    deviation = abs(math.log(max(ratio, 1e-9)))
    return _clamp_01(1.0 - (deviation / math.log(2.5)))

def _fluency_proxy(translation: str) -> float:
    """Referanssız akıcılık göstergesi: tekrar ve tekrarlı noktalama cezası."""
    tokens = _tokenize(translation)

    if not tokens:
        return 0.0
    if len(tokens) == 1:
        return 1.0

    unique_ratio = len(set(tokens)) / len(tokens)
    repeated_punct = len(re.findall(r"([!?.,])\1{1,}", translation))
    punct_penalty = min(0.2, repeated_punct * 0.05)

    return _clamp_01(unique_ratio - punct_penalty)

def _round_trip_consistency(source: str, back_translation: str) -> float:
    """Round-trip (hedef->kaynak) tutarlılığına göre semantik benzerlik tahmini."""
    source = (source or "").strip()
    back_translation = (back_translation or "").strip()

    if not source and not back_translation:
        return 1.0
    if not source or not back_translation:
        return 0.0

    try:
        # Aynı dilde (kaynak) karşılaştırma için chrF oldukça güçlü bir göstergedir.
        from .bleu_scorer import calculate_chrf
        chrf_score = calculate_chrf(back_translation, source)
        if chrf_score is not None:
            return _clamp_01(chrf_score)
    except Exception:
        pass

    return _clamp_01(SequenceMatcher(None, source.casefold(), back_translation.casefold()).ratio())

def evaluate_without_reference(source: str, translation: str, back_translation: Optional[str] = None) -> Dict[str, float]:
    """
    Referans metin yokken çeviri kalitesini sezgisel metriklerle tahmin et.

    Üretilen skorlar 0-1 aralığındadır ve karşılaştırmalı değerlendirme için uygundur.
    """
    source = (source or "").strip()
    translation = (translation or "").strip()

    if not source and not translation:
        return {
            'estimated_accuracy': 1.0,
            'adequacy': 1.0,
            'fluency': 1.0,
            'format_preservation': 1.0,
            'completeness': 1.0,
            'untranslated_penalty': 0.0
        }

    if not translation:
        return {
            'estimated_accuracy': 0.0,
            'adequacy': 0.0,
            'fluency': 0.0,
            'format_preservation': 0.0,
            'completeness': 0.0,
            'untranslated_penalty': 1.0
        }

    length_adequacy = _length_adequacy(source, translation)
    fluency = _fluency_proxy(translation)

    placeholder_info = check_placeholder_preservation(source, translation)
    placeholder_score = 1.0 if placeholder_info.get('all_preserved') else 0.6

    special_char_score = calculate_special_char_preservation(source, translation)
    format_preservation = _clamp_01((placeholder_score * 0.6) + (special_char_score * 0.4))

    source_words = set(_tokenize(source))
    untranslated_words = detect_untranslated_words(translation, source_words)
    untranslated_penalty = 0.0
    if source_words:
        untranslated_penalty = min(1.0, len(untranslated_words) / max(len(source_words), 1))

    completeness = _clamp_01(1.0 - untranslated_penalty)

    base_estimated_accuracy = _clamp_01(
        (length_adequacy * 0.35) +
        (fluency * 0.25) +
        (format_preservation * 0.20) +
        (completeness * 0.20)
    )

    round_trip_score = None
    estimated_accuracy = base_estimated_accuracy

    if back_translation is not None:
        round_trip_score = _round_trip_consistency(source, back_translation)
        # Hybrid QE: heuristik kalite + round-trip tutarlılık birlikte değerlendirilir.
        estimated_accuracy = _clamp_01((base_estimated_accuracy * 0.65) + (round_trip_score * 0.35))

    return {
        'estimated_accuracy': estimated_accuracy,
        'base_estimated_accuracy': base_estimated_accuracy,
        'adequacy': length_adequacy,
        'fluency': fluency,
        'format_preservation': format_preservation,
        'completeness': completeness,
        'untranslated_penalty': untranslated_penalty,
        'round_trip_consistency': round_trip_score
    }

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
