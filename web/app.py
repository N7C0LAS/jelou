"""
Jelou Web App - Backend Flask
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path

# Agregar el directorio raíz al path para importar jelou
sys.path.insert(0, str(Path(__file__).parent.parent))

from jelou import translate_word, translate_ipa

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/api/translate', methods=['POST'])
def translate():
    """
    Endpoint API para traducir palabras.
    
    Request JSON:
    {
        "word": "hello",
        "mode": "word"  # o "ipa"
    }
    
    Response JSON:
    {
        "success": true,
        "word": "hello",
        "ipa": "hʌloʊ",
        "spanish": "halou",
        "found": true
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'word' not in data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó ninguna palabra'
            }), 400
        
        word = data['word'].strip()
        mode = data.get('mode', 'word')
        
        if not word:
            return jsonify({
                'success': False,
                'error': 'La palabra está vacía'
            }), 400
        
        if mode == 'ipa':
            # Modo IPA directo
            spanish = translate_ipa(word)
            return jsonify({
                'success': True,
                'word': word,
                'ipa': word,
                'spanish': spanish,
                'found': True,
                'mode': 'ipa'
            })
        else:
            # Modo palabra (por defecto)
            result = translate_word(word)
            
            return jsonify({
                'success': True,
                **result,
                'mode': 'word'
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'jelou'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
