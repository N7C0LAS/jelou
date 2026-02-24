"""
API pública de Jelou.
Punto de entrada principal para usar Jelou como librería.

Flujo: palabra → CMU Dictionary → ARPABET → IPA → español

Autor: Nicolás Espejo
Proyecto: Jelou
Licencia: MIT
"""

from typing import List, Dict

from jelou.cmu_dictionary import lookup_word, lookup_word_with_stress
from jelou.phonetic_engine import ipa_to_spanish


def translate_word(word: str) -> Dict:
    """
    Traduce una palabra inglesa a fonética en español.

    Retorna dict con: word, ipa, spanish, found.
    found=False si la palabra no existe en el CMU Dictionary.

    >>> translate_word("hello")
    {'word': 'hello', 'ipa': 'hʌloʊ', 'spanish': 'jalóu', 'found': True}
    """
    result = {"word": word, "ipa": None, "spanish": None, "found": False}

    ipa_display = lookup_word(word)
    ipa = lookup_word_with_stress(word)

    if ipa:
        result["ipa"] = ipa_display
        result["spanish"] = ipa_to_spanish(ipa)
        result["found"] = True

    return result


def translate_ipa(ipa: str) -> str:
    """
    Convierte IPA directamente a fonética en español sin usar el diccionario.

    Manejo de stress:
    - Si tiene ˈ estándar → convierte a ~~STRESS~~
    - Si tiene vocal larga (iː/uː) → inserta stress ahí
    - Sin ninguno → procesa sin acento

    >>> translate_ipa("θɪŋk")
    'zink'
    >>> translate_ipa("ʃiː")
    'shí'
    """
    if "ˈ" in ipa:
        return ipa_to_spanish(ipa.replace("ˈ", "~~STRESS~~"))

    for lv in ["iː", "uː"]:
        if lv in ipa:
            return ipa_to_spanish(ipa.replace(lv, "~~STRESS~~" + lv, 1))

    return ipa_to_spanish(ipa)


def batch_translate(words: List[str]) -> List[Dict]:
    """
    Traduce una lista de palabras. El diccionario se carga una sola vez.

    >>> batch_translate(["hello", "world"])
    [{'word': 'hello', ...}, {'word': 'world', ...}]
    """
    return [translate_word(word) for word in words]