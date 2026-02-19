/**
 * Jelou Web Application - Frontend JavaScript
 * ============================================
 * 
 * Este módulo maneja toda la lógica del frontend de la aplicación web Jelou.
 * Gestiona la interacción del usuario, peticiones API y actualización de UI.
 * 
 * Funcionalidades:
 * ----------------
 * - Cambio de modo (Palabra / IPA directo)
 * - Validación de entrada
 * - Peticiones AJAX a la API
 * - Actualización dinámica de resultados
 * - Manejo de estados (loading, error, success)
 * - Ejemplos interactivos
 * 
 * Stack:
 * ------
 * - Vanilla JavaScript (sin frameworks)
 * - Fetch API para peticiones HTTP
 * - Manipulación directa del DOM
 * 
 * Autor: Nicolás Espejo
 * Proyecto: Jelou
 * Licencia: MIT
 */


// =========================
// ESTADO DE LA APLICACIÓN
// =========================

/**
 * Modo actual de traducción
 * @type {string} 'word' para modo palabra, 'ipa' para modo IPA directo
 */
let currentMode = 'word';


// =========================
// ELEMENTOS DEL DOM
// =========================

// Controles principales
const wordInput = document.getElementById('wordInput');
const translateBtn = document.getElementById('translateBtn');
const modeWordBtn = document.getElementById('modeWord');
const modeIPABtn = document.getElementById('modeIPA');
const inputLabel = document.getElementById('inputLabel');

// Contenedores de estado
const resultDiv = document.getElementById('result');
const errorDiv = document.getElementById('error');
const loadingDiv = document.getElementById('loading');

// Elementos de resultado
const resultWord = document.getElementById('resultWord');
const resultIPA = document.getElementById('resultIPA');
const resultSpanish = document.getElementById('resultSpanish');
const ipaSection = document.getElementById('ipaSection');
const errorMessage = document.getElementById('errorMessage');


// =========================
// CAMBIO DE MODO
// =========================

/**
 * Cambia al modo "Palabra en inglés"
 */
modeWordBtn.addEventListener('click', () => {
    currentMode = 'word';
    
    modeWordBtn.classList.remove('bg-gray-200', 'text-gray-700');
    modeWordBtn.classList.add('bg-indigo-600', 'text-white');
    modeIPABtn.classList.remove('bg-indigo-600', 'text-white');
    modeIPABtn.classList.add('bg-gray-200', 'text-gray-700');
    
    inputLabel.textContent = 'Escribe una palabra en inglés:';
    wordInput.placeholder = 'Ejemplo: hello';
    wordInput.value = '';
    hideResults();
});

/**
 * Cambia al modo "IPA directo"
 */
modeIPABtn.addEventListener('click', () => {
    currentMode = 'ipa';
    
    modeIPABtn.classList.remove('bg-gray-200', 'text-gray-700');
    modeIPABtn.classList.add('bg-indigo-600', 'text-white');
    modeWordBtn.classList.remove('bg-indigo-600', 'text-white');
    modeWordBtn.classList.add('bg-gray-200', 'text-gray-700');
    
    inputLabel.textContent = 'Escribe en notación IPA:';
    wordInput.placeholder = 'Ejemplo: θɪŋk';
    wordInput.value = '';
    hideResults();
});


// =========================
// FUNCIÓN PRINCIPAL DE TRADUCCIÓN
// =========================

/**
 * Traduce la palabra o IPA ingresado por el usuario.
 * 
 * Flujo:
 * ------
 * 1. Validar que hay entrada
 * 2. Mostrar estado de carga
 * 3. Hacer petición POST a /api/translate
 * 4. Procesar respuesta
 * 5. Mostrar resultado o error
 * 
 * @async
 * @returns {Promise<void>}
 */
async function translate() {
    const word = wordInput.value.trim();
    
    if (!word) {
        showError('Por favor escribe una palabra');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                word: word,
                mode: currentMode
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            if (currentMode === 'word' && !data.found) {
                showError(`La palabra "${word}" no se encontró en el diccionario. Intenta usar el modo IPA.`);
            } else {
                showResult(data);
            }
        } else {
            showError(data.error || 'Error desconocido');
        }
        
    } catch (error) {
        showError('Error de conexión. Por favor intenta de nuevo.');
        console.error('Error:', error);
    }
}


// =========================
// FUNCIONES DE UI
// =========================

/**
 * Muestra el resultado de la traducción.
 */
function showResult(data) {
    hideAll();

    resultWord.textContent = data.word;
    resultIPA.textContent = data.ipa || '-';
    resultSpanish.textContent = data.spanish;

    if (currentMode === 'ipa') {
        ipaSection.classList.add('hidden');
    } else {
        ipaSection.classList.remove('hidden');
    }

    resultDiv.classList.remove('hidden');
    resultDiv.classList.add('fade-in');

    showPronunciationGuide(data.spanish || '');
}

/**
 * Muestra un mensaje de error.
 */
function showError(message) {
    hideAll();
    errorMessage.textContent = message;
    errorDiv.classList.remove('hidden');
    errorDiv.classList.add('fade-in');
}

/**
 * Muestra el indicador de carga.
 */
function showLoading() {
    hideAll();
    loadingDiv.classList.remove('hidden');
}

/**
 * Oculta todos los contenedores de estado.
 */
function hideAll() {
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    loadingDiv.classList.add('hidden');
}

/**
 * Oculta los resultados.
 */
function hideResults() {
    hideAll();
}


// =========================
// EVENT LISTENERS
// =========================

translateBtn.addEventListener('click', translate);

wordInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        translate();
    }
});

document.querySelectorAll('.example-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        if (currentMode === 'ipa') {
            modeWordBtn.click();
        }
        wordInput.value = btn.textContent.trim();
        translate();
    });
});


// =========================
// INICIALIZACIÓN
// =========================

wordInput.focus();


// =========================
// COPIAR RESULTADO
// =========================

/**
 * Copia la pronunciación en español al portapapeles.
 */
function copyResult() {
    const text = resultSpanish.textContent;
    if (!text) return;

    navigator.clipboard.writeText(text).then(() => {
        const btn = document.getElementById('copyBtnText');
        btn.textContent = '¡Copiado!';
        setTimeout(() => {
            btn.textContent = 'Copiar';
        }, 2000);
    }).catch(() => {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        const btn = document.getElementById('copyBtnText');
        btn.textContent = '¡Copiado!';
        setTimeout(() => {
            btn.textContent = 'Copiar';
        }, 2000);
    });
}


// =========================
// AUDIO - WEB SPEECH API
// =========================

/**
 * Carga las voces disponibles del navegador de forma asíncrona.
 * Chrome carga las voces de manera diferida, por lo que se necesita
 * esperar a que estén disponibles antes de intentar usarlas.
 * 
 * @returns {Promise<SpeechSynthesisVoice[]>}
 */
function getVoices() {
    return new Promise((resolve) => {
        const voices = speechSynthesis.getVoices();
        if (voices.length > 0) {
            resolve(voices);
            return;
        }
        // Chrome dispara este evento cuando las voces están listas
        speechSynthesis.onvoiceschanged = () => {
            resolve(speechSynthesis.getVoices());
        };
        // Timeout de seguridad: si en 3 segundos no hay voces, continuar igual
        setTimeout(() => resolve(speechSynthesis.getVoices()), 3000);
    });
}

/**
 * Pronuncia la palabra original en inglés usando Web Speech API.
 * 
 * Detecta correctamente si el navegador soporta audio:
 * - Sin speechSynthesis → navegador sin soporte (Firefox antiguo, etc.)
 * - Brave bloquea speechSynthesis por privacidad → voces vacías tras espera
 * - Chrome/Edge → voces se cargan asincrónicamente, se espera antes de verificar
 */
async function speakWord() {
    const word = resultWord.textContent;
    if (!word) return;

    if (!window.speechSynthesis) {
        alert('Tu navegador no soporta audio. Prueba con Chrome o Edge.');
        return;
    }

    const btn = document.getElementById('audioBtnText');
    btn.textContent = '🔊 Cargando...';

    const voices = await getVoices();

    // Si tras esperar no hay voces, es Brave u otro navegador restrictivo
    if (voices.length === 0) {
        btn.textContent = 'Escuchar';
        alert('Audio no disponible en este navegador. Prueba con Chrome o Edge.');
        return;
    }

    const utterance = new SpeechSynthesisUtterance(word);
    utterance.lang = 'en-US';
    utterance.rate = 0.9;

    utterance.onstart = () => { btn.textContent = '🔊 Reproduciendo...'; };
    utterance.onend = () => { btn.textContent = 'Escuchar'; };
    utterance.onerror = () => { btn.textContent = 'Escuchar'; };

    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
}


// =========================
// MODO OSCURO
// =========================

/**
 * Alterna entre modo claro y oscuro.
 * Guarda la preferencia en localStorage.
 */
function toggleTheme() {
    const html = document.documentElement;
    const isDark = html.classList.contains('dark');
    const icon = document.getElementById('themeIcon');

    if (isDark) {
        html.classList.remove('dark');
        localStorage.setItem('theme', 'light');
        icon.textContent = '🌙';
    } else {
        html.classList.add('dark');
        localStorage.setItem('theme', 'dark');
        icon.textContent = '☀️';
    }
}

// Sincronizar ícono con tema actual al cargar
(function() {
    const theme = localStorage.getItem('theme') || 'light';
    const icon = document.getElementById('themeIcon');
    if (icon) icon.textContent = theme === 'dark' ? '☀️' : '🌙';
})();


// =========================
// GUÍA CONTEXTUAL DE PRONUNCIACIÓN
// =========================

const PRONUNCIATION_TIPS = {
    'sh': '💡 SH se pronuncia como cuando pides silencio: "shhhh"',
    'ng': '💡 NG se pronuncia como la N de "banco" o "tango"',
    'er': '💡 ER es un sonido único del inglés — lengua curvada hacia atrás',
    'ch': '💡 CH se pronuncia igual que en español: "chico"',
    'z': '💡 Z se pronuncia como la Z española — lengua entre dientes soplando'
};

function showPronunciationGuide(spanish) {
    const guide = document.getElementById('pronunciationGuide');
    const tip = document.getElementById('pronunciationTip');
    if (!guide || !tip) return;

    const text = spanish.toLowerCase();
    const tips = [];

    if (text.includes('sh')) tips.push(PRONUNCIATION_TIPS['sh']);
    if (text.includes('ng')) tips.push(PRONUNCIATION_TIPS['ng']);
    if (text.includes('er')) tips.push(PRONUNCIATION_TIPS['er']);
    if (text.includes('ch')) tips.push(PRONUNCIATION_TIPS['ch']);
    if (text.includes('z')) tips.push(PRONUNCIATION_TIPS['z']);

    if (tips.length === 0) {
        guide.classList.add('hidden');
        return;
    }

    tip.innerHTML = tips.join('<br>');
    guide.classList.remove('hidden');
}