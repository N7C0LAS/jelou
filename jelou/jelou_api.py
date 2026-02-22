"""
API Pública de Jelou
====================

Este módulo es el punto de entrada principal para usar Jelou como librería.
Integra todos los componentes del sistema en una API simple y coherente.

Flujo de datos completo:
------------------------
1. Usuario proporciona palabra en inglés
2. CMU Dictionary busca la palabra → retorna ARPABET
3. ARPABET se convierte a IPA
4. IPA se convierte a representación en español
5. Se retorna resultado al usuario

Funciones principales:
----------------------
- translate_word(word): Traducción completa palabra → español
- translate_ipa(ipa): Conversión directa IPA → español
- batch_translate(words): Procesar múltiples palabras

Uso como librería:
------------------
```python
from jelou import translate_word

result = translate_word("hello")
print(result['spanish'])  # 'halou'
```

Autor: Nicolás Espejo
Proyecto: Jelou
Licencia: MIT
"""

from typing import List, Dict

from jelou.cmu_dictionary import lookup_word, lookup_word_with_stress
from jelou.phonetic_engine import ipa_to_spanish

# =========================
# FUNCIONES PRINCIPALES
# =========================


def translate_word(word: str) -> Dict:
    """
    Traduce una palabra en inglés a representación fonética en español.

    Este es el punto de entrada principal de Jelou. Realiza la conversión
    completa: Palabra → ARPABET → IPA → Español.

    Flujo interno:
    --------------
    1. Buscar palabra en CMU Dictionary
    2. Si se encuentra: obtener IPA
    3. Convertir IPA a español usando phonetic_engine
    4. Retornar resultado estructurado

    Args:
        word (str): Palabra en inglés (case-insensitive)
                   Ejemplos: "hello", "world", "computer"

    Returns:
        Dict: Diccionario con estructura:
            {
                'word': str,      # Palabra original
                'ipa': str|None,  # Pronunciación IPA (None si no encontrada)
                'spanish': str|None,  # Pronunciación en español (None si no encontrada)
                'found': bool     # True si la palabra existe en el diccionario
            }

    Examples:
        >>> translate_word("hello")
        {
            'word': 'hello',
            'ipa': 'hʌloʊ',
            'spanish': 'halou',
            'found': True
        }

        >>> translate_word("think")
        {
            'word': 'think',
            'ipa': 'θɪŋk',
            'spanish': 'zink',
            'found': True
        }

        >>> translate_word("notarealword")
        {
            'word': 'notarealword',
            'ipa': None,
            'spanish': None,
            'found': False
        }

    Note:
        La primera llamada puede ser lenta (~2-3 segundos) porque carga
        el diccionario CMU. Las llamadas siguientes son instantáneas.

        Si la palabra no se encuentra, considerar usar translate_ipa()
        con la pronunciación IPA manual.
    """
    # Estructura de respuesta base
    result = {"word": word, "ipa": None, "spanish": None, "found": False}

    # Paso 1: Buscar palabra en diccionario CMU
    # Retorna IPA o None si no existe
    ipa_display = lookup_word(word)  # IPA limpio para mostrar al usuario
    ipa = lookup_word_with_stress(word)  # IPA con marcadores para el motor fonético

    # Paso 2: Si se encontró, convertir a español
    if ipa:
        result["ipa"] = ipa_display
        result["spanish"] = ipa_to_spanish(ipa)
        result["found"] = True

    return result


def translate_ipa(ipa: str) -> str:
    """
    Convierte directamente notación IPA a representación en español.

    Este método es útil cuando:
    - La palabra no está en el diccionario
    - El usuario conoce la notación IPA
    - Se quiere experimentar con pronunciaciones personalizadas

    No requiere diccionario CMU, es una conversión directa.

    Manejo de stress:
    -----------------
    Si el IPA incluye marcadores estándar (ˈ), los convierte a ~~STRESS~~
    internamente para que el motor fonético aplique acentos correctamente.
    Si no hay marcadores, aplica acento a la primera vocal larga (iː, uː)
    o a la primera vocal de la palabra.

    Args:
        ipa (str): Cadena en notación IPA
                  Puede incluir marcas de acento (ˈ, ˌ)
                  Ejemplos: "θɪŋk", "ʃiː", "wɝld", "hɛˈloʊ"

    Returns:
        str: Representación fonética en español

    Examples:
        >>> translate_ipa("θɪŋk")
        'zink'
        >>> translate_ipa("ʃiː")
        'shí'
        >>> translate_ipa("fuːd")
        'fúd'
        >>> translate_ipa("hɛˈloʊ")
        'jelóu'
    """
    # Convertir marcadores estándar IPA (ˈ) a ~~STRESS~~
    # ˈ precede la sílaba tónica en IPA estándar
    if "ˈ" in ipa:
        # Insertar ~~STRESS~~ después de ˈ y eliminar ˈ
        processed = ipa.replace("ˈ", "~~STRESS~~")
        return ipa_to_spanish(processed)

    # Sin marcadores: insertar stress en vocal larga si existe
    # Orden de prioridad: iː > uː > primera vocal
    _LONG_VOWELS = ["iː", "uː"]
    for lv in _LONG_VOWELS:
        if lv in ipa:
            stressed = ipa.replace(lv, "~~STRESS~~" + lv, 1)
            return ipa_to_spanish(stressed)

    # Sin vocal larga: procesar directamente
    return ipa_to_spanish(ipa)


def batch_translate(words: List[str]) -> List[Dict]:
    """
    Traduce múltiples palabras de una vez.

    Útil para:
    - Procesar listas de vocabulario
    - Generar flashcards
    - Análisis de textos
    - APIs que procesan múltiples palabras

    Args:
        words (List[str]): Lista de palabras en inglés
                          Ejemplo: ["hello", "world", "computer"]

    Returns:
        List[Dict]: Lista de diccionarios con resultados.
                    Cada elemento tiene la misma estructura que translate_word()

    Examples:
        >>> batch_translate(["hello", "world"])
        [
            {'word': 'hello', 'ipa': 'hʌloʊ', 'spanish': 'halou', 'found': True},
            {'word': 'world', 'ipa': 'wɝld', 'spanish': 'werld', 'found': True}
        ]

        >>> batch_translate(["think", "notaword", "computer"])
        [
            {'word': 'think', 'ipa': 'θɪŋk', 'spanish': 'zink', 'found': True},
            {'word': 'notaword', 'ipa': None, 'spanish': None, 'found': False},
            {'word': 'computer', 'ipa': 'kʌmpjuːtɝ', 'spanish': 'kampjúter', 'found': True}  # noqa: E501
        ]

    Note:
        El diccionario CMU se carga una sola vez para todas las palabras,
        por lo que procesar 100 palabras es casi tan rápido como procesar 1.

    Performance:
        - Primera palabra: ~2-3 segundos (carga diccionario)
        - Palabras adicionales: ~0.001 segundos cada una
    """
    return [translate_word(word) for word in words]
