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

Versión: 0.2.3 (Correcciones fonéticas)
Autor: Nicolás Espejo
Proyecto: Jelou
Licencia: MIT
"""

# =========================
# REGLAS FONÉTICAS
# =========================

# Reglas compuestas: Se procesan PRIMERO porque contienen secuencias
# de múltiples símbolos IPA que deben tratarse como una unidad.
# El orden importa: reglas más largas primero para evitar conversiones parciales.
COMPOUND_RULES = {
    "aɪər": "air",  # Diptongo + schwa + r: "fire" → "fair"
    "aʊər": "aur",  # Diptongo + schwa + r: "hour" → "aur"
    "dʒ": "y",  # Africada sonora: "job" → "yob"
    "tʃ": "ch",  # Africada sorda: "chair" → "cher"
    "θ": "z",  # Fricativa dental sorda: "think" → "zink"
    "ð": "d",  # Fricativa dental sonora: "this" → "dis"
    "ʃ": "sh",  # Fricativa postalveolar sorda: "she" → "shí"
    "ʒ": "sh",  # Fricativa postalveolar sonora: "vision" → "vishan"
    "eər": "er",  # Vocal + schwa + r: "care" → "ker"
}

# Reglas de vocales: Mapeo de vocales IPA a representación en español
# Se incluyen vocales cortas, largas (marcadas con ː), diptongos y vocales r-coloreadas
VOWEL_RULES = {
    "iː": "í",  # Vocal larga: "see" → "sí"
    "ɪ": "i",  # Vocal corta: "sit" → "sit"
    "ɛ": "e",  # Vocal abierta: "bed" → "bed"
    "æ": "a",  # Vocal baja frontal: "cat" → "kat"
    "ɑ": "a",  # Vocal baja posterior: "father" → "fáder"
    "ʌ": "a",  # Vocal media-baja: "but" → "bat"
    "e": "e",  # Vocal media: "bed" → "bed"
    "ə": "a",  # Schwa (vocal neutra): "about" → "abaut"
    "ɔ": "o",  # Vocal media-baja posterior: "law" → "lo"
    "ʊ": "u",  # Vocal alta posterior corta: "book" → "buk"
    "aʊ": "au",  # Diptongo: "now" → "nau"
    "oʊ": "ou",  # Diptongo: "go" → "gou"
    "uː": "ú",  # Vocal larga: "food" → "fúd"
    "ɝ": "er",  # Vocal r-coloreada: "bird" → "berd"
    "ɚ": "er",  # Vocal r-coloreada débil: "better" → "beter"
}

# Reglas de consonantes: Mapeo directo de consonantes IPA a español
# La mayoría tienen correspondencia directa con el español
CONSONANT_RULES = {
    "h": "j",  # Fricativa glotal sorda: "hello" → "jelou" (NUEVO)
    "ŋ": "ng",  # Nasal velar: "sing" → "sing"
    "k": "k",  # Oclusiva velar sorda
    "s": "s",  # Fricativa alveolar sorda
    "z": "z",  # Fricativa alveolar sonora
    "w": "w",  # Aproximante labio-velar
    "r": "r",  # Aproximante alveolar
    "l": "l",  # Aproximante lateral alveolar
    "n": "n",  # Nasal alveolar
    "m": "m",  # Nasal bilabial
    "f": "f",  # Fricativa labiodental sorda
    "v": "v",  # Fricativa labiodental sonora
    "b": "b",  # Oclusiva bilabial sonora
    "p": "p",  # Oclusiva bilabial sorda
    "t": "t",  # Oclusiva alveolar sorda
    "d": "d",  # Oclusiva alveolar sonora
    "g": "g",  # Oclusiva velar sonora
}


# =========================
# MOTOR DE CONVERSIÓN
# =========================


def ipa_to_spanish(ipa: str) -> str:
    """
    Convierte una cadena IPA a representación fonética en español.

    Esta es la función principal del motor fonético. Procesa la entrada
    IPA en múltiples fases para lograr precisión fonética.

    Proceso:
    --------
    1. Normaliza la entrada (minúsculas, elimina marcas de acento)
    2. Aplica reglas compuestas (deben ir primero)
    3. Aplica reglas de vocales
    4. Aplica reglas de consonantes
    5. Aplica correcciones contextuales
    6. Aplica correcciones fonéticas finales

    Args:
        ipa (str): Cadena en notación IPA (ej: "θɪŋk", "hɛˈloʊ")

    Returns:
        str: Representación fonética en español (ej: "zink", "jelou")

    Examples:
        >>> ipa_to_spanish("θɪŋk")
        'zink'
        >>> ipa_to_spanish("hɛloʊ")
        'jelou'
        >>> ipa_to_spanish("eɪdʒ")
        'eish'
        >>> ipa_to_spanish("kəmpjuːtɚ")
        'kampiúter'

    Note:
        Las marcas de acento primario (ˈ) y secundario (ˌ) del IPA
        se eliminan ya que el español usa acentos gráficos.

    Cambios en v0.2.3:
        - Corrección: secuencia "íi" → "íe" e "ii" → "ie"
          para palabras como "vehicle" donde IY+IH generaban
          vocal doble en lugar del diptongo correcto.
    """
    # Paso 1: Procesar marcadores de acento ANTES de normalizar
    # Extraer posiciones de acento antes de perderlas con lower()
    import re
    stressed_ipa = ipa

    # Reemplazar ~~STRESS~~VOCAL con la vocal acentuada directamente
    STRESS_MAP = {
        "aʊ": "áu", "aɪ": "ái", "eɪ": "éi", "oʊ": "óu", "ɔɪ": "ói",
        "iː": "í", "uː": "ú",
        "ɑ": "á", "æ": "á", "ʌ": "á", "ɔ": "ó",
        "ɛ": "é", "ɝ": "ér", "ɪ": "í", "i": "í", "ʊ": "ú",
    }
    for ipa_v, esp_v in sorted(STRESS_MAP.items(), key=lambda x: -len(x[0])):
        stressed_ipa = stressed_ipa.replace("~~STRESS~~" + ipa_v, "~~A~~" + esp_v)
    stressed_ipa = stressed_ipa.replace("~~STRESS~~", "")

    # Paso 1b: Normalizar entrada
    result = stressed_ipa.lower()

    # Paso 2: Eliminar marcas de acento del IPA estándar
    result = result.replace("ˈ", "").replace("ˌ", "")

    # Paso 3: ESPECIAL - Proteger /j/ IPA y resultados de reglas compuestas
    # Marcador temporal para /j/ del IPA (yes, you)
    result = result.replace("j", "~~~TEMP_J~~~")

    # Paso 4: Aplicar reglas compuestas PRIMERO
    for ipa_sound, adapted in COMPOUND_RULES.items():
        result = result.replace(ipa_sound, adapted)

    # Paso 5: Proteger "sh" y "ch" creados por reglas compuestas
    # Evita que la "h" en "sh" se convierta a "j"
    result = result.replace("sh", "~~~TEMP_SH~~~")
    result = result.replace("ch", "~~~TEMP_CH~~~")

    # Paso 6: Aplicar reglas de vocales
    for ipa_sound, adapted in VOWEL_RULES.items():
        result = result.replace(ipa_sound, adapted)

    # Paso 7: Aplicar reglas de consonantes
    for ipa_sound, adapted in CONSONANT_RULES.items():
        result = result.replace(ipa_sound, adapted)

    # Paso 8: Restaurar marcadores temporales
    result = result.replace("~~~TEMP_J~~~", "i")
    result = result.replace("~~~TEMP_SH~~~", "sh")
    result = result.replace("~~~TEMP_CH~~~", "ch")

    # Paso 9: Correcciones contextuales para precisión fonética
    for vocal in ["a", "e", "i", "o", "u", "á", "é", "í", "ó", "ú"]:
        if result.endswith(f"{vocal}y"):
            result = result[:-1] + "sh"

    result = result.replace("pj", "pi")

    # Paso 10: Correcciones fonéticas finales
    result = result.replace("ngk", "nk")
    result = result.replace("ngg", "ng")
    # Secuencias de vocales i+i producto de IY+IH se convierten en diptongo ie
    # Ej: "vehicle" IY1+IH0 → "íi" → "íe" → víekal
    result = result.replace("íi", "íe")
    result = result.replace("ii", "ie")

    # Paso 11: Restaurar vocales acentuadas
    result = result.replace("~~a~~", "")

    return result