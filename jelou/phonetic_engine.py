"""
Motor de Adaptación Fonética - IPA a Español
=============================================

Este módulo convierte símbolos del Alfabeto Fonético Internacional (IPA)
a una representación fonética legible usando el alfabeto español.

Propósito:
----------
Facilitar la pronunciación del inglés para hispanohablantes sin necesidad
de aprender IPA. El sistema prioriza claridad y utilidad sobre precisión
lingüística académica.

Principios de diseño:
---------------------
1. Un símbolo representa un solo sonido
2. Conversión determinista (misma entrada = misma salida)
3. Sistema consistente y predecible
4. Resultado pronunciable sin contexto adicional

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
    "aɪər": "air",   # Diptongo + schwa + r: "fire" → "fair"
    "aʊər": "aur",   # Diptongo + schwa + r: "hour" → "aur"
    "dʒ": "y",       # Africada sonora: "job" → "yob"
    "tʃ": "ch",      # Africada sorda: "chair" → "cher"
    "θ": "z",        # Fricativa dental sorda: "think" → "zink"
    "ð": "d",        # Fricativa dental sonora: "this" → "dis"
    "ʃ": "sh",       # Fricativa postalveolar sorda: "she" → "shí"
    "ʒ": "sh",       # Fricativa postalveolar sonora: "vision" → "vishan"
    "eər": "er",     # Vocal + schwa + r: "care" → "ker"
}

# Reglas de vocales: Mapeo de vocales IPA a representación en español
# Se incluyen vocales cortas, largas (marcadas con ː), diptongos y vocales r-coloreadas
VOWEL_RULES = {
    "iː": "í",       # Vocal larga: "see" → "sí"
    "ɪ": "i",        # Vocal corta: "sit" → "sit"
    "ɛ": "e",        # Vocal abierta: "bed" → "bed"
    "æ": "a",        # Vocal baja frontal: "cat" → "kat"
    "ɑ": "a",        # Vocal baja posterior: "father" → "fáder"
    "ʌ": "a",        # Vocal media-baja: "but" → "bat"
    "e": "e",        # Vocal media: "bed" → "bed"
    "ə": "a",        # Schwa (vocal neutra): "about" → "abaut"
    "ɔ": "o",        # Vocal media-baja posterior: "law" → "lo"
    "ʊ": "u",        # Vocal alta posterior corta: "book" → "buk"
    "aʊ": "au",      # Diptongo: "now" → "nau"
    "oʊ": "ou",      # Diptongo: "go" → "gou"
    "uː": "ú",       # Vocal larga: "food" → "fúd"
    "ɝ": "er",       # Vocal r-coloreada: "bird" → "berd"
    "ɚ": "er",       # Vocal r-coloreada débil: "better" → "beter"
}

# Reglas de consonantes: Mapeo directo de consonantes IPA a español
# La mayoría tienen correspondencia directa con el español
CONSONANT_RULES = {
    "ŋ": "ng",       # Nasal velar: "sing" → "sing"
    "k": "k",        # Oclusiva velar sorda
    "s": "s",        # Fricativa alveolar sorda
    "z": "z",        # Fricativa alveolar sonora
    "w": "w",        # Aproximante labio-velar
    "r": "r",        # Aproximante alveolar
    "l": "l",        # Aproximante lateral alveolar
    "n": "n",        # Nasal alveolar
    "m": "m",        # Nasal bilabial
    "f": "f",        # Fricativa labiodental sorda
    "v": "v",        # Fricativa labiodental sonora
    "b": "b",        # Oclusiva bilabial sonora
    "p": "p",        # Oclusiva bilabial sorda
    "t": "t",        # Oclusiva alveolar sorda
    "d": "d",        # Oclusiva alveolar sonora
    "g": "g",        # Oclusiva velar sonora
}


# =========================
# MOTOR DE CONVERSIÓN
# =========================

def ipa_to_spanish(ipa: str) -> str:
    """
    Convierte una cadena IPA a representación fonética en español.
    
    Esta es la función principal del motor fonético. Procesa la entrada
    IPA en tres fases: reglas compuestas, vocales, y consonantes.
    
    Proceso:
    --------
    1. Normaliza la entrada (minúsculas, elimina marcas de acento)
    2. Aplica reglas compuestas (deben ir primero)
    3. Aplica reglas de vocales
    4. Aplica reglas de consonantes
    5. Aplica correcciones fonéticas finales
    
    Args:
        ipa (str): Cadena en notación IPA (ej: "θɪŋk", "hɛˈloʊ")
        
    Returns:
        str: Representación fonética en español (ej: "zink", "helou")
        
    Examples:
        >>> ipa_to_spanish("θɪŋk")
        'zink'
        >>> ipa_to_spanish("ʃiː")
        'shí'
        >>> ipa_to_spanish("wɝld")
        'werld'
        
    Note:
        Las marcas de acento primario (ˈ) y secundario (ˌ) del IPA
        se eliminan ya que el español usa acentos gráficos.
    """
    # Paso 1: Normalizar entrada
    result = ipa.lower()

    # Paso 2: Eliminar marcas de acento del IPA (no las usamos en español)
    result = result.replace("ˈ", "").replace("ˌ", "")

    # Paso 3: Aplicar reglas compuestas (PRIMERO - orden importa)
    # Estas deben procesarse antes que las reglas individuales para evitar
    # conversiones parciales incorrectas
    for ipa_sound, adapted in COMPOUND_RULES.items():
        result = result.replace(ipa_sound, adapted)

    # Paso 4: Aplicar reglas de vocales
    for ipa_sound, adapted in VOWEL_RULES.items():
        result = result.replace(ipa_sound, adapted)

    # Paso 5: Aplicar reglas de consonantes
    for ipa_sound, adapted in CONSONANT_RULES.items():
        result = result.replace(ipa_sound, adapted)

    # Paso 6: Correcciones fonéticas finales
    # Estas reglas evitan secuencias problemáticas en español
    result = result.replace("ngk", "nk")    # "finger" → "finger" no "fingger"
    result = result.replace("ngg", "ng")    # "longer" → "longer" no "longger"

    return result