from jelou.phonetic_engine import ipa_to_spanish

def test_long_vowels():
    assert ipa_to_spanish("iː") == "í"
    assert ipa_to_spanish("uː") == "ú"

def test_short_vowels():
    assert ipa_to_spanish("ɪ") == "i"
    assert ipa_to_spanish("ʌ") == "a"

def test_r_colored_vowel():
    assert ipa_to_spanish("ɝ") == "er"

def test_schwa_is_converted_to_a():
    from jelou.phonetic_engine import ipa_to_spanish

    assert ipa_to_spanish("ə") == "a"
    assert ipa_to_spanish("əbaʊt") == "abaut"

def test_open_e_vowel():
    assert ipa_to_spanish("ɛ") == "e"
    assert ipa_to_spanish("bɛd") == "bed"

def test_short_u_vowel():
    assert ipa_to_spanish("ʊ") == "u"
    assert ipa_to_spanish("bʊk") == "buk"

def test_weak_r_vowel():
    assert ipa_to_spanish("ɚ") == "er"
    assert ipa_to_spanish("bɛtɚ") == "beter"
