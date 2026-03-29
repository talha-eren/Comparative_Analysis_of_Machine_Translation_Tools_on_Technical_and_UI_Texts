"""Yardımcı fonksiyonlar"""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

def load_dataset(dataset_path: str) -> List[Dict]:
    """
    Dataset dosyasını yükle
    
    Args:
        dataset_path: Dataset dosya yolu
    
    Returns:
        Dataset listesi
    """
    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"✗ Dataset yükleme hatası: {e}")
        return []

def save_results(results: Any, output_path: str):
    """
    Sonuçları JSON dosyasına kaydet
    
    Args:
        results: Kaydedilecek veri
        output_path: Çıktı dosya yolu
    """
    try:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Sonuçlar kaydedildi: {output_path}")
        
    except Exception as e:
        print(f"✗ Sonuç kaydetme hatası: {e}")

def format_time(seconds: float) -> str:
    """
    Saniyeyi okunabilir formata çevir
    
    Args:
        seconds: Saniye
    
    Returns:
        Formatlanmış string (örn: "2m 30s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

def calculate_statistics(scores: List[float]) -> Dict[str, float]:
    """
    Skor listesinden istatistikler hesapla
    
    Args:
        scores: Skor listesi
    
    Returns:
        İstatistikler dict
    """
    if not scores:
        return {}
    
    valid_scores = [s for s in scores if s is not None]
    
    if not valid_scores:
        return {}
    
    sorted_scores = sorted(valid_scores)
    n = len(sorted_scores)
    
    return {
        'mean': sum(valid_scores) / n,
        'median': sorted_scores[n // 2],
        'min': min(valid_scores),
        'max': max(valid_scores),
        'std': (sum((x - sum(valid_scores) / n) ** 2 for x in valid_scores) / n) ** 0.5,
        'count': n
    }

def create_timestamp() -> str:
    """
    Timestamp oluştur
    
    Returns:
        ISO format timestamp
    """
    return datetime.now().isoformat()

def sanitize_text(text: str) -> str:
    """
    Metni temizle (çeviri için hazırla)
    
    Args:
        text: Ham metin
    
    Returns:
        Temizlenmiş metin
    """
    # Başındaki/sonundaki boşlukları temizle
    text = text.strip()
    
    # Çoklu boşlukları tek boşluğa indir
    text = ' '.join(text.split())
    
    return text
