"""Dataset yükleme sınıfı"""

import json
from pathlib import Path
from typing import List, Dict, Optional

class DatasetLoader:
    """Dataset yükleme ve yönetme sınıfı"""
    
    def __init__(self, data_dir: str = "data/processed"):
        """
        Args:
            data_dir: İşlenmiş veri dizini
        """
        self.data_dir = Path(data_dir)
        self.datasets = {}
    
    def load_all_datasets(self):
        """Tüm dataset'leri yükle"""
        dataset_files = {
            'technical': self.data_dir / 'technical_dataset.json',
            'ui': self.data_dir / 'ui_dataset.json',
            'error': self.data_dir / 'error_dataset.json',
            'train': self.data_dir / 'train_set.json',
            'test': self.data_dir / 'test_set.json',
            'all': self.data_dir / 'all_dataset.json'
        }
        
        for name, path in dataset_files.items():
            if path.exists():
                self.datasets[name] = self._load_json(path)
                print(f"✓ {name}: {len(self.datasets[name])} segment")
            else:
                print(f"⚠ {name} bulunamadı: {path}")
    
    def _load_json(self, file_path: Path) -> List[Dict]:
        """JSON dosyasını yükle"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"✗ Dosya yükleme hatası: {e}")
            return []
    
    def get_dataset(self, name: str) -> Optional[List[Dict]]:
        """
        Belirli bir dataset'i al
        
        Args:
            name: Dataset adı (technical, ui, error, train, test, all)
        
        Returns:
            Dataset listesi veya None
        """
        return self.datasets.get(name)
    
    def get_sample(self, dataset_name: str, size: int = 100, 
                   category: Optional[str] = None) -> List[Dict]:
        """
        Dataset'ten örnek al
        
        Args:
            dataset_name: Dataset adı
            size: Örnek boyutu
            category: Kategori filtresi (opsiyonel)
        
        Returns:
            Örnek segment listesi
        """
        dataset = self.get_dataset(dataset_name)
        
        if not dataset:
            return []
        
        # Kategori filtresi
        if category:
            dataset = [s for s in dataset if s.get('category') == category]
        
        # Örnek al
        import random
        return random.sample(dataset, min(size, len(dataset)))
    
    def get_statistics(self) -> Dict:
        """
        Dataset istatistiklerini al
        
        Returns:
            İstatistikler dict
        """
        stats = {}
        
        for name, dataset in self.datasets.items():
            if dataset:
                stats[name] = {
                    'total_segments': len(dataset),
                    'avg_length': sum(s.get('length', 0) for s in dataset) / len(dataset),
                    'categories': self._count_categories(dataset),
                    'sources': self._count_sources(dataset)
                }
        
        return stats
    
    def _count_categories(self, dataset: List[Dict]) -> Dict[str, int]:
        """Kategori dağılımını say"""
        from collections import Counter
        categories = [s.get('category', 'unknown') for s in dataset]
        return dict(Counter(categories))
    
    def _count_sources(self, dataset: List[Dict]) -> Dict[str, int]:
        """Kaynak dağılımını say"""
        from collections import Counter
        sources = [s.get('source', 'unknown') for s in dataset]
        return dict(Counter(sources))
