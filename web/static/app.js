let currentMode = 'word';

const wordInput = document.getElementById('wordInput');
const translateBtn = document.getElementById('translateBtn');
const modeWordBtn = document.getElementById('modeWord');
const modeIPABtn = document.getElementById('modeIPA');
const inputLabel = document.getElementById('inputLabel');

const resultDiv = document.getElementById('result');
const errorDiv = document.getElementById('error');
const loadingDiv = document.getElementById('loading');

const resultWord = document.getElementById('resultWord');
const resultIPA = document.getElementById('resultIPA');
const resultSpanish = document.getElementById('resultSpanish');
const ipaSection = document.getElementById('ipaSection');
const errorMessage = document.getElementById('errorMessage');

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
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ word: word, mode: currentMode })
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

function showError(message) {
    hideAll();
    errorMessage.textContent = message;
    errorDiv.classList.remove('hidden');
    errorDiv.classList.add('fade-in');
}

function showLoading() {
    hideAll();
    loadingDiv.classList.remove('hidden');
}

function hideAll() {
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    loadingDiv.classList.add('hidden');
}

function hideResults() {
    hideAll();
}

translateBtn.addEventListener('click', translate);

wordInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') translate();
});

document.querySelectorAll('.example-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        if (currentMode === 'ipa') modeWordBtn.click();
        wordInput.value = btn.textContent.trim();
        translate();
    });
});

wordInput.focus();

function copyResult() {
    const text = resultSpanish.textContent;
    if (!text) return;
    navigator.clipboard.writeText(text).then(() => {
        const btn = document.getElementById('copyBtnText');
        btn.textContent = '¡Copiado!';
        setTimeout(() => { btn.textContent = 'Copiar'; }, 2000);
    }).catch(() => {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        const btn = document.getElementById('copyBtnText');
        btn.textContent = '¡Copiado!';
        setTimeout(() => { btn.textContent = 'Copiar'; }, 2000);
    });
}

function getVoices() {
    return new Promise((resolve) => {
        const voices = speechSynthesis.getVoices();
        if (voices.length > 0) { resolve(voices); return; }
        speechSynthesis.onvoiceschanged = () => { resolve(speechSynthesis.getVoices()); };
        setTimeout(() => resolve(speechSynthesis.getVoices()), 3000);
    });
}

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

const MOON_SVG = `<svg class="w-5 h-5 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>`;
const SUN_SVG = `<svg class="w-5 h-5 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707M17.657 17.657l-.707-.707M6.343 6.343l-.707-.707M12 8a4 4 0 100 8 4 4 0 000-8z"/></svg>`;


function toggleTheme() {
    const html = document.documentElement;
    const isDark = html.classList.contains('dark');
    const icon = document.getElementById('themeIcon');
    if (isDark) {
        html.classList.remove('dark');
        localStorage.setItem('theme', 'light');
        icon.innerHTML = MOON_SVG;
    } else {
        html.classList.add('dark');
        localStorage.setItem('theme', 'dark');
        icon.innerHTML = SUN_SVG;
    }
}

(function() {
    const theme = localStorage.getItem('theme') || 'light';
    const icon = document.getElementById('themeIcon');
    if (icon) icon.innerHTML = theme === 'dark' ? SUN_SVG : MOON_SVG;
})();

const PRONUNCIATION_TIPS = {
    'sh': '💡 SH se pronuncia soplando aire entre los dientes — como en "show" o "sheep"',
    'ng': '💡 NG se pronuncia como la N en "banco" o "mango" — un solo sonido nasal',
    'er': '💡 ER es un sonido único del inglés — lengua curvada hacia atrás sin pronunciar la R',
    'z': '💡 Z se pronuncia con la lengua entre los dientes soplando suave — como la pronuncian los españoles',
    'vocales': '💡 Las vocales sin acento se pronuncian suave y corto — no las marques fuerte',
    't_flap': '💡 T entre vocales puede sonar como una R suave — pronunciarla así suena más natural',
    'dch': '💡 DCH — acumula aire en la D y suéltalo fuerte al pronunciar la CH',
};

function showResult(data) {

    updateURL(data.word);

    // Ocultar botón Escuchar en modo IPA
    const audioBtn = document.getElementById('audioBtn');
    if (currentMode === 'ipa') {
        audioBtn.classList.add('hidden');
    } else {
        audioBtn.classList.remove('hidden');
    }
    
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
    showPronunciationGuide(data.spanish || '', data.ipa || '');
}

function showPronunciationGuide(spanish, ipa = '') {
    const guide = document.getElementById('pronunciationGuide');
    const tip = document.getElementById('pronunciationTip');
    if (!guide || !tip) return;

    const text = spanish.toLowerCase();
    const tips = [];

    if (text.includes('dch')) tips.push(PRONUNCIATION_TIPS['dch']);
    if (text.includes('sh')) tips.push(PRONUNCIATION_TIPS['sh']);
    if (text.includes('ng')) tips.push(PRONUNCIATION_TIPS['ng']);
    if (text.includes('er')) tips.push(PRONUNCIATION_TIPS['er']);
    if (ipa.includes('θ') || ipa.includes('ð')) tips.push(PRONUNCIATION_TIPS['z']);

    const vowelsWithoutAccent = (text.match(/[aeiou]/g) || []).length;
    if (vowelsWithoutAccent >= 3) tips.push(PRONUNCIATION_TIPS['vocales']);

    const ipaClean = ipa.replace('ː', '');
    if (/[aeiouɪʊʌɛæɑɔəɝɚ]t[aeiouɪʊʌɛæɑɔəɝɚ]/i.test(ipaClean)) {
        tips.push(PRONUNCIATION_TIPS['t_flap']);
    }

    if (tips.length === 0) {
        guide.classList.add('hidden');
        return;
    }

    tip.innerHTML = tips.join('<br>');
    guide.classList.remove('hidden');
}

// URL compartible — actualizar ?w= al transliterar
function updateURL(word) {
    const url = new URL(window.location);
    url.searchParams.set('w', word);
    window.history.pushState({}, '', url);
}

// Al cargar la página, leer ?w= y transliterar automáticamente
(function() {
    const params = new URLSearchParams(window.location.search);
    const word = params.get('w');
    if (word) {
        wordInput.value = word;
        translate();
    }
})();