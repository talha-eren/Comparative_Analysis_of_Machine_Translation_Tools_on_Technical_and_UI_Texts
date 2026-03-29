"""METEOR metriği hesaplama (NLTK kullanarak)"""

from collections import Counter
from typing import Optional

try:
    import nltk
    from nltk.translate.meteor_score import meteor_score
    NLTK_AVAILABLE = True
    
    # NLTK verilerini indir (ilk çalıştırmada)
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        print("NLTK WordNet indiriliyor...")
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
        
except ImportError:
    NLTK_AVAILABLE = False
    print("⚠ nltk kurulu değil")


def _normalize_text(text: str) -> str:
    """Karşılaştırma öncesi metni normalize et."""
    return " ".join((text or "").strip().split())


def _simple_token_f1(hypothesis: str, reference: str) -> float:
    """NLTK yoksa veya kısa metinlerde kullanılacak token-F1 benzerlik skoru (0-1)."""
    hyp_tokens = _normalize_text(hypothesis).casefold().split()
    ref_tokens = _normalize_text(reference).casefold().split()

    if not hyp_tokens and not ref_tokens:
        return 1.0
    if not hyp_tokens or not ref_tokens:
        return 0.0

    hyp_counter = Counter(hyp_tokens)
    ref_counter = Counter(ref_tokens)
    overlap = sum((hyp_counter & ref_counter).values())

    precision = overlap / len(hyp_tokens)
    recall = overlap / len(ref_tokens)

    if precision + recall == 0:
        return 0.0

    return (2 * precision * recall) / (precision + recall)

def calculate_meteor(hypothesis: str, reference: str) -> Optional[float]:
    """
    METEOR skoru hesapla
    
    METEOR (Metric for Evaluation of Translation with Explicit Ordering)
    eş anlamlı kelime desteği ve recall odaklı bir metriktir.
    
    Args:
        hypothesis: Çeviri (sistem çıktısı)
        reference: Referans çeviri
    
    Returns:
        METEOR skoru (0-1 arası) veya None
    """
    hypothesis = _normalize_text(hypothesis)
    reference = _normalize_text(reference)

    if not hypothesis and not reference:
        return 1.0
    if not hypothesis or not reference:
        return 0.0

    if hypothesis.casefold() == reference.casefold():
        return 1.0

    # Kisa UI metinlerinde token-F1 daha kararlı ve sezgiseldir.
    if len(hypothesis.split()) <= 2 and len(reference.split()) <= 2:
        return _simple_token_f1(hypothesis, reference)

    if not NLTK_AVAILABLE:
        return _simple_token_f1(hypothesis, reference)
    
    try:
        # METEOR tokenization gerektirir
        hypothesis_tokens = hypothesis.split()
        reference_tokens = reference.split()
        
        # METEOR skoru hesapla
        score = meteor_score([reference_tokens], hypothesis_tokens)
        
        return score
        
    except Exception as e:
        print(f"✗ METEOR hesaplama hatası: {e}")
        return _simple_token_f1(hypothesis, reference)

def batch_calculate_meteor(hypotheses: list, references: list) -> list:
    """
    Toplu METEOR hesaplama
    
    Args:
        hypotheses: Çeviriler listesi
        references: Referans çeviriler listesi
    
    Returns:
        METEOR skorları listesi
    """
    scores = []
    for hyp, ref in zip(hypotheses, references):
        score = calculate_meteor(hyp, ref)
        scores.append(score)
    
    return scores
