"""
Tests de integración end-to-end para Jelou API
"""

from jelou.jelou_api import translate_word, translate_ipa


def test_translate_ipa_direct():
    """Test conversión directa IPA → español"""
    assert translate_ipa("θɪŋk") == "zink"
    assert translate_ipa("ʃiː") == "shí"
    assert translate_ipa("wɝld") == "werld"


def test_translate_word_structure():
    """Test estructura del resultado de translate_word"""
    result = translate_word("hello")
    
    # Verificar estructura
    assert 'word' in result
    assert 'ipa' in result
    assert 'spanish' in result
    assert 'found' in result
    
    assert result['word'] == "hello"
    assert result['found'] is True
    assert result['ipa'] is not None
    assert result['spanish'] is not None


def test_translate_word_not_found():
    """Test palabra no encontrada"""
    result = translate_word("xyzabc123notaword")
    
    assert result['found'] is False
    assert result['ipa'] is None
    assert result['spanish'] is None


def test_integration_think():
    """Test completo del flujo con IPA conocido"""
    result = translate_ipa("θɪŋk")
    assert result == "zink"


def test_integration_vision():
    """Test con palabra que tiene sonido ʒ"""
    result = translate_ipa("vɪʒʌn")
    assert result == "vishan"
