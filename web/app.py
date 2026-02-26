"""
Backend Flask de Jelou.
Sirve la interfaz web y expone la API REST.

Endpoints:
  GET  /              → página principal
  POST /api/translate → traducción palabra o IPA
  GET  /api/health    → health check

Autor: Nicolás Espejo
Proyecto: Jelou
Licencia: MIT
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from jelou import translate_word, translate_ipa  # noqa: E402

app = Flask(__name__)
CORS(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/translate", methods=["POST"])
@limiter.limit("30 per minute")
def translate():
    """
    Traduce palabra o IPA a fonética en español.

    Request:  {"word": "hello", "mode": "word|ipa"}
    Response: {"success": true, "word": ..., "ipa": ..., "spanish": ..., "found": ...}
    Errors:   400 si falta la palabra, 500 si hay error interno.
    """
    try:
        data = request.get_json()

        if not data or "word" not in data:
            return jsonify({"success": False, "error": "No se proporcionó ninguna palabra"}), 400

        word = data["word"].strip()
        mode = data.get("mode", "word")

        if not word:
            return jsonify({"success": False, "error": "La palabra está vacía"}), 400

        if len(word) > 100:
            return jsonify({"success": False, "error": "La entrada es demasiado larga (máximo 100 caracteres)"}), 400

        if mode == "ipa":
    # Limpiar IPA externo — el usuario puede pegar de cualquier diccionario
            word = word.strip('/')
            word = word.replace('.', '')
            word = word.replace('ː', '')   # eliminar marcador de longitud U+02D0
            word = word.replace(':', '')
            word = word.replace('ˈ', '')   # eliminar marcador de acento primario
            word = word.replace('ˌ', '')   # eliminar marcador de acento secundario
            spanish = translate_ipa(word)
            return jsonify({
                "success": True,
                "word": word,
                "ipa": word,
                "spanish": spanish,
                "found": True,
                "mode": "ipa",
    })
        else:
            result = translate_word(word)
            return jsonify({
                "success": True,
                **result,
                "mode": "word",
            })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Retorna status ok. Usado por Render para monitoreo."""
    return jsonify({"status": "ok", "service": "jelou"})


if __name__ == "__main__":
    # Solo para desarrollo local. En producción se usa Gunicorn.
    app.run(debug=True, host="0.0.0.0", port=5000)