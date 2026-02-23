"""
Tests de integración end-to-end para Jelou API
"""
from jelou.jelou_api import translate_word, translate_ipa

def test_translate_ipa_direct():
    assert translate_ipa("θɪŋk") == "zink"
    assert translate_ipa("ʃiː") == "shí"
    assert translate_ipa("wɝld") == "werld"

def test_translate_word_structure():
    result = translate_word("hello")
    assert 'word' in result
    assert 'ipa' in result
    assert 'spanish' in result
    assert 'found' in result
    assert result['word'] == "hello"
    assert result['found'] is True
    assert result['ipa'] is not None
    assert result['spanish'] is not None

def test_translate_word_not_found():
    result = translate_word("xyzabc123notaword")
    assert result['found'] is False
    assert result['ipa'] is None
    assert result['spanish'] is None

def test_integration_think():
    result = translate_ipa("θɪŋk")
    assert result == "zink"

def test_integration_vision():
    result = translate_ipa("vɪʒʌn")
    assert result == "vishan"

def test_integration_vehicle():
    result = translate_word("vehicle")
    assert result['found'] is True
    assert result['spanish'] == "víekal"

def test_integration_impossible():
    result = translate_word("impossible")
    assert result['found'] is True
    assert result['spanish'] == "impásabal"

def test_integration_communication():
    result = translate_word("communication")
    assert result['found'] is True
    assert result['spanish'] == "kamiunakéishan"

def test_integration_education():
    result = translate_word("education")
    assert result['found'] is True
    assert result['spanish'] == "eyukéishan"

def test_integration_information():
    result = translate_word("information")
    assert result['found'] is True
    assert result['spanish'] == "inferméishan"

def test_integration_vegetable():
    result = translate_word("vegetable")
    assert result['found'] is True
    assert result['spanish'] == "véchtabal"

def test_integration_monday():
    result = translate_word("monday")
    assert result['found'] is True
    assert result['spanish'] == "mándei"

def test_integration_saturday():
    result = translate_word("saturday")
    assert result['found'] is True
    assert result['spanish'] == "sáterdei"

def test_integration_thursday():
    result = translate_word("thursday")
    assert result['found'] is True
    assert result['spanish'] == "zérsdei"