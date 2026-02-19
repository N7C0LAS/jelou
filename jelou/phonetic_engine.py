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


def ipa_to_spanish(ipa: str) -> str:
    import re
    stressed_ipa = ipa

    STRESS_MAP = {
        "aʊ": "áu", "aɪ": "ái", "eɪ": "éi", "oʊ": "óu", "ɔɪ": "ói",
        "iː": "í", "uː": "ú",
        "ɑ": "á", "æ": "á", "ʌ": "á", "ɔ": "ó",
        "ɛ": "é", "ɝ": "ér", "ɪ": "í", "i": "í", "ʊ": "ú",
    }
    for ipa_v, esp_v in sorted(STRESS_MAP.items(), key=lambda x: -len(x[0])):
        stressed_ipa = stressed_ipa.replace("~~STRESS~~" + ipa_v, "~~A~~" + esp_v)
    stressed_ipa = stressed_ipa.replace("~~STRESS~~", "")

    result = stressed_ipa.lower()
    result = result.replace("ˈ", "").replace("ˌ", "")

    # Eliminar semivocal j redundante después de dʒ antes de proteger j
    # Resuelve: "education" ɛdʒjuːk → eyukéishan (no eyiúkéishan)
    result = result.replace("dʒj", "dʒ")

    result = result.replace("j", "~~~TEMP_J~~~")

    for ipa_sound, adapted in COMPOUND_RULES.items():
        result = result.replace(ipa_sound, adapted)

    result = result.replace("sh", "~~~TEMP_SH~~~")
    result = result.replace("ch", "~~~TEMP_CH~~~")

    for ipa_sound, adapted in VOWEL_RULES.items():
        result = result.replace(ipa_sound, adapted)

    for ipa_sound, adapted in CONSONANT_RULES.items():
        result = result.replace(ipa_sound, adapted)

    result = result.replace("~~~TEMP_J~~~", "i")
    result = result.replace("~~~TEMP_SH~~~", "sh")
    result = result.replace("~~~TEMP_CH~~~", "ch")

    for vocal in ["a", "e", "i", "o", "u", "á", "é", "í", "ó", "ú"]:
        if result.endswith(f"{vocal}y"):
            result = result[:-1] + "sh"

    result = result.replace("pj", "pi")
    result = result.replace("ngk", "nk")
    result = result.replace("ngg", "ng")
    result = result.replace("íi", "íe")
    result = result.replace("ii", "ie")
    result = result.replace("~~a~~", "")

    return result