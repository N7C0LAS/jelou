"""
Motor de adaptación fonética Inglés (IPA) → Español
"""

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

VOWEL_RULES = {
    "iː": "í",
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
    "uː": "ú",
    "ɝ": "er",
    "ɚ": "er",

}

CONSONANT_RULES = {
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

# =========================
# MOTOR
# =========================



def ipa_to_spanish(ipa: str) -> str:
    """
    Convierte una cadena IPA en una representación fonética
    basada en caracteres familiares para hispanohablantes.
    """
    result = ipa.lower()

    # Eliminar marcas de acento del IPA
    result = result.replace("ˈ", "").replace("ˌ", "")

    # 1. Reglas compuestas (orden importa)
    for ipa_sound, adapted in COMPOUND_RULES.items():
        result = result.replace(ipa_sound, adapted)

    # 2. Vocales
    for ipa_sound, adapted in VOWEL_RULES.items():
        result = result.replace(ipa_sound, adapted)

    # 3. Consonantes
    for ipa_sound, adapted in CONSONANT_RULES.items():
        result = result.replace(ipa_sound, adapted)

    # 4. Correcciones fonéticas finales
    result = result.replace("ngk", "nk")
    result = result.replace("ngg", "ng")


    return result
