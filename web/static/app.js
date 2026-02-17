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
 * 
 * Actualiza:
 * - Estado global (currentMode)
 * - Estilos de botones
 * - Etiqueta y placeholder del input
 * - Limpia resultados anteriores
 */
modeWordBtn.addEventListener('click', () => {
    currentMode = 'word';
    
    // Actualizar estilos de botones
    modeWordBtn.classList.remove('bg-gray-200', 'text-gray-700');
    modeWordBtn.classList.add('bg-indigo-600', 'text-white');
    modeIPABtn.classList.remove('bg-indigo-600', 'text-white');
    modeIPABtn.classList.add('bg-gray-200', 'text-gray-700');
    
    // Actualizar UI
    inputLabel.textContent = 'Escribe una palabra en inglés:';
    wordInput.placeholder = 'Ejemplo: hello';
    wordInput.value = '';
    hideResults();
});

/**
 * Cambia al modo "IPA directo"
 * 
 * Actualiza:
 * - Estado global (currentMode)
 * - Estilos de botones
 * - Etiqueta y placeholder del input
 * - Limpia resultados anteriores
 */
modeIPABtn.addEventListener('click', () => {
    currentMode = 'ipa';
    
    // Actualizar estilos de botones
    modeIPABtn.classList.remove('bg-gray-200', 'text-gray-700');
    modeIPABtn.classList.add('bg-indigo-600', 'text-white');
    modeWordBtn.classList.remove('bg-indigo-600', 'text-white');
    modeWordBtn.classList.add('bg-gray-200', 'text-gray-700');
    
    // Actualizar UI
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
 * Manejo de errores:
 * ------------------
 * - Entrada vacía → Error de validación
 * - Palabra no encontrada → Error con sugerencia
 * - Error de red → Error de conexión
 * - Error del servidor → Error genérico
 * 
 * @async
 * @returns {Promise<void>}
 */
async function translate() {
    // Obtener y limpiar entrada
    const word = wordInput.value.trim();
    
    // Validación: entrada no puede estar vacía
    if (!word) {
        showError('Por favor escribe una palabra');
        return;
    }
    
    // Mostrar indicador de carga
    showLoading();
    
    try {
        // Hacer petición POST a la API
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
        
        // Parsear respuesta JSON
        const data = await response.json();
        
        // Procesar respuesta según éxito
        if (data.success) {
            // Verificar si la palabra se encontró (solo en modo palabra)
            if (currentMode === 'word' && !data.found) {
                showError(`La palabra "${word}" no se encontró en el diccionario. Intenta usar el modo IPA.`);
            } else {
                showResult(data);
            }
        } else {
            // Error retornado por la API
            showError(data.error || 'Error desconocido');
        }
        
    } catch (error) {
        // Error de red o parsing
        showError('Error de conexión. Por favor intenta de nuevo.');
        console.error('Error:', error);
    }
}


// =========================
// FUNCIONES DE UI
// =========================

/**
 * Muestra el resultado de la traducción.
 * 
 * @param {Object} data - Datos de respuesta de la API
 * @param {string} data.word - Palabra original
 * @param {string} data.ipa - Pronunciación IPA
 * @param {string} data.spanish - Pronunciación en español
 * @param {string} data.mode - Modo usado ('word' o 'ipa')
 */
function showResult(data) {
    // Ocultar otros estados
    hideAll();
    
    // Poblar elementos con datos
    resultWord.textContent = data.word;
    resultIPA.textContent = data.ipa || '-';
    resultSpanish.textContent = data.spanish;
    
    // Mostrar/ocultar sección IPA según el modo
    // En modo IPA directo, no tiene sentido mostrar el IPA otra vez
    if (currentMode === 'ipa') {
        ipaSection.classList.add('hidden');
    } else {
        ipaSection.classList.remove('hidden');
    }
    
    // Mostrar resultado con animación
    resultDiv.classList.remove('hidden');
    resultDiv.classList.add('fade-in');
}

/**
 * Muestra un mensaje de error.
 * 
 * @param {string} message - Mensaje de error a mostrar
 */
function showError(message) {
    // Ocultar otros estados
    hideAll();
    
    // Establecer mensaje
    errorMessage.textContent = message;
    
    // Mostrar error con animación
    errorDiv.classList.remove('hidden');
    errorDiv.classList.add('fade-in');
}

/**
 * Muestra el indicador de carga.
 * 
 * Se muestra mientras se espera la respuesta de la API.
 */
function showLoading() {
    hideAll();
    loadingDiv.classList.remove('hidden');
}

/**
 * Oculta todos los contenedores de estado.
 * 
 * Útil antes de mostrar un nuevo estado para evitar
 * que múltiples estados sean visibles simultáneamente.
 */
function hideAll() {
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    loadingDiv.classList.add('hidden');
}

/**
 * Oculta los resultados.
 * Alias de hideAll() para claridad semántica.
 */
function hideResults() {
    hideAll();
}


// =========================
// EVENT LISTENERS
// =========================

/**
 * Click en botón "Traducir"
 */
translateBtn.addEventListener('click', translate);

/**
 * Enter en el input
 * Permite traducir presionando Enter sin necesidad de hacer click
 */
wordInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        translate();
    }
});

/**
 * Click en botones de ejemplo
 * 
 * Funcionalidad:
 * --------------
 * 1. Si está en modo IPA, cambiar automáticamente a modo palabra
 * 2. Poblar input con la palabra del ejemplo
 * 3. Ejecutar traducción automáticamente
 */
document.querySelectorAll('.example-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Si está en modo IPA, cambiar a modo palabra
        if (currentMode === 'ipa') {
            modeWordBtn.click();
        }
        
        // Poblar input con el texto del botón
        wordInput.value = btn.textContent.trim();
        
        // Traducir automáticamente
        translate();
    });
});


// =========================
// INICIALIZACIÓN
// =========================

/**
 * Auto-focus en el input al cargar la página
 * Mejora UX permitiendo que el usuario empiece a escribir inmediatamente
 */
wordInput.focus();

// =========================
// COPIAR RESULTADO
// =========================

/**
 * Copia la pronunciación en español al portapapeles.
 * Muestra feedback visual confirmando la acción.
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
        // Fallback para navegadores sin soporte clipboard API
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
