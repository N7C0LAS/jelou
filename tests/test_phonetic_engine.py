from jelou.phonetic_engine import ipa_to_spanish

def test_basic_words():
    assert ipa_to_spanish("θɪŋk") == "zink"
    assert ipa_to_spanish("ðɪs") == "zis"
    assert ipa_to_spanish("ʃiː") == "shi"
    assert ipa_to_spanish("siː") == "si"
    assert ipa_to_spanish("dʒɑb") == "yab"
    assert ipa_to_spanish("wɝld") == "werld"
    assert ipa_to_spanish("ɪˈnʌf") == "inaf"

def test_voiced_th_sound_is_converted_to_z():
    from jelou.phonetic_engine import ipa_to_spanish
    assert ipa_to_spanish("ð") == "z"
    assert ipa_to_spanish("ðɪs") == "zis"
    assert ipa_to_spanish("ðæt") == "zat"


def test_diphthong_au():
    assert ipa_to_spanish("aʊ") == "au"

def test_diphthong_ai():
    assert ipa_to_spanish("aɪ") == "ai"

def test_word_with_diphthong_ai():
    assert ipa_to_spanish("taɪm") == "taim"

def test_diphthong_ou():
    assert ipa_to_spanish("oʊ") == "ou"

def test_diphthong_ei():
    assert ipa_to_spanish("eɪ") == "ei"

def test_diphthong_oi():
    assert ipa_to_spanish("ɔɪ") == "oi"


def test_voiced_sh_sound():
    assert ipa_to_spanish("ʒ") == "sh"
    assert ipa_to_spanish("ˈvɪʒən") == "vishan"

def test_ng_followed_by_g():
    assert ipa_to_spanish("fɪŋgɚ") == "finger"

def test_e_r_diphthong():
    assert ipa_to_spanish("keər") == "ker"
    assert ipa_to_spanish("heər") == "jer"

def test_diphthong_r():
    assert ipa_to_spanish("faɪər") == "fair"
    assert ipa_to_spanish("aʊər") == "aur"
    assert ipa_to_spanish("haʊər") == "jaur"
