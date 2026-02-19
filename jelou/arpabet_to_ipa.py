"""
Conversor ARPABET a IPA
=======================

Este módulo convierte la notación ARPABET (usada por el CMU Pronouncing Dictionary)
al Alfabeto Fonético Internacional (IPA).

¿Qué es ARPABET?
----------------
ARPABET es un sistema de notación fonética basado en ASCII, diseñado para
representar la pronunciación del inglés americano usando solo caracteres ASCII.
Fue creado por ARPA (Advanced Research Projects Agency) en los años 70.

Ejemplo de conversión:
----------------------
ARPABET: "HH EH1 L OW0"  →  IPA: "hɛloʊ"  →  Español: "helou"

Autor: Nicolás Espejo
Proyecto: Jelou
Licencia: MIT
"""

from typing import Optional, Tuple

# =========================
# TABLA DE CONVERSIÓN ARPABET → IPA
# =========================

# Esta tabla mapea cada fonema ARPABET a su equivalente en IPA.
# Basada en la documentación oficial del CMU Pronouncing Dictionary.
# Referencia: http://www.speech.cs.cmu.edu/cgi-bin/cmudict

ARPABET_TO_IPA = {
    # ============
    # VOCALES
    # ============
    "AA": "ɑ",  # Vocal baja posterior: "father" /ˈfɑːðər/
    "AE": "æ",  # Vocal baja frontal: "cat" /kæt/
    "AH": "ʌ",  # Vocal media-baja central: "but" /bʌt/
    "AO": "ɔ",  # Vocal media-baja posterior: "dog" /dɔɡ/
    "AW": "aʊ",  # Diptongo: "now" /naʊ/
    "AY": "aɪ",  # Diptongo: "time" /taɪm/
    "EH": "ɛ",  # Vocal media-baja frontal: "bed" /bɛd/
    "ER": "ɝ",  # Vocal r-coloreada: "bird" /bɝd/
    "EY": "eɪ",  # Diptongo: "day" /deɪ/
    "IH": "ɪ",  # Vocal alta frontal corta: "sit" /sɪt/
    "IY": "i",  # Vocal alta frontal: "see" /siː/ (acento se agrega con stress=1)
    "OW": "oʊ",  # Diptongo: "go" /ɡoʊ/
    "OY": "ɔɪ",  # Diptongo: "boy" /bɔɪ/
    "UH": "ʊ",  # Vocal alta posterior corta: "book" /bʊk/
    "UW": "uː",  # Vocal alta posterior larga: "food" /fuːd/
    # ============
    # CONSONANTES
    # ============
    "B": "b",  # Oclusiva bilabial sonora: "book"
    "CH": "tʃ",  # Africada postalveolar sorda: "chair"
    "D": "d",  # Oclusiva alveolar sonora: "day"
    "DH": "ð",  # Fricativa dental sonora: "this"
    "F": "f",  # Fricativa labiodental sorda: "fun"
    "G": "g",  # Oclusiva velar sonora: "go"
    "HH": "h",  # Fricativa glotal sorda: "hello"
    "JH": "dʒ",  # Africada postalveolar sonora: "job"
    "K": "k",  # Oclusiva velar sorda: "cat"
    "L": "l",  # Aproximante lateral alveolar: "light"
    "M": "m",  # Nasal bilabial: "man"
    "N": "n",  # Nasal alveolar: "no"
    "NG": "ŋ",  # Nasal velar: "sing"
    "P": "p",  # Oclusiva bilabial sorda: "pen"
    "R": "r",  # Aproximante alveolar: "red"
    "S": "s",  # Fricativa alveolar sorda: "see"
    "SH": "ʃ",  # Fricativa postalveolar sorda: "she"
    "T": "t",  # Oclusiva alveolar sorda: "time"
    "TH": "θ",  # Fricativa dental sorda: "think"
    "V": "v",  # Fricativa labiodental sonora: "very"
    "W": "w",  # Aproximante labio-velar: "water"
    "Y": "j",  # Aproximante palatal: "yes"
    "Z": "z",  # Fricativa alveolar sonora: "zoo"
    "ZH": "ʒ",  # Fricativa postalveolar sonora: "vision"
}


# =========================
# FUNCIONES DE CONVERSIÓN
# =========================


def arpabet_to_ipa(arpabet_sequence: str) -> str:
    """
    Convierte una secuencia de fonemas ARPABET a notación IPA.

    Proceso:
    --------
    1. Divide la secuencia en fonemas individuales (separados por espacios)
    2. Limpia cada fonema eliminando los números de estrés (0, 1, 2)
    3. Identifica cuál vocal con stress primario (1) es la tónica principal
       — si hay más de una, se toma la última para palabras como "information"
    4. Busca cada fonema en la tabla de conversión
    5. Une todos los símbolos IPA resultantes

    Números de estrés en ARPABET:
    ------------------------------
    0 = Sin estrés (átona)
    1 = Estrés primario (tónica principal)
    2 = Estrés secundario (tónica secundaria) — se ignora en español

    En español solo existe una sílaba tónica por palabra, por lo que
    el stress secundario (2) se descarta y cuando hay múltiples stress
    primarios (1) se conserva únicamente el último.

    Args:
        arpabet_sequence (str): Fonemas ARPABET separados por espacios.
                               Puede incluir números de estrés.
                               Ejemplo: "HH AH0 L OW1"

    Returns:
        str: Cadena en notación IPA sin espacios.
             Ejemplo: "hʌloʊ"

    Examples:
        >>> arpabet_to_ipa("HH EH1 L OW0")
        'hɛloʊ'

        >>> arpabet_to_ipa("TH IH1 NG K")
        'θɪŋk'

        >>> arpabet_to_ipa("W ER1 L D")
        'wɝld'

    Note:
        Si un fonema no se encuentra en la tabla, se pasa tal cual
        en minúsculas (comportamiento de fallback para casos raros).
    """
    # Validar entrada vacía
    if not arpabet_sequence:
        return ""

    # Paso 1: Normalizar a mayúsculas y separar por espacios
    phonemes = arpabet_sequence.upper().split()

    # Vocales que reciben marcador de acento
    STRESSED_VOWELS = {
        "AA", "AE", "AH", "AO", "AW", "AY",
        "EH", "ER", "EY", "IH", "IY", "OW",
        "OY", "UH", "UW"
    }

    # Paso 2: Identificar el índice de la vocal tónica principal.
    # Si hay más de un stress primario (1), se toma el último.
    # Esto resuelve palabras como "information" (IH2 N F AO1 R M EY1 SH AH0 N)
    # donde CMU marca dos vocales con stress 1 — la tónica real es la última.
    primary_stress_index = None
    for i, phoneme in enumerate(phonemes):
        if phoneme and phoneme[-1] == "1":
            clean = phoneme.rstrip("012")
            if clean in STRESSED_VOWELS:
                primary_stress_index = i

    # Paso 3: Procesar cada fonema
    ipa_result = []
    for i, phoneme in enumerate(phonemes):
        # Extraer número de estrés si existe
        stress = ""
        if phoneme and phoneme[-1] in "012":
            stress = phoneme[-1]

        # Limpiar el fonema
        clean_phoneme = phoneme.rstrip("012")

        # Paso 4: Buscar en la tabla de conversión
        if clean_phoneme in ARPABET_TO_IPA:
            ipa_symbol = ARPABET_TO_IPA[clean_phoneme]
            # Agregar marcador de acento solo a la vocal tónica principal
            if i == primary_stress_index:
                ipa_result.append("~~STRESS~~" + ipa_symbol)
            else:
                ipa_result.append(ipa_symbol)
        else:
            ipa_result.append(clean_phoneme.lower())

    # Paso 5: Unir todos los símbolos IPA en una sola cadena
    return "".join(ipa_result)


def arpabet_to_ipa_clean(arpabet_sequence: str) -> str:
    """Devuelve IPA puro sin marcadores de acento. Para mostrar al usuario."""
    result = arpabet_to_ipa(arpabet_sequence)
    result = result.replace("~~STRESS~~", "")
    return result


def parse_cmu_line(line: str) -> Optional[Tuple[str, str]]:
    """
    Parsea una línea del CMU Pronouncing Dictionary y retorna palabra + IPA.

    Formato del CMU Dictionary:
    ---------------------------
    Cada línea tiene el formato:
    PALABRA  FONEMA1 FONEMA2 FONEMA3 ...

    Ejemplo:
    HELLO  HH AH0 L OW1
    WORLD  W ER1 L D

    Variantes de pronunciación:
    ---------------------------
    Algunas palabras tienen múltiples pronunciaciones, indicadas con (N):
    HELLO(1)  HH EH1 L OW0
    HELLO(2)  HH AH0 L OW1

    Este parser limpia los números de variante.

    Args:
        line (str): Línea del archivo CMU Dictionary

    Returns:
        Optional[Tuple[str, str]]: Tupla (palabra, ipa) si la línea es válida,
                                   None si la línea es un comentario o está vacía.

    Examples:
        >>> parse_cmu_line("HELLO  HH AH0 L OW1")
        ('hello', 'hʌloʊ')

        >>> parse_cmu_line("WORLD  W ER1 L D")
        ('world', 'wɝld')

        >>> parse_cmu_line(";;;Comment line")
        None

        >>> parse_cmu_line("HELLO(2)  HH EH1 L OW0")
        ('hello', 'hɛloʊ')

    Note:
        - Las palabras se convierten a minúsculas
        - Los comentarios (líneas que empiezan con ;;;) se ignoran
        - Las variantes (WORD(1), WORD(2)) se limpian de su número
    """
    # Paso 1: Limpiar espacios en blanco
    line = line.strip()

    # Paso 2: Ignorar líneas vacías o comentarios
    if not line or line.startswith(";;;"):
        return None

    # Paso 3: Separar la palabra de los fonemas
    parts = line.split(maxsplit=1)

    if len(parts) < 2:
        return None

    word, arpabet = parts

    # Paso 4: Limpiar la palabra
    word = word.split("(")[0].lower()

    # Paso 5: Convertir ARPABET a IPA limpio (sin marcadores)
    ipa = arpabet_to_ipa_clean(arpabet)

    # Paso 6: Retornar tupla (palabra, ipa)
    return (word, ipa)