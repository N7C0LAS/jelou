"""
Jelou Web Application - Backend Flask
======================================

Este módulo implementa el servidor web para la aplicación Jelou.
Proporciona una API REST y sirve la interfaz HTML para usuarios finales.

Arquitectura:
-------------
- Backend: Flask (Python)
- Frontend: HTML + Tailwind CSS + JavaScript
- API: REST con JSON
- Deploy: Render (producción)

Endpoints:
----------
GET  /              - Página principal (HTML)
POST /api/translate - API para traducir palabras
GET  /api/health    - Health check para monitoreo

Stack tecnológico:
------------------
- Flask: Framework web ligero
- Flask-CORS: Permite peticiones cross-origin
- Jelou API: Motor de traducción integrado

Autor: Nicolás Espejo
Proyecto: Jelou
Licencia: MIT
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path

# Agregar el directorio raíz al path para importar el paquete jelou
# Esto permite que web/app.py importe jelou incluso estando en un subdirectorio
sys.path.insert(0, str(Path(__file__).parent.parent))

from jelou import translate_word, translate_ipa  # noqa: E402

# =========================
# CONFIGURACIÓN DE FLASK
# =========================

# Inicializar aplicación Flask
app = Flask(__name__)

# Habilitar CORS (Cross-Origin Resource Sharing)
# Permite que la API sea accesible desde otros dominios
# Útil para desarrollo y para futuras apps móviles
CORS(app)


# =========================
# RUTAS - FRONTEND
# =========================


@app.route("/")
def index():
    """
    Página principal de la aplicación web.

    Sirve el archivo HTML que contiene la interfaz de usuario.
    El HTML se encuentra en web/templates/index.html

    Returns:
        str: Contenido HTML renderizado

    Note:
        Flask busca automáticamente templates en la carpeta 'templates/'
        relativa a la ubicación de app.py
    """
    return render_template("index.html")


# =========================
# RUTAS - API REST
# =========================


@app.route("/api/translate", methods=["POST"])
def translate():
    """
    Endpoint API para traducir palabras o IPA a español.

    Este es el endpoint principal de la API. Acepta peticiones POST
    con JSON y retorna la traducción correspondiente.

    Request (JSON):
    ---------------
    {
        "word": "hello",      # Palabra en inglés o IPA
        "mode": "word"        # "word" o "ipa"
    }

    Response Success (JSON):
    ------------------------
    {
        "success": true,
        "word": "hello",
        "ipa": "hʌloʊ",
        "spanish": "halou",
        "found": true,
        "mode": "word"
    }

    Response Error (JSON):
    ----------------------
    {
        "success": false,
        "error": "Descripción del error"
    }

    HTTP Status Codes:
    ------------------
    200: Éxito
    400: Bad Request (falta palabra, palabra vacía)
    500: Error interno del servidor

    Examples:
        Modo palabra:
        POST /api/translate
        {"word": "hello", "mode": "word"}
        → {"success": true, "spanish": "halou", ...}

        Modo IPA:
        POST /api/translate
        {"word": "θɪŋk", "mode": "ipa"}
        → {"success": true, "spanish": "zink", ...}

    Note:
        La primera petición puede ser lenta (~2-3 segundos) porque
        carga el diccionario CMU. Las siguientes son instantáneas.
    """
    try:
        # ==================
        # VALIDAR REQUEST
        # ==================

        # Obtener datos JSON del request
        data = request.get_json()

        # Validar que se envió JSON
        if not data or "word" not in data:
            return (
                jsonify(
                    {"success": False, "error": "No se proporcionó ninguna palabra"}
                ),
                400,
            )

        # Extraer parámetros
        word = data["word"].strip()
        mode = data.get("mode", "word")  # Default: modo palabra

        # Validar que la palabra no esté vacía
        if not word:
            return jsonify({"success": False, "error": "La palabra está vacía"}), 400

        # ==================
        # MODO IPA DIRECTO
        # ==================

        if mode == "ipa":
            # Conversión directa IPA → español
            spanish = translate_ipa(word)

            return jsonify(
                {
                    "success": True,
                    "word": word,
                    "ipa": word,  # En modo IPA, input = IPA
                    "spanish": spanish,
                    "found": True,  # Siempre True en modo IPA
                    "mode": "ipa",
                }
            )

        # ==================
        # MODO PALABRA
        # ==================

        else:
            # Traducción completa: palabra → IPA → español
            result = translate_word(word)

            return jsonify(
                {
                    "success": True,
                    **result,  # Spread operator: incluye word, ipa, spanish, found
                    "mode": "word",
                }
            )

    # ==================
    # MANEJO DE ERRORES
    # ==================

    except Exception as e:
        # Capturar cualquier error inesperado
        # En producción, esto también se registra en logs
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health():
    """
    Health check endpoint para monitoreo.

    Este endpoint es útil para:
    - Verificar que el servidor está funcionando
    - Monitoreo automático (Render, uptime monitors)
    - Load balancers y orquestadores

    Returns:
        JSON: Estado del servicio

    Response:
    ---------
    {
        "status": "ok",
        "service": "jelou"
    }

    HTTP Status:
    ------------
    200: Servicio funcionando correctamente

    Example:
        GET /api/health
        → {"status": "ok", "service": "jelou"}

    Note:
        Este endpoint no requiere autenticación y siempre retorna 200
        si el servidor está funcionando.
    """
    return jsonify({"status": "ok", "service": "jelou"})


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    """
    Ejecuta el servidor Flask en modo desarrollo.

    Configuración de desarrollo:
    ----------------------------
    - debug=True: Recarga automática al cambiar código
    - host='0.0.0.0': Accesible desde cualquier IP (útil para testing en red local)
    - port=5000: Puerto estándar de Flask

    En producción (Render):
    -----------------------
    Se usa Gunicorn en lugar de este servidor de desarrollo.
    Ver: web/gunicorn_config.py y Procfile

    Uso:
    ----
    python web/app.py

    Luego abrir: http://localhost:5000

    Note:
        NO usar este servidor en producción. Es solo para desarrollo.
        Para producción, usar Gunicorn con configuración apropiada.
    """
    app.run(debug=True, host="0.0.0.0", port=5000)
