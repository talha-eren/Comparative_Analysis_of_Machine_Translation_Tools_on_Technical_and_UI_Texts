"""BLEU, chrF++ ve TER metriklerini hesaplama (SacreBLEU kullanarak)."""

from difflib import SequenceMatcher
from typing import Optional

try:
    import sacrebleu
    SACREBLEU_AVAILABLE = True
except ImportError:
    SACREBLEU_AVAILABLE = False
    print("⚠ sacrebleu kurulu değil")


def _normalize_text(text: str) -> str:
    """Karşılaştırma öncesi metni normalize et."""
    return " ".join((text or "").strip().split())


def _fallback_similarity(hypothesis: str, reference: str) -> float:
    """SacreBLEU yoksa kullanılacak basit benzerlik skoru (0-1)."""
    hyp = _normalize_text(hypothesis)
    ref = _normalize_text(reference)

    if not hyp and not ref:
        return 1.0
    if not hyp or not ref:
        return 0.0

    return SequenceMatcher(None, hyp.casefold(), ref.casefold()).ratio()

def calculate_bleu(hypothesis: str, reference: str) -> Optional[float]:
    """
    BLEU skoru hesapla
    
    Args:
        hypothesis: Çeviri (sistem çıktısı)
        reference: Referans çeviri (doğru çeviri)
    
    Returns:
        BLEU skoru (0-100 arası) veya None
    """
    hypothesis = _normalize_text(hypothesis)
    reference = _normalize_text(reference)

    if not hypothesis and not reference:
        return 1.0
    if not hypothesis or not reference:
        return 0.0

    if not SACREBLEU_AVAILABLE:
        return _fallback_similarity(hypothesis, reference)
    
    try:
        # Segment bazli degerlendirmede sentence_bleu, kisa metinlerde daha stabildir.
        bleu = sacrebleu.sentence_bleu(
            hypothesis,
            [reference],
            smooth_method='exp'
        )
        return bleu.score / 100.0  # 0-1 arasına normalize et
        
    except Exception as e:
        print(f"✗ BLEU hesaplama hatası: {e}")
        return _fallback_similarity(hypothesis, reference)

def calculate_chrf(hypothesis: str, reference: str) -> Optional[float]:
    """
    chrF++ skoru hesapla
    
    Args:
        hypothesis: Çeviri (sistem çıktısı)
        reference: Referans çeviri
    
    Returns:
        chrF++ skoru (0-1 arası) veya None
    """
    hypothesis = _normalize_text(hypothesis)
    reference = _normalize_text(reference)

    if not hypothesis and not reference:
        return 1.0
    if not hypothesis or not reference:
        return 0.0

    if not SACREBLEU_AVAILABLE:
        return _fallback_similarity(hypothesis, reference)
    
    try:
        chrf = sacrebleu.sentence_chrf(hypothesis, [reference])
        return chrf.score / 100.0  # 0-1 arasına normalize et
        
    except Exception as e:
        print(f"✗ chrF hesaplama hatası: {e}")
        return _fallback_similarity(hypothesis, reference)

def calculate_ter(hypothesis: str, reference: str) -> Optional[float]:
    """
    TER (Translation Error Rate) hesapla
    
    Args:
        hypothesis: Çeviri (sistem çıktısı)
        reference: Referans çeviri
    
    Returns:
        TER skoru (0-1 arası, düşük = daha iyi) veya None
    """
    hypothesis = _normalize_text(hypothesis)
    reference = _normalize_text(reference)

    if not hypothesis and not reference:
        return 0.0
    if not hypothesis or not reference:
        return 1.0

    if not SACREBLEU_AVAILABLE:
        return 1.0 - _fallback_similarity(hypothesis, reference)
    
    try:
        ter = sacrebleu.sentence_ter(hypothesis, [reference])
        return ter.score / 100.0  # 0-1 arasına normalize et
        
    except Exception as e:
        print(f"✗ TER hesaplama hatası: {e}")
        return 1.0 - _fallback_similarity(hypothesis, reference)

def calculate_all_metrics(hypothesis: str, reference: str) -> dict:
    """
    Tüm SacreBLEU metriklerini hesapla
    
    Args:
        hypothesis: Çeviri
        reference: Referans çeviri
    
    Returns:
        Metrik skorları dict
    """
    return {
        'bleu': calculate_bleu(hypothesis, reference),
        'chrf': calculate_chrf(hypothesis, reference),
        'ter': calculate_ter(hypothesis, reference)
    }

def batch_calculate_bleu(hypotheses: list, references: list) -> list:
    """
    Toplu BLEU hesaplama
    
    Args:
        hypotheses: Çeviriler listesi
        references: Referans çeviriler listesi
    
    Returns:
        BLEU skorları listesi
    """
    scores = []
    for hyp, ref in zip(hypotheses, references):
        score = calculate_bleu(hyp, ref)
        scores.append(score)
    
    return scores
