"""
Módulo para integración con CMU Pronouncing Dictionary.

El CMU Pronouncing Dictionary es un diccionario de pronunciación
de código abierto para inglés norteamericano.

URL: http://www.speech.cs.cmu.edu/cgi-bin/cmudict
"""

import urllib.request
from pathlib import Path
from typing import Dict, Optional

from jelou.arpabet_to_ipa import parse_cmu_line


# URL del diccionario CMU
CMU_DICT_URL = "https://raw.githubusercontent.com/cmusphinx/cmudict/master/cmudict.dict"

# Ubicación local del diccionario (caché)
CACHE_DIR = Path.home() / ".jelou"
CACHE_FILE = CACHE_DIR / "cmudict.txt"


class CMUDictionary:
    """
    Diccionario de pronunciación CMU con conversión a IPA.
    """
    
    def __init__(self):
        self._dict: Dict[str, str] = {}
        self._loaded = False
    
    def load(self, force_download: bool = False) -> None:
        """
        Carga el diccionario CMU.
        
        Args:
            force_download: Si True, descarga aunque exista caché
        """
        # Si ya está cargado en memoria, no hacer nada
        if self._loaded and not force_download:
            return
        
        # Usar caché si existe
        if CACHE_FILE.exists() and not force_download:
            self._load_from_file(CACHE_FILE)
        else:
            # Descargar diccionario
            self._download_and_cache()
            self._load_from_file(CACHE_FILE)
        
        self._loaded = True
    
    def _download_and_cache(self) -> None:
        """
        Descarga el diccionario CMU y lo guarda en caché.
        """
        print("📥 Descargando CMU Pronouncing Dictionary...")
        
        # Crear directorio de caché
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        
        try:
            # Descargar
            with urllib.request.urlopen(CMU_DICT_URL) as response:
                content = response.read().decode('utf-8')
            
            # Guardar en caché
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Diccionario descargado y guardado en: {CACHE_FILE}")
        
        except Exception as e:
            raise RuntimeError(f"Error descargando el diccionario CMU: {e}")
    
    def _load_from_file(self, filepath: Path) -> None:
        """
        Carga el diccionario desde un archivo.
        """
        print(f"📖 Cargando diccionario desde: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                result = parse_cmu_line(line)
                if result:
                    word, ipa = result
                    # Guardar primera pronunciación (ignorar variantes)
                    if word not in self._dict:
                        self._dict[word] = ipa
        
        print(f"✅ Diccionario cargado: {len(self._dict)} palabras")
    
    def lookup(self, word: str) -> Optional[str]:
        """
        Busca la pronunciación IPA de una palabra.
        
        Args:
            word: Palabra en inglés
            
        Returns:
            Pronunciación en IPA, o None si no se encuentra
        """
        # Asegurarse de que el diccionario esté cargado
        if not self._loaded:
            self.load()
        
        # Buscar (case-insensitive)
        return self._dict.get(word.lower())
    
    def __len__(self) -> int:
        """Retorna el número de palabras en el diccionario."""
        return len(self._dict)


# Instancia global singleton
_cmu_dict = CMUDictionary()


def get_dictionary() -> CMUDictionary:
    """
    Retorna la instancia singleton del diccionario CMU.
    """
    return _cmu_dict


def lookup_word(word: str) -> Optional[str]:
    """
    Función de conveniencia para buscar una palabra.
    
    Args:
        word: Palabra en inglés
        
    Returns:
        Pronunciación en IPA, o None si no se encuentra
    """
    return _cmu_dict.lookup(word)
