"""
Integración con CMU Pronouncing Dictionary
===========================================

Este módulo gestiona la descarga, caché y búsqueda de pronunciaciones
en el CMU Pronouncing Dictionary, el diccionario de pronunciación
de código abierto más grande para inglés americano.

¿Qué es el CMU Pronouncing Dictionary?
---------------------------------------
Es un diccionario desarrollado por Carnegie Mellon University que contiene
más de 126,000 palabras con sus pronunciaciones en formato ARPABET.

Características clave:
----------------------
- Descarga automática en primera ejecución
- Sistema de caché local para uso offline
- Búsqueda rápida por palabra
- Conversión automática ARPABET → IPA → Español

Autor: Nicolás Espejo
Proyecto: Jelou
Licencia: MIT
"""

import urllib.request
from pathlib import Path
from typing import Dict, Optional

from jelou.arpabet_to_ipa import arpabet_to_ipa, arpabet_to_ipa_clean

# =========================
# CONFIGURACIÓN
# =========================

# URL del diccionario CMU en GitHub
# Este es el repositorio oficial mantenido por CMU Sphinx
CMU_DICT_URL = "https://raw.githubusercontent.com/cmusphinx/cmudict/master/cmudict.dict"

# Ubicación del caché local
# Se guarda en el directorio home del usuario para persistencia
CACHE_DIR = Path.home() / ".jelou"
CACHE_FILE = CACHE_DIR / "cmudict.txt"


# =========================
# CLASE PRINCIPAL
# =========================


class CMUDictionary:
    """
    Gestor del diccionario de pronunciación CMU.

    Esta clase maneja:
    - Descarga del diccionario desde internet
    - Almacenamiento en caché local
    - Carga del diccionario en memoria
    - Búsqueda de pronunciaciones

    Patrón de diseño:
    -----------------
    Singleton: Solo existe una instancia del diccionario en memoria
    para evitar cargar 126,000 palabras múltiples veces.

    Attributes:
        _dict (Dict[str, str]): Diccionario palabra → IPA con marcadores de stress
        _loaded (bool): Indica si el diccionario ya está cargado en memoria
    """

    def __init__(self):
        """
        Inicializa el gestor del diccionario.

        El diccionario NO se carga automáticamente en __init__ para
        evitar tiempos de inicio lentos. Se carga bajo demanda en
        la primera búsqueda (lazy loading).
        """
        self._dict: Dict[str, str] = {}
        self._loaded = False

    def load(self, force_download: bool = False) -> None:
        """
        Carga el diccionario CMU en memoria.

        Estrategia de carga:
        --------------------
        1. Si ya está cargado en memoria → no hacer nada (optimización)
        2. Si existe caché local → cargar desde archivo
        3. Si no existe caché → descargar de internet y guardar

        Args:
            force_download (bool): Si True, descarga aunque exista caché.
                                  Útil para actualizar a la última versión.
                                  Default: False

        Raises:
            RuntimeError: Si la descarga falla (sin conexión, URL inválida, etc.)

        Examples:
            >>> dictionary = CMUDictionary()
            >>> dictionary.load()
            >>> dictionary.load(force_download=True)
        """
        if self._loaded and not force_download:
            return

        if CACHE_FILE.exists() and not force_download:
            self._load_from_file(CACHE_FILE)
        else:
            self._download_and_cache()
            self._load_from_file(CACHE_FILE)

        self._loaded = True

    def _download_and_cache(self) -> None:
        """
        Descarga el diccionario CMU desde internet y lo guarda en caché.

        Proceso:
        --------
        1. Crear directorio de caché si no existe
        2. Descargar archivo desde GitHub
        3. Decodificar contenido (UTF-8)
        4. Guardar en archivo local

        Raises:
            RuntimeError: Si la descarga falla por cualquier motivo

        Note:
            Este método solo se ejecuta una vez por instalación,
            o cuando se fuerza la recarga con force_download=True.
        """
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
        """
        Calcula un puntaje para elegir la mejor variante de pronunciación.

        Criterios (menor puntaje = mejor variante):
        1. Cantidad de HH — menos HH es mejor (H muda entre vocales)
        2. Cantidad de AH0 — menos AH0 es mejor (schwa reducido)

        Esta estrategia resuelve simultáneamente:
        - "vehicle": variante (2) elimina HH muda → víekal ✓
        - "education": variante (2) tiene UW en lugar de AH → eyúkéishan ✓
        - "information": variante (2) tiene AO en lugar de ER → informéishan ✓

        Args:
            arpabet (str): Secuencia de fonemas ARPABET

        Returns:
            tuple: (hh_count, ah0_count) — menor es mejor
        """
        tokens = arpabet.upper().split()
        hh_count = tokens.count("HH")
        ah0_count = tokens.count("AH0")
        return (hh_count, ah0_count)

    def _load_from_file(self, filepath: Path) -> None:
        """
        Carga el diccionario desde un archivo local.

        Proceso:
        --------
        1. Abrir archivo
        2. Leer línea por línea
        3. Parsear cada línea (palabra + ARPABET → IPA con stress)
        4. Almacenar en diccionario interno

        Gestión de variantes:
        ---------------------
        Se usa una estrategia de puntaje para elegir la mejor variante:
        - Se evalúan HH (H muda) y AH0 (schwa reducido)
        - La variante con menor puntaje en ambos criterios gana
        - Esto preserva pronunciaciones más naturales y precisas

        Almacenamiento de stress:
        -------------------------
        El IPA se guarda CON los marcadores ~~STRESS~~ para que el motor
        fonético pueda aplicar acentos correctamente al español.
        El método lookup() los elimina al devolver resultados al usuario.
        El método lookup_with_stress() los conserva para uso interno.

        Args:
            filepath (Path): Ruta al archivo del diccionario

        Note:
            Este método procesa ~126,000 líneas. Toma ~2-3 segundos.
            El resultado se mantiene en memoria para búsquedas rápidas.
        """
        print(f"📖 Cargando diccionario desde: {filepath}")

        # Almacena el ARPABET crudo de la variante actual para comparar scores
        _arpabet_cache: Dict[str, str] = {}

        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                # Ignorar líneas vacías o comentarios
                if not line or line.startswith(";;;"):
                    continue

                # Separar palabra de fonemas
                parts = line.split(maxsplit=1)
                if len(parts) < 2:
                    continue

                word_raw, arpabet = parts

                # Limpiar variantes: "HELLO(2)" → "hello"
                word = word_raw.split("(")[0].lower()
                is_variant = "(" in word_raw

                if not is_variant:
                    # Primera pronunciación: guardar siempre
                    self._dict[word] = arpabet_to_ipa(arpabet)
                    _arpabet_cache[word] = arpabet
                else:
                    # Variante posterior: reemplazar solo si tiene mejor puntaje
                    current_arpabet = _arpabet_cache.get(word, "")
                    current_score = self._score_variant(current_arpabet)
                    new_score = self._score_variant(arpabet)

                    if new_score < current_score:
                        self._dict[word] = arpabet_to_ipa(arpabet)
                        _arpabet_cache[word] = arpabet

        print(f"✅ Diccionario cargado: {len(self._dict)} palabras")

    def lookup_with_stress(self, word: str) -> Optional[str]:
        """Devuelve IPA con marcadores de acento. Para uso interno del motor fonético."""
        self.load()
        return self._dict.get(word.lower())

    def lookup(self, word: str) -> Optional[str]:
        """
        Busca la pronunciación IPA de una palabra.

        Proceso:
        --------
        1. Asegurar que el diccionario esté cargado (lazy loading)
        2. Normalizar palabra a minúsculas
        3. Buscar en diccionario interno
        4. Retornar IPA limpio (sin marcadores de stress) o None

        Args:
            word (str): Palabra en inglés a buscar (case-insensitive)

        Returns:
            Optional[str]: Pronunciación en IPA si se encuentra,
                          None si la palabra no existe en el diccionario

        Examples:
            >>> dictionary = CMUDictionary()
            >>> dictionary.lookup("hello")
            'hʌloʊ'

            >>> dictionary.lookup("HELLO")
            'hʌloʊ'

            >>> dictionary.lookup("xyzabc")
            None

        Note:
            La primera llamada a lookup() puede ser lenta (~2-3 segundos)
            porque carga el diccionario. Las siguientes son instantáneas.
        """
        if not self._loaded:
            self.load()

        result = self._dict.get(word.lower())
        if result:
            return result.replace("~~STRESS~~", "")
        return None

    def __len__(self) -> int:
        """
        Retorna el número de palabras en el diccionario.

        Returns:
            int: Cantidad de palabras cargadas

        Example:
            >>> dictionary = CMUDictionary()
            >>> dictionary.load()
            >>> len(dictionary)
            126052
        """
        return len(self._dict)


# =========================
# API SINGLETON
# =========================

# Instancia global única del diccionario
# Evita cargar 126,000 palabras múltiples veces en memoria
_cmu_dict = CMUDictionary()


def get_dictionary() -> CMUDictionary:
    """
    Retorna la instancia singleton del diccionario CMU.

    Returns:
        CMUDictionary: La instancia global del diccionario

    Example:
        >>> dict1 = get_dictionary()
        >>> dict2 = get_dictionary()
        >>> dict1 is dict2
        True
    """
    return _cmu_dict


def lookup_word(word: str) -> Optional[str]:
    """
    Función de conveniencia para buscar una palabra.

    Args:
        word (str): Palabra en inglés a buscar

    Returns:
        Optional[str]: Pronunciación en IPA o None

    Examples:
        >>> lookup_word("hello")
        'hʌloʊ'

        >>> lookup_word("world")
        'wɝld'

        >>> lookup_word("notaword")
        None
    """
    return _cmu_dict.lookup(word)


def lookup_word_with_stress(word: str) -> Optional[str]:
    """Devuelve IPA con marcadores de acento. Para uso interno del motor fonético."""
    global _cmu_dict
    if _cmu_dict is None:
        _cmu_dict = get_dictionary()
    return _cmu_dict.lookup_with_stress(word)