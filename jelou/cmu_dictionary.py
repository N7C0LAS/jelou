import urllib.request
from pathlib import Path
from typing import Dict, Optional

from jelou.arpabet_to_ipa import arpabet_to_ipa, arpabet_to_ipa_clean

CMU_DICT_URL = "https://raw.githubusercontent.com/cmusphinx/cmudict/master/cmudict.dict"
CACHE_DIR = Path.home() / ".jelou"
CACHE_FILE = CACHE_DIR / "cmudict.txt"


class CMUDictionary:

    def __init__(self):
        self._dict: Dict[str, str] = {}
        self._loaded = False

    def load(self, force_download: bool = False) -> None:
        if self._loaded and not force_download:
            return
        if CACHE_FILE.exists() and not force_download:
            self._load_from_file(CACHE_FILE)
        else:
            self._download_and_cache()
            self._load_from_file(CACHE_FILE)
        self._loaded = True

    def _download_and_cache(self) -> None:
        print("📥 Descargando CMU Pronouncing Dictionary...")
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        try:
            with urllib.request.urlopen(CMU_DICT_URL) as response:
                content = response.read().decode("utf-8")
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Diccionario descargado y guardado en: {CACHE_FILE}")
        except Exception as e:
            raise RuntimeError(f"Error descargando el diccionario CMU: {e}")

    def _score_variant(self, arpabet: str) -> tuple:
        tokens = arpabet.upper().split()
        hh_count = tokens.count("HH")
        ah0_count = tokens.count("AH0")
        uw0_count = tokens.count("UW0")
        return (hh_count, ah0_count, uw0_count)

    def _load_from_file(self, filepath: Path) -> None:
        print(f"📖 Cargando diccionario desde: {filepath}")

        _PREFER_EY = {
            'monday', 'tuesday', 'wednesday', 'thursday',
            'friday', 'saturday', 'sunday',
            "monday's", "tuesday's", "wednesday's", "thursday's",
            "friday's", "saturday's", "sunday's",
            'mondays', 'tuesdays', 'wednesdays', 'thursdays',
            'fridays', 'saturdays', 'sundays'
        }

        _MANUAL_OVERRIDES = {
            'saturday': 'S AE1 T ER0 D EY2',
            "saturday's": 'S AE1 T ER0 D EY2 Z',
            'saturdays': 'S AE1 T ER0 D EY2 Z',
        }

        _arpabet_cache: Dict[str, str] = {}

        for word, arpabet in _MANUAL_OVERRIDES.items():
            self._dict[word] = arpabet_to_ipa(arpabet)
            _arpabet_cache[word] = arpabet

        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(";;;"):
                    continue
                parts = line.split(maxsplit=1)
                if len(parts) < 2:
                    continue
                word_raw, arpabet = parts
                word = word_raw.split("(")[0].lower()
                is_variant = "(" in word_raw

                if word in _MANUAL_OVERRIDES:
                    continue

                if not is_variant:
                    self._dict[word] = arpabet_to_ipa(arpabet)
                    _arpabet_cache[word] = arpabet
                else:
                    current_arpabet = _arpabet_cache.get(word, "")
                    current_score = self._score_variant(current_arpabet)
                    new_score = self._score_variant(arpabet)

                    if word in _PREFER_EY and "EY" in arpabet.upper():
                        self._dict[word] = arpabet_to_ipa(arpabet)
                        _arpabet_cache[word] = arpabet
                    elif new_score < current_score:
                        self._dict[word] = arpabet_to_ipa(arpabet)
                        _arpabet_cache[word] = arpabet

        print(f"✅ Diccionario cargado: {len(self._dict)} palabras")

    def lookup_with_stress(self, word: str) -> Optional[str]:
        self.load()
        return self._dict.get(word.lower())

    def lookup(self, word: str) -> Optional[str]:
        if not self._loaded:
            self.load()
        result = self._dict.get(word.lower())
        if result:
            return result.replace("~~STRESS~~", "")
        return None

    def __len__(self) -> int:
        return len(self._dict)


_cmu_dict = CMUDictionary()


def get_dictionary() -> CMUDictionary:
    return _cmu_dict


def lookup_word(word: str) -> Optional[str]:
    return _cmu_dict.lookup(word)


def lookup_word_with_stress(word: str) -> Optional[str]:
    global _cmu_dict
    if _cmu_dict is None:
        _cmu_dict = get_dictionary()
    return _cmu_dict.lookup_with_stress(word)