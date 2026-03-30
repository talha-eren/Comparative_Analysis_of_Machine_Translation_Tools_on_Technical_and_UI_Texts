"""BLEU, chrF++ ve TER metriklerini hesaplama (SacreBLEU kullanarak)"""

from typing import Optional

try:
    import sacrebleu
    SACREBLEU_AVAILABLE = True
except ImportError:
    SACREBLEU_AVAILABLE = False
    print("⚠ sacrebleu kurulu değil")


def _is_short_text(hypothesis: str, reference: str) -> bool:
    """Kisa stringler için sentence-level metric daha stabildir."""
    hyp_tokens = (hypothesis or "").split()
    ref_tokens = (reference or "").split()
    return min(len(hyp_tokens), len(ref_tokens)) <= 6

def calculate_bleu(hypothesis: str, reference: str) -> Optional[float]:
    """
    BLEU skoru hesapla
    
    Args:
        hypothesis: Çeviri (sistem çıktısı)
        reference: Referans çeviri (doğru çeviri)
    
    Returns:
        BLEU skoru (0-100 arası) veya None
    """
    if not SACREBLEU_AVAILABLE:
        return None
    
    try:
        if _is_short_text(hypothesis, reference) and hasattr(sacrebleu, 'sentence_bleu'):
            bleu = sacrebleu.sentence_bleu(hypothesis, [reference])
        else:
            bleu = sacrebleu.corpus_bleu([hypothesis], [[reference]])
        return bleu.score / 100.0  # 0-1 arasına normalize et
        
    except Exception as e:
        print(f"✗ BLEU hesaplama hatası: {e}")
        return None

def calculate_chrf(hypothesis: str, reference: str) -> Optional[float]:
    """
    chrF++ skoru hesapla
    
    Args:
        hypothesis: Çeviri (sistem çıktısı)
        reference: Referans çeviri
    
    Returns:
        chrF++ skoru (0-1 arası) veya None
    """
    if not SACREBLEU_AVAILABLE:
        return None
    
    try:
        if _is_short_text(hypothesis, reference) and hasattr(sacrebleu, 'sentence_chrf'):
            chrf = sacrebleu.sentence_chrf(hypothesis, [reference])
        else:
            chrf = sacrebleu.corpus_chrf([hypothesis], [[reference]])
        return chrf.score / 100.0  # 0-1 arasına normalize et
        
    except Exception as e:
        print(f"✗ chrF hesaplama hatası: {e}")
        return None

def calculate_ter(hypothesis: str, reference: str) -> Optional[float]:
    """
    TER (Translation Error Rate) hesapla
    
    Args:
        hypothesis: Çeviri (sistem çıktısı)
        reference: Referans çeviri
    
    Returns:
        TER skoru (0-1 arası, düşük = daha iyi) veya None
    """
    if not SACREBLEU_AVAILABLE:
        return None
    
    try:
        if _is_short_text(hypothesis, reference) and hasattr(sacrebleu, 'sentence_ter'):
            ter = sacrebleu.sentence_ter(hypothesis, [reference])
        else:
            ter = sacrebleu.corpus_ter([hypothesis], [[reference]])
        return ter.score / 100.0  # 0-1 arasına normalize et
        
    except Exception as e:
        print(f"✗ TER hesaplama hatası: {e}")
        return None

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
    if not SACREBLEU_AVAILABLE:
        return [None] * len(hypotheses)
    
    scores = []
    for hyp, ref in zip(hypotheses, references):
        score = calculate_bleu(hyp, ref)
        scores.append(score)
    
    return scores
