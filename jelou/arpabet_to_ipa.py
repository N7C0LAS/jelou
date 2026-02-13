"""
Conversor de ARPABET (CMU Dictionary) a IPA (International Phonetic Alphabet)

El CMU Pronouncing Dictionary usa ARPABET, un sistema de notación fonética
basado en ASCII. Este módulo convierte ARPABET a IPA para poder usar
el motor fonético de Jelou.
"""

from typing import Optional, Tuple

# Tabla de conversión ARPABET → IPA
# Basado en la convención del CMU Pronouncing Dictionary
ARPABET_TO_IPA = {
    # Vocales
    "AA": "ɑ",      # father
    "AE": "æ",      # cat
    "AH": "ʌ",      # but
    "AO": "ɔ",      # dog
    "AW": "aʊ",     # now
    "AY": "aɪ",     # time
    "EH": "ɛ",      # bed
    "ER": "ɝ",      # bird
    "EY": "eɪ",     # day
    "IH": "ɪ",      # sit
    "IY": "iː",     # see
    "OW": "oʊ",     # go
    "OY": "ɔɪ",     # boy
    "UH": "ʊ",      # book
    "UW": "uː",     # food
    
    # Consonantes
    "B": "b",
    "CH": "tʃ",
    "D": "d",
    "DH": "ð",      # this
    "F": "f",
    "G": "g",
    "HH": "h",
    "JH": "dʒ",     # job
    "K": "k",
    "L": "l",
    "M": "m",
    "N": "n",
    "NG": "ŋ",      # sing
    "P": "p",
    "R": "r",
    "S": "s",
    "SH": "ʃ",      # she
    "T": "t",
    "TH": "θ",      # think
    "V": "v",
    "W": "w",
    "Y": "j",       # yes
    "Z": "z",
    "ZH": "ʒ",      # vision
}


def arpabet_to_ipa(arpabet_sequence: str) -> str:
    """
    Convierte una secuencia ARPABET a IPA.
    
    Args:
        arpabet_sequence: String con fonemas ARPABET separados por espacios
                         Puede incluir números de estrés (0, 1, 2)
                         Ej: "HH AH0 L OW1"
    
    Returns:
        String en notación IPA
        
    Examples:
        >>> arpabet_to_ipa("HH EH1 L OW0")
        'hɛloʊ'
        >>> arpabet_to_ipa("TH IH1 ŋ K")
        'θɪŋk'
    """
    if not arpabet_sequence:
        return ""
    
    # Separar por espacios y procesar cada fonema
    phonemes = arpabet_sequence.upper().split()
    ipa_result = []
    
    for phoneme in phonemes:
        # Remover números de estrés (0, 1, 2)
        clean_phoneme = phoneme.rstrip("012")
        
        # Buscar en la tabla de conversión
        if clean_phoneme in ARPABET_TO_IPA:
            ipa_result.append(ARPABET_TO_IPA[clean_phoneme])
        else:
            # Si no se encuentra, pasar tal cual (fallback)
            ipa_result.append(clean_phoneme.lower())
    
    return "".join(ipa_result)



def parse_cmu_line(line: str) -> Optional[tuple[str, str]]
    """
    Parsea una línea del CMU Dictionary.
    
    Formato esperado:
    WORD  PHONEME1 PHONEME2 ...
    
    Args:
        line: Línea del diccionario CMU
        
    Returns:
        Tupla (palabra, ipa) o None si la línea no es válida
        
    Examples:
        >>> parse_cmu_line("HELLO  HH AH0 L OW1")
        ('hello', 'hɛloʊ')
    """
    line = line.strip()
    
    # Ignorar líneas vacías o comentarios
    if not line or line.startswith(";;;"):
        return None
    
    # Separar palabra y fonemas
    parts = line.split(maxsplit=1)
    if len(parts) < 2:
        return None
    
    word, arpabet = parts
    
    # Limpiar palabra (remover variantes como HELLO(1), HELLO(2))
    word = word.split("(")[0].lower()
    
    # Convertir a IPA
    ipa = arpabet_to_ipa(arpabet)
    
    return (word, ipa)
