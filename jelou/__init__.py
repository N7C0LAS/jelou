"""
Jelou - Motor de adaptación fonética Inglés → Español

Convierte pronunciación IPA del inglés en representación
fonética legible para hispanohablantes.
"""

from jelou.jelou_api import translate_word, translate_ipa, batch_translate
from jelou.phonetic_engine import ipa_to_spanish

__version__ = "0.4.8"

__all__ = [
    "translate_word",
    "translate_ipa",
    "batch_translate",
    "ipa_to_spanish",
]
