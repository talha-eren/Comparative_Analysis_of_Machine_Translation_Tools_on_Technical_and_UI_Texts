"""COMET metriği hesaplama (unbabel-comet kullanarak)"""

from typing import Optional
import threading

try:
    from comet import download_model, load_from_checkpoint
    COMET_AVAILABLE = True
except ImportError:
    COMET_AVAILABLE = False
    print("WARN: unbabel-comet kurulu degil")


_COMET_MODEL = None
_COMET_LOCK = threading.Lock()


def _get_comet_model():
    """COMET modelini lazy olarak yukle."""
    global _COMET_MODEL
    if not COMET_AVAILABLE:
        return None

    with _COMET_LOCK:
        if _COMET_MODEL is None:
            model_path = download_model("Unbabel/wmt22-comet-da")
            _COMET_MODEL = load_from_checkpoint(model_path)
    return _COMET_MODEL


def calculate_comet(source: str, hypothesis: str, reference: str) -> Optional[float]:
    """
    COMET skoru hesapla

    Args:
        source: Kaynak metin
        hypothesis: Sistem çevirisi (MT)
        reference: Referans çeviri

    Returns:
        COMET skoru (genelde 0-1 arasi) veya None
    """
    if not COMET_AVAILABLE:
        return None

    if not source or not hypothesis or not reference:
        return None

    try:
        model = _get_comet_model()
        if model is None:
            return None

        data = [{"src": source, "mt": hypothesis, "ref": reference}]
        output = model.predict(data, batch_size=1, gpus=0)

        if hasattr(output, "scores") and output.scores:
            return float(output.scores[0])
        if isinstance(output, dict):
            scores = output.get("scores")
            if scores:
                return float(scores[0])

        return None
    except Exception as e:
        print(f"ERROR: COMET hesaplama hatasi: {e}")
        return None
