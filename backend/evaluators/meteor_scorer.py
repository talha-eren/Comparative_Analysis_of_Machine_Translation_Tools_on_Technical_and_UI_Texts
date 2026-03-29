"""METEOR metriği hesaplama (NLTK kullanarak)"""

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
    if not NLTK_AVAILABLE:
        return None
    
    try:
        # METEOR tokenization gerektirir
        hypothesis_tokens = hypothesis.split()
        reference_tokens = reference.split()
        
        # METEOR skoru hesapla
        score = meteor_score([reference_tokens], hypothesis_tokens)
        
        return score
        
    except Exception as e:
        print(f"✗ METEOR hesaplama hatası: {e}")
        return None

def batch_calculate_meteor(hypotheses: list, references: list) -> list:
    """
    Toplu METEOR hesaplama
    
    Args:
        hypotheses: Çeviriler listesi
        references: Referans çeviriler listesi
    
    Returns:
        METEOR skorları listesi
    """
    if not NLTK_AVAILABLE:
        return [None] * len(hypotheses)
    
    scores = []
    for hyp, ref in zip(hypotheses, references):
        score = calculate_meteor(hyp, ref)
        scores.append(score)
    
    return scores
