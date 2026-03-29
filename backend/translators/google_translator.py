"""Google Cloud Translation API wrapper (API key REST veya servis hesabı)"""

import os
from typing import List, Optional

import requests

from .base_translator import BaseTranslator

_GOOGLE_TRANSLATE_V2 = "https://translation.googleapis.com/language/translate/v2"

try:
    from google.cloud import translate_v2 as translate

    GOOGLE_CLIENT_AVAILABLE = True
except ImportError:
    GOOGLE_CLIENT_AVAILABLE = False
    print("[!] google-cloud-translate kurulu degil (servis hesabi modu kapali)")


class GoogleTranslator(BaseTranslator):
    """Google Cloud Translation API wrapper sınıfı"""

    def __init__(self):
        super().__init__("Google Translate")
        self._mode: Optional[str] = None
        self.client = None
        self._api_key: Optional[str] = None

        self._api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if self._api_key:
            self._mode = "rest"
            self._is_available = True
            print(f"[OK] {self.name} hazir (API anahtari)")
            return

        if not GOOGLE_CLIENT_AVAILABLE:
            print(f"[X] {self.name} kullanilamiyor: Kutuphane kurulu degil")
            return

        try:
            credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if not credentials_path:
                print(f"[!] {self.name}: GOOGLE_TRANSLATE_API_KEY veya GOOGLE_APPLICATION_CREDENTIALS ayarlanmamis")
                return

            if not os.path.exists(credentials_path):
                print(f"[!] {self.name}: Credentials dosyasi bulunamadi: {credentials_path}")
                return

            self.client = translate.Client()
            self._mode = "client"
            self._is_available = True
            print(f"[OK] {self.name} hazir (servis hesabi)")

        except Exception as e:
            print(f"[X] {self.name} baslatma hatasi: {e}")
            self._is_available = False

    def _translate_rest(
        self, texts: List[str], source_lang: str, target_lang: str
    ) -> List[Optional[str]]:
        if not texts:
            return []
        params = {"key": self._api_key}
        body = {
            "q": texts,
            "source": source_lang,
            "target": target_lang,
            "format": "text",
        }
        try:
            r = requests.post(_GOOGLE_TRANSLATE_V2, params=params, json=body, timeout=60)
            r.raise_for_status()
            data = r.json()
            trans = data.get("data", {}).get("translations", [])
            return [t.get("translatedText") for t in trans]
        except Exception as e:
            print(f"[X] {self.name} REST ceviri hatasi: {e}")
            return [None] * len(texts)

    def translate(self, text: str, source_lang: str = "en", target_lang: str = "tr") -> Optional[str]:
        if not self._is_available:
            return None

        if self._mode == "rest":
            out = self._translate_rest([text], source_lang, target_lang)
            return out[0] if out else None

        try:
            result = self.client.translate(
                text,
                source_language=source_lang,
                target_language=target_lang,
                format_="text",
            )
            return result["translatedText"]
        except Exception as e:
            print(f"[X] {self.name} ceviri hatasi: {e}")
            return None

    def batch_translate(
        self, texts: List[str], source_lang: str = "en", target_lang: str = "tr"
    ) -> List[Optional[str]]:
        if not self._is_available:
            return [None] * len(texts)

        if self._mode == "rest":
            chunk_size = 100
            out: List[Optional[str]] = []
            for i in range(0, len(texts), chunk_size):
                chunk = texts[i : i + chunk_size]
                out.extend(self._translate_rest(chunk, source_lang, target_lang))
            return out

        try:
            results = self.client.translate(
                texts,
                source_language=source_lang,
                target_language=target_lang,
                format_="text",
            )
            if isinstance(results, list):
                return [r["translatedText"] for r in results]
            return [results["translatedText"]]
        except Exception as e:
            print(f"[X] {self.name} toplu ceviri hatasi: {e}")
            return [None] * len(texts)

    def estimate_cost(self, char_count: int) -> float:
        cost_per_million = 20.0
        return (char_count / 1_000_000) * cost_per_million

    def get_supported_languages(self) -> List[str]:
        if not self._is_available:
            return []

        if self._mode == "rest":
            try:
                r = requests.get(
                    f"{_GOOGLE_TRANSLATE_V2}/languages",
                    params={"key": self._api_key, "target": "en"},
                    timeout=30,
                )
                r.raise_for_status()
                data = r.json()
                return [lang["language"] for lang in data.get("data", {}).get("languages", [])]
            except Exception as e:
                print(f"[X] {self.name} dil listesi hatasi: {e}")
                return []

        try:
            results = self.client.get_languages()
            return [lang["language"] for lang in results]
        except Exception as e:
            print(f"[X] {self.name} dil listesi hatasi: {e}")
            return []
