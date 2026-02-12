"""
API principal de Jelou.

Este módulo integra todos los componentes:
1. CMU Dictionary (palabra → IPA)
2. Motor fonético (IPA → español)
"""

from jelou.cmu_dictionary import lookup_word
from jelou.phonetic_engine import ipa_to_spanish


def translate_word(word: str) -> dict:
    """
    Traduce una palabra en inglés a su representación fonética en español.
    
    Este es el punto de entrada principal de la API de Jelou.
    
    Args:
        word: Palabra en inglés (ej: "hello")
        
    Returns:
        Diccionario con:
        - word: palabra original
        - ipa: representación IPA (si se encontró)
        - spanish: representación fonética en español
        - found: True si la palabra se encontró en el diccionario
        
    Examples:
        >>> translate_word("hello")
        {
            'word': 'hello',
            'ipa': 'hɛloʊ',
            'spanish': 'helou',
            'found': True
        }
    """
    result = {
        'word': word,
        'ipa': None,
        'spanish': None,
        'found': False
    }
    
    # Buscar en diccionario CMU
    ipa = lookup_word(word)
    
    if ipa:
        result['ipa'] = ipa
        result['spanish'] = ipa_to_spanish(ipa)
        result['found'] = True
    
    return result


def translate_ipa(ipa: str) -> str:
    """
    Convierte directamente IPA a representación en español.
    
    Args:
        ipa: String en notación IPA
        
    Returns:
        Representación fonética en español
        
    Examples:
        >>> translate_ipa("θɪŋk")
        'zink'
    """
    return ipa_to_spanish(ipa)


def batch_translate(words: list[str]) -> list[dict]:
    """
    Traduce múltiples palabras de una vez.
    
    Args:
        words: Lista de palabras en inglés
        
    Returns:
        Lista de diccionarios con resultados
    """
    return [translate_word(word) for word in words]
