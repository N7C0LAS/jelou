"""
Tests para el conversor ARPABET → IPA
"""

from jelou.arpabet_to_ipa import arpabet_to_ipa, parse_cmu_line


def test_basic_conversion():
    """Test conversión básica de ARPABET a IPA"""
    assert arpabet_to_ipa("HH EH1 L OW0") == "héloʊ"
    assert arpabet_to_ipa("TH IH1 NG K") == "θíŋk"
    assert arpabet_to_ipa("W ER1 L D") == "wérld"


def test_stress_markers_removed():
    """Los marcadores de estrés generan acentos en vocales tónicas"""
    assert arpabet_to_ipa("K AE1 T") == "kát"
    assert arpabet_to_ipa("AH0 B AW1 T") == "ʌbáut"


def test_diphthongs():
    """Test de diptongos"""
    assert arpabet_to_ipa("T AY1 M") == "táim"
    assert arpabet_to_ipa("N AW1") == "náu"
    assert arpabet_to_ipa("B OY1") == "bói"


def test_th_sounds():
    """Test de sonidos TH (θ y ð)"""
    assert arpabet_to_ipa("TH IH1 NG K") == "θíŋk"  # voiceless
    assert arpabet_to_ipa("DH IH1 S") == "ðís"       # voiced


def test_sh_ch_sounds():
    """Test de sonidos SH, CH, ZH"""
    assert arpabet_to_ipa("SH IY1") == "ʃí"
    assert arpabet_to_ipa("CH EH1 R") == "tʃér"
    assert arpabet_to_ipa("V IH1 ZH AH0 N") == "víʒʌn"


def test_parse_cmu_line():
    """Test del parser de líneas CMU"""
    result = parse_cmu_line("HELLO  HH AH0 L OW1")
    assert result == ("hello", "hʌlóu")

    result = parse_cmu_line("WORLD  W ER1 L D")
    assert result == ("world", "wérld")


def test_parse_cmu_line_with_variant():
    """Test de palabras con variantes (HELLO(1), HELLO(2))"""
    result = parse_cmu_line("HELLO(2)  HH EH1 L OW0")
    assert result[0] == "hello"  # Debe limpiar (2)


def test_parse_cmu_line_ignores_comments():
    """Test que ignora comentarios"""
    assert parse_cmu_line(";;;This is a comment") is None
    assert parse_cmu_line("") is None


def test_empty_input():
    """Test con input vacío"""
    assert arpabet_to_ipa("") == ""
