"""
Motor de Adaptación Fonética - IPA a Español
=============================================

Este módulo convierte símbolos del Alfabeto Fonético Internacional (IPA)
a una representación fonética legible usando el alfabeto español.

Propósito:
----------
Facilitar la pronunciación del inglés para hispanohablantes sin necesidad
de aprender IPA. El sistema prioriza precisión fonética y claridad.

Principios de diseño:
---------------------
1. Un símbolo representa un solo sonido
2. Conversión determinista (misma entrada = misma salida)
3. Sistema consistente y predecible
4. Resultado pronunciable sin contexto adicional
5. Precisión fonética sobre simplicidad

Versión: 0.2.5
Autor: Nicolás Espejo
Proyecto: Jelou
Licencia: MIT
"""

import re

# =========================
# REGLAS FONÉTICAS
# =========================

COMPOUND_RULES = {
    "aɪər": "air",
    "aʊər": "aur",
    "dʒ": "y",
    "tʃ": "ch",
    "θ": "z",
    "ð": "d",
    "ʃ": "sh",
    "ʒ": "sh",
    "eər": "er",
}

# iː → i y uː → u por defecto (átonas).
# El acento se aplica únicamente via STRESS_MAP cuando hay ~~STRESS~~
# o via translate_ipa() que inserta ~~STRESS~~ automáticamente.
VOWEL_RULES = {
    "iː": "i",   # Átona por defecto — acento solo via STRESS_MAP
    "ɪ": "i",
    "ɛ": "e",
    "æ": "a",
    "ɑ": "a",
    "ʌ": "a",
    "e": "e",
    "ə": "a",
    "ɔ": "o",
    "ʊ": "u",
    "aʊ": "au",
    "oʊ": "ou",
    "uː": "u",   # Átona por defecto — acento solo via STRESS_MAP
    "ɝ": "er",
    "ɚ": "er",
}

CONSONANT_RULES = {
    "h": "j",
    "ŋ": "ng",
    "k": "k",
    "s": "s",
    "z": "z",
    "w": "w",
    "r": "r",
    "l": "l",
    "n": "n",
    "m": "m",
    "f": "f",
    "v": "v",
    "b": "b",
    "p": "p",
    "t": "t",
    "d": "d",
    "g": "g",
}

# Vocales IPA — usadas para detectar contexto consonántico
_VOWELS = "aeiouɪʊʌɛæɑɔəɝɚ"


def ipa_to_spanish(ipa: str) -> str:
    """
    Convierte una cadena IPA a representación fonética en español.

    Proceso:
    --------
    1. Procesa marcadores ~~STRESS~~ y protege vocales acentuadas resultantes
    2. Elimina marcas de acento estándar del IPA (ˈ ˌ)
    3. Elimina semivocal j redundante después de dʒ
    4. Protege j temporalmente
    5. Aplica reglas compuestas
    6. Protege sh, ch creados por reglas compuestas
    7. Aplica reglas de vocales
    8. Aplica reglas de consonantes
    9. Restaura marcadores temporales
    10. Aplica correcciones contextuales
    11. Aplica correcciones fonéticas finales

    Args:
        ipa (str): Cadena en notación IPA con marcadores ~~STRESS~~

    Returns:
        str: Representación fonética en español con acento gráfico

    Examples:
        >>> ipa_to_spanish("θɪŋk")
        'zink'
        >>> ipa_to_spanish("hɛloʊ")
        'jelou'
        >>> ipa_to_spanish("ʃiː")
        'shí'
        >>> ipa_to_spanish("v~~STRESS~~ɛdʒtʌbʌl")
        'véchtabal'

    Cambios en v0.2.5:
        - dʒ seguido de consonante → ch (vegetable: véytabal → véchtabal)
    """
    stressed_ipa = ipa

    # Paso 1: Procesar marcadores ~~STRESS~~
    STRESS_MAP = {
        "aʊ": "áu", "aɪ": "ái", "eɪ": "éi", "oʊ": "óu", "ɔɪ": "ói",
        "iː": "í",  "uː": "ú",
        "ɑ": "á",   "æ": "á",   "ʌ": "á",   "ɔ": "ó",
        "ɛ": "é",   "ɝ": "ér",  "ɪ": "í",   "i": "í",   "ʊ": "ú",
    }
    for ipa_v, esp_v in sorted(STRESS_MAP.items(), key=lambda x: -len(x[0])):
        stressed_ipa = stressed_ipa.replace("~~STRESS~~" + ipa_v, "~~A~~" + esp_v)
    stressed_ipa = stressed_ipa.replace("~~STRESS~~", "")

    result = stressed_ipa.lower()
    result = result.replace("ˈ", "").replace("ˌ", "")

    # Paso 1b: Proteger vocales acentuadas ya procesadas por STRESS_MAP
    result = result.replace("~~a~~í", "~~~TEMP_I_STRESS~~~")
    result = result.replace("~~a~~ú", "~~~TEMP_U_STRESS~~~")
    result = result.replace("~~a~~", "~~~TEMP_STRESS~~~")

    # Paso 2: Eliminar semivocal j redundante después de dʒ
    result = result.replace("dʒj", "dʒ")

    # Paso 3: Convertir dʒ seguido de consonante a ch
    # "vegetable" dʒt → cht → véchtabal (no véytabal)
    # Debe hacerse ANTES de proteger j y aplicar COMPOUND_RULES
    result = re.sub(r'dʒ([^' + _VOWELS + r'])', r'ch\1', result)

    # Paso 4: Proteger /j/ IPA temporalmente
    result = result.replace("j", "~~~TEMP_J~~~")

    # Paso 5: Aplicar reglas compuestas
    for ipa_sound, adapted in COMPOUND_RULES.items():
        result = result.replace(ipa_sound, adapted)

    # Paso 6: Proteger sh, ch creados por reglas compuestas
    result = result.replace("sh", "~~~TEMP_SH~~~")
    result = result.replace("ch", "~~~TEMP_CH~~~")

    # Paso 7: Aplicar reglas de vocales
    for ipa_sound, adapted in VOWEL_RULES.items():
        result = result.replace(ipa_sound, adapted)

    # Paso 8: Aplicar reglas de consonantes
    for ipa_sound, adapted in CONSONANT_RULES.items():
        result = result.replace(ipa_sound, adapted)

    # Paso 9: Restaurar todos los marcadores temporales
    result = result.replace("~~~TEMP_I_STRESS~~~", "í")
    result = result.replace("~~~TEMP_U_STRESS~~~", "ú")
    result = result.replace("~~~TEMP_STRESS~~~", "")
    result = result.replace("~~~TEMP_J~~~", "i")
    result = result.replace("~~~TEMP_SH~~~", "sh")
    result = result.replace("~~~TEMP_CH~~~", "ch")

    # Paso 10: Correcciones contextuales
    for vocal in ["a", "e", "i", "o", "u", "á", "é", "í", "ó", "ú"]:
        if result.endswith(f"{vocal}y"):
            result = result[:-1] + "sh"

    result = result.replace("pj", "pi")

    # Paso 11: Correcciones fonéticas finales
    result = result.replace("ngk", "nk")
    result = result.replace("ngg", "ng")
    result = result.replace("íi", "íe")
    result = result.replace("ii", "ie")

   
    return result