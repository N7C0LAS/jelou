// Estado de la aplicación
let currentMode = 'word'; // 'word' o 'ipa'

// Elementos del DOM
const wordInput = document.getElementById('wordInput');
const translateBtn = document.getElementById('translateBtn');
const resultDiv = document.getElementById('result');
const errorDiv = document.getElementById('error');
const loadingDiv = document.getElementById('loading');
const modeWordBtn = document.getElementById('modeWord');
const modeIPABtn = document.getElementById('modeIPA');
const inputLabel = document.getElementById('inputLabel');

// Elementos de resultado
const resultWord = document.getElementById('resultWord');
const resultIPA = document.getElementById('resultIPA');
const resultSpanish = document.getElementById('resultSpanish');
const ipaSection = document.getElementById('ipaSection');
const errorMessage = document.getElementById('errorMessage');

// Cambiar modo
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

// Traducir palabra
async function translate() {
    const word = wordInput.value.trim();
    
    if (!word) {
        showError('Por favor escribe una palabra');
        return;
    }
    
    // Mostrar loading
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

// Mostrar resultado
function showResult(data) {
    hideAll();
    
    resultWord.textContent = data.word;
    resultIPA.textContent = data.ipa || '-';
    resultSpanish.textContent = data.spanish;
    
    // Mostrar/ocultar sección IPA según el modo
    if (currentMode === 'ipa') {
        ipaSection.classList.add('hidden');
    } else {
        ipaSection.classList.remove('hidden');
    }
    
    resultDiv.classList.remove('hidden');
    resultDiv.classList.add('fade-in');
}

// Mostrar error
function showError(message) {
    hideAll();
    errorMessage.textContent = message;
    errorDiv.classList.remove('hidden');
    errorDiv.classList.add('fade-in');
}

// Mostrar loading
function showLoading() {
    hideAll();
    loadingDiv.classList.remove('hidden');
}

// Ocultar todo
function hideAll() {
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    loadingDiv.classList.add('hidden');
}

// Ocultar resultados
function hideResults() {
    hideAll();
}

// Event listeners
translateBtn.addEventListener('click', translate);

wordInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        translate();
    }
});

// Ejemplos
document.querySelectorAll('.example-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Cambiar a modo palabra si está en IPA
        if (currentMode === 'ipa') {
            modeWordBtn.click();
        }
        
        wordInput.value = btn.textContent.trim();
        translate();
    });
});

// Focus en input al cargar
wordInput.focus();
