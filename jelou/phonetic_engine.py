"""
Motor fonético IPA → español para hispanohablantes.
Convierte IPA a una representación pronunciable usando el alfabeto español.

Autor: Nicolás Espejo
Proyecto: Jelou
Licencia: MIT
"""

import re

# θ y ð se protegen con TEMP_Z para que CONSONANT_RULES no los convierta a s
COMPOUND_RULES = {
    "aɪər": "air",
    "aʊər": "aur",
    "dʒ": "dch",
    "tʃ": "ch",
    "θ": "~~~TEMP_Z~~~",
    "ð": "~~~TEMP_Z~~~",
    "ʃ": "sh",
    "ʒ": "sh",
    "eər": "er",
}

# iː/uː → i/u por defecto (átonas). El acento se aplica solo via STRESS_MAP.
VOWEL_RULES = {
    "iː": "i",
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
    "uː": "u",
    "ɝ": "er",
    "ɚ": "er",
}

CONSONANT_RULES = {
    "h": "j",
    "ŋ": "ng",
    "k": "k",
    "s": "s",
    "z": "s",  # z nativa inglesa → s (zone→sóun). Solo θ/ð generan z via TEMP_Z.
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

_VOWELS = "aeiouɪʊʌɛæɑɔəɝɚ"


def ipa_to_spanish(ipa: str) -> str:
    """
    Convierte IPA con marcadores ~~STRESS~~ a fonética en español con acento gráfico.

    El proceso aplica reglas en orden estricto para evitar colisiones:
    1. Resuelve ~~STRESS~~ → vocal acentuada y protege el resultado
    2. Elimina marcas IPA (ˈ ˌ) y semivocal j redundante tras dʒ
    3. Convierte dʒ+consonante → ch (vegetable→véchtabal)
    4. Protege j IPA para que no colisione con COMPOUND_RULES
    5. Aplica COMPOUND_RULES (θ/ð→TEMP_Z, dʒ→y, tʃ→ch, ʃ→sh...)
    6. Protege sh/ch para que CONSONANT_RULES no los rompa
    7. Aplica VOWEL_RULES
    8. Aplica CONSONANT_RULES
    9. Restaura todos los marcadores temporales
    10. Correcciones contextuales (vocal+y final → sh, pj → pi)
    11. Correcciones fonéticas (ngk→nk, ngg→ng, íi→íe, ii→ie)

    >>> ipa_to_spanish("θɪŋk")
    'zink'
    >>> ipa_to_spanish("hɛloʊ")
    'jelou'
    """
    stressed_ipa = ipa

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

    result = result.replace("~~a~~í", "~~~TEMP_I_STRESS~~~")
    result = result.replace("~~a~~ú", "~~~TEMP_U_STRESS~~~")
    result = result.replace("~~a~~", "~~~TEMP_STRESS~~~")

    result = result.replace("dʒj", "dʒ")
    result = re.sub(r'dʒ([^' + _VOWELS + r'~])', r'ch\1', result)
    result = result.replace("j", "~~~TEMP_J~~~")

    for ipa_sound, adapted in COMPOUND_RULES.items():
        result = result.replace(ipa_sound, adapted)

    result = result.replace("sh", "~~~TEMP_SH~~~")
    result = result.replace("ch", "~~~TEMP_CH~~~")

    for ipa_sound, adapted in VOWEL_RULES.items():
        result = result.replace(ipa_sound, adapted)

    for ipa_sound, adapted in CONSONANT_RULES.items():
        result = result.replace(ipa_sound, adapted)

    result = result.replace("~~~TEMP_I_STRESS~~~", "í")
    result = result.replace("~~~TEMP_U_STRESS~~~", "ú")
    result = result.replace("~~~TEMP_STRESS~~~", "")
    result = result.replace("~~~TEMP_J~~~", "i")
    result = result.replace("~~~TEMP_SH~~~", "sh")
    result = result.replace("~~~TEMP_CH~~~", "ch")
    result = result.replace("~~~TEMP_Z~~~", "z")

    for vocal in ["a", "e", "i", "o", "u", "á", "é", "í", "ó", "ú"]:
        if result.endswith(f"{vocal}y"):
            result = result[:-1] + "sh"

    result = result.replace("pj", "pi")
    result = result.replace("ngk", "nk")
    result = result.replace("ngg", "ng")
    result = result.replace("íi", "íe")
    result = result.replace("ii", "ie")

    return result