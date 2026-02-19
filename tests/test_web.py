"""
Tests para el backend Flask de Jelou.
Cubre los endpoints principales de la API REST.
"""

import pytest
from web.app import app


@pytest.fixture
def client():
    """Cliente de prueba para la aplicación Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_returns_200(client):
    """GET / debe retornar 200 y HTML."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Jelou" in response.data


def test_health_check(client):
    """GET /api/health debe retornar status ok."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "jelou"


def test_translate_word(client):
    """POST /api/translate con palabra válida debe retornar transliteración."""
    response = client.post(
        "/api/translate",
        json={"word": "hello", "mode": "word"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["word"] == "hello"
    assert "spanish" in data
    assert "ipa" in data


def test_translate_ipa_mode(client):
    """POST /api/translate en modo IPA debe funcionar correctamente."""
    response = client.post(
        "/api/translate",
        json={"word": "θɪŋk", "mode": "ipa"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["spanish"] == "zink"
    assert data["mode"] == "ipa"


def test_translate_missing_word(client):
    """POST /api/translate sin palabra debe retornar error 400."""
    response = client.post(
        "/api/translate",
        json={}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False


def test_translate_empty_word(client):
    """POST /api/translate con palabra vacía debe retornar error 400."""
    response = client.post(
        "/api/translate",
        json={"word": "   ", "mode": "word"}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False


def test_translate_word_not_found(client):
    """POST /api/translate con palabra inexistente debe retornar found=False."""
    response = client.post(
        "/api/translate",
        json={"word": "xyzxyzxyz", "mode": "word"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["found"] is False
