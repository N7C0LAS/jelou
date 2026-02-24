"""
Conversor ARPABET → IPA.
ARPABET es el sistema ASCII del CMU Dictionary para representar fonética inglesa.
Ejemplo: "HH EH1 L OW0" → "hɛloʊ"

Autor: Nicolás Espejo
Proyecto: Jelou
Licencia: MIT
"""

from typing import Optional, Tuple

ARPABET_TO_IPA = {
    "AA": "ɑ",
    "AE": "æ",
    "AH": "ʌ",
    "AO": "ɔ",
    "AW": "aʊ",
    "AY": "aɪ",
    "EH": "ɛ",
    "ER": "ɝ",
    "EY": "eɪ",
    "IH": "ɪ",
    "IY": "i",
    "OW": "oʊ",
    "OY": "ɔɪ",
    "UH": "ʊ",
    "UW": "uː",
    "B": "b",
    "CH": "tʃ",
    "D": "d",
    "DH": "ð",
    "F": "f",
    "G": "g",
    "HH": "h",
    "JH": "dʒ",
    "K": "k",
    "L": "l",
    "M": "m",
    "N": "n",
    "NG": "ŋ",
    "P": "p",
    "R": "r",
    "S": "s",
    "SH": "ʃ",
    "T": "t",
    "TH": "θ",
    "V": "v",
    "W": "w",
    "Y": "j",
    "Z": "z",
    "ZH": "ʒ",
}


def arpabet_to_ipa(arpabet_sequence: str) -> str:
    """
    Convierte ARPABET a IPA insertando ~~STRESS~~ antes de la vocal tónica.

    El stress secundario (2) se ignora — en español solo hay una sílaba tónica.
    Si hay múltiples stress primarios (1), se toma el último (resuelve "information").

    >>> arpabet_to_ipa("HH EH1 L OW0")
    'hɛ~~STRESS~~loʊ'  # stress en EH
    """
    if not arpabet_sequence:
        return ""

    phonemes = arpabet_sequence.upper().split()

    STRESSED_VOWELS = {
        "AA", "AE", "AH", "AO", "AW", "AY",
        "EH", "ER", "EY", "IH", "IY", "OW",
        "OY", "UH", "UW"
    }

    # Tomar el último stress primario (1) como vocal tónica
    primary_stress_index = None
    for i, phoneme in enumerate(phonemes):
        if phoneme and phoneme[-1] == "1":
            clean = phoneme.rstrip("012")
            if clean in STRESSED_VOWELS:
                primary_stress_index = i

    ipa_result = []
    for i, phoneme in enumerate(phonemes):
        clean_phoneme = phoneme.rstrip("012")
        if clean_phoneme in ARPABET_TO_IPA:
            ipa_symbol = ARPABET_TO_IPA[clean_phoneme]
            if i == primary_stress_index:
                ipa_result.append("~~STRESS~~" + ipa_symbol)
            else:
                ipa_result.append(ipa_symbol)
        else:
            ipa_result.append(clean_phoneme.lower())

    return "".join(ipa_result)


def arpabet_to_ipa_clean(arpabet_sequence: str) -> str:
    """Retorna IPA puro sin marcadores ~~STRESS~~. Para mostrar al usuario."""
    return arpabet_to_ipa(arpabet_sequence).replace("~~STRESS~~", "")


def parse_cmu_line(line: str) -> Optional[Tuple[str, str]]:
    """
    Parsea una línea del CMU Dictionary y retorna (palabra, ipa) o None.

    Ignora comentarios (;;;) y limpia variantes (WORD(2) → word).

    >>> parse_cmu_line("HELLO  HH AH0 L OW1")
    ('hello', 'hʌloʊ')
    >>> parse_cmu_line(";;;Comment")
    None
    """
    line = line.strip()
    if not line or line.startswith(";;;"):
        return None

    parts = line.split(maxsplit=1)
    if len(parts) < 2:
        return None

    word, arpabet = parts
    word = word.split("(")[0].lower()
    return (word, arpabet_to_ipa_clean(arpabet))