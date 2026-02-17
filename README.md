# 🗣️ Jelou

**Pronunciación de inglés hecha simple para hispanohablantes**

Jelou es un motor de adaptación fonética que convierte palabras en inglés a una representación fonética legible, eliminando la barrera del Alfabeto Fonético Internacional (IPA).

[![Tests](https://github.com/N7C0LAS/jelou/actions/workflows/tests.yml/badge.svg)](https://github.com/N7C0LAS/jelou/actions)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/N7C0LAS/jelou/blob/main/LICENSE)
[![Release](https://img.shields.io/github/v/release/N7C0LAS/jelou)](https://github.com/N7C0LAS/jelou/releases)

---

## 🎯 Problema que resuelve

El IPA es preciso pero poco intuitivo. **Jelou traduce símbolos fonéticos complejos a una forma visual cercana al español**, reduciendo la fricción en el aprendizaje de pronunciación.

**Ejemplo:**
- IPA tradicional: `θɪŋk` ❌ (¿Cómo se lee esto?)
- Con Jelou: `zink` ✅ (¡Inmediatamente comprensible!)

---

## 🌐 Aplicación Web

**Usa Jelou desde tu navegador:** [https://jelou.onrender.com](https://jelou.onrender.com)

La aplicación web ofrece:
- 🎨 Interfaz moderna y responsive
- 📱 Funciona en móvil, tablet y desktop
- ⚡ Traducción instantánea de 126,052 palabras
- 🔄 Dos modos: Palabra en inglés + IPA directo
- 🔊 Audio de pronunciación en inglés nativo
- 📋 Botón para copiar el resultado
- 💡 Ejemplos interactivos

**No requiere instalación** - solo abre el link y empieza a usar.

---

## ✨ Características

- 🎯 **126,052 palabras** del CMU Pronouncing Dictionary
- 🔄 **Conversión automática**: palabra → IPA → español
- 🔊 **Audio de pronunciación** en inglés nativo (Web Speech API)
- 📋 **Botón de copiar** resultado al portapapeles
- 🎨 **Modo IPA directo** para usuarios avanzados
- 📦 **Sistema de caché** (descarga una vez, usa offline en CLI)
- 🧪 **34 tests** validando cada componente
- 🐍 **API Python** para integración en otros proyectos
- 🌐 **Aplicación web** accesible desde cualquier dispositivo
- 📝 **Código completamente documentado** para contribuidores
- 🧹 **Código limpio** con Black y Flake8

---

## 🚀 Instalación (CLI)

### Requisitos
- Python 3.9 o superior
- Conexión a internet (solo primera vez)

### Instalación desde código fuente
```bash
# Clonar repositorio
git clone https://github.com/N7C0LAS/jelou.git
cd jelou

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar en modo desarrollo
pip install -e .
```

---

## 💻 Uso

### 1️⃣ Aplicación Web (Recomendado)

**Accede a:** [https://jelou.onrender.com](https://jelou.onrender.com)

- No requiere instalación
- Interfaz intuitiva
- Funciona en cualquier dispositivo
- Audio de pronunciación integrado

### 2️⃣ CLI - Modo palabra
```bash
$ jelou hello
jalou

$ jelou world
werld

$ jelou computer
kampiúter

$ jelou think
zink
```

### 3️⃣ CLI - Modo verbose
```bash
$ jelou hello --verbose
Palabra: hello
IPA:     hʌloʊ
Español: jalou
```

### 4️⃣ CLI - Modo IPA directo

Para usuarios que ya conocen IPA:
```bash
$ jelou --ipa θɪŋk
zink

$ jelou --ipa /ʃiː/
shí
```

### 5️⃣ API Python
```python
from jelou import translate_word, translate_ipa

# Traducir palabra completa
result = translate_word("hello")
print(result)
# {
#     'word': 'hello',
#     'ipa': 'hʌloʊ',
#     'spanish': 'jalou',
#     'found': True
# }

# Convertir IPA directo
spanish = translate_ipa("θɪŋk")
print(spanish)  # "zink"

# Procesar múltiples palabras
from jelou import batch_translate
results = batch_translate(["hello", "world", "think"])
```

---

## 🔤 Sistema de representación

### Sonidos difíciles del inglés

| Sonido IPA | Representación | Ejemplo EN → ES |
|-----------|---------------|-----------------|
| θ | z | think → **zink** |
| ð | d | this → **dis** |
| ʃ | sh | she → **shí** |
| dʒ | y | job → **yab** |
| ŋ | ng | sing → **sing** |
| ɝ | er | world → **werld** |
| ʒ | sh | vision → **vishan** |
| h | j | hello → **jalou** |

### Vocales

| IPA | Español | Ejemplo |
|-----|---------|---------|
| iː | í | see → **sí** |
| ʊ | u | book → **buk** |
| ʌ | a | but → **bat** |
| æ | a | cat → **kat** |

**Documentación completa:** Ver [rules.md](rules.md)

---

## 🧪 Tests
```bash
# Ejecutar todos los tests
pytest

# Tests con detalles
pytest -v

# Tests específicos
pytest tests/test_integration.py
pytest tests/test_arpabet_to_ipa.py
```

**Resultado actual:** ✅ 34/34 tests pasando en Python 3.9-3.12

---

## 🧹 Calidad de código

El proyecto usa **Black** para formateo y **Flake8** para linting:

```bash
# Formatear código
black jelou/ web/

# Verificar linting
flake8 jelou/ web/
```

**Estado actual:** ✅ 0 errores de linting

---

## 📂 Arquitectura del proyecto

### Stack tecnológico

**Backend:**
- Python 3.9+
- Flask (web framework)
- CMU Pronouncing Dictionary

**Frontend:**
- HTML5
- Tailwind CSS
- Vanilla JavaScript
- Web Speech API (audio)

**Infrastructure:**
- GitHub Actions (CI/CD)
- Render (deployment)
- Gunicorn (production server)
- Google Analytics (métricas)

### Estructura de archivos
```
jelou/
├── jelou/                       # Paquete principal
│   ├── cli.py                  # Interfaz de línea de comandos
│   ├── phonetic_engine.py      # Motor IPA → Español
│   ├── arpabet_to_ipa.py       # Conversor ARPABET → IPA
│   ├── cmu_dictionary.py       # Diccionario CMU (126k palabras)
│   └── jelou_api.py            # API pública unificada
├── web/                         # Aplicación web
│   ├── app.py                  # Backend Flask
│   ├── templates/              # HTML
│   └── static/                 # JavaScript
├── tests/                       # 34 tests unitarios + integración
├── rules.md                     # Documentación de reglas fonéticas
└── README.md
```

### Flujo de datos
```
Palabra en inglés
       ↓
CMU Dictionary (ARPABET)
       ↓
Conversor → IPA
       ↓
Motor fonético
       ↓
Representación en español
```

---

## 🎓 Ejemplos prácticos

### Palabras comunes
```bash
jelou hello    # → jalou
jelou goodbye  # → gudbái
jelou please   # → plís
jelou thank    # → zank
jelou water    # → wáter
jelou coffee   # → káfi
```

### Palabras difíciles
```bash
jelou through      # → zrú
jelou thought      # → zot
jelou schedule     # → skéyul
jelou wednesday    # → wénsdei
```

---

## ⚙️ Primera ejecución (CLI)

La primera vez que uses Jelou CLI con una palabra (no IPA), descargará automáticamente el diccionario CMU (~3MB):
```bash
$ jelou hello
📥 Descargando CMU Pronouncing Dictionary...
✅ Diccionario descargado y guardado en: ~/.jelou/cmudict.txt
📖 Cargando diccionario desde: ~/.jelou/cmudict.txt
✅ Diccionario cargado: 126052 palabras
jalou
```

Las siguientes ejecuciones serán **instantáneas** (usa caché local).

---

## 🛣️ Roadmap

### ✅ v0.1.0 - MVP CLI
- Motor fonético IPA → español
- Integración CMU Dictionary
- CLI con dos modos
- API Python pública
- 34 tests automatizados

### ✅ v0.2.0 - Aplicación Web
- Aplicación web completa con Flask
- Interfaz responsive moderna
- Deploy en producción
- Código completamente documentado
- Guías para contribuidores

### ✅ v0.2.1 - Correcciones Fonéticas
- /h/ → 'j' (hello → jalou)
- /j/ → 'i' (yes → ies)
- /dʒ/ contextual (age → eish)
- Sistema de marcadores temporales

### ✅ v0.3.0 - Calidad y UX (Actual)
- Linter configurado (Black + Flake8) — 0 errores
- Google Analytics integrado
- Botón de copiar resultado
- Audio de pronunciación (Web Speech API)

### 🚧 Próximo
- [ ] Soporte para frases completas
- [ ] Sistema de acentos mejorado

### 🔮 Futuro
- [ ] App móvil (iOS/Android)
- [ ] Extensión de navegador
- [ ] API pública de pago

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Ver [CONTRIBUTING.md](CONTRIBUTING.md) para guías detalladas.

### Proceso rápido:

1. Fork el proyecto
2. Crea un branch: `git checkout -b feature/NuevaCaracteristica`
3. Haz commit: `git commit -m 'feat: agregar NuevaCaracteristica'`
4. Push: `git push origin feature/NuevaCaracteristica`
5. Abre un Pull Request

### Guías para contribuir
- ✅ Todos los tests deben pasar
- ✅ Código formateado con Black (`black jelou/ web/`)
- ✅ Sin errores de linting (`flake8 jelou/ web/`)
- ✅ Agregar tests para código nuevo
- ✅ Documentar funciones públicas
- ✅ Código completamente comentado

**El proyecto está completamente documentado** - cada función incluye docstrings con argumentos, retornos y ejemplos.

---

## 📝 Limitaciones actuales

- Solo inglés americano (no británico)
- Solo palabras individuales en CLI (frases próximamente)
- Palabras no encontradas requieren modo `--ipa` manual
- CLI requiere conexión a internet la primera vez

**La aplicación web** no tiene estas limitaciones y funciona completamente online.

---

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles

---

## 🙏 Agradecimientos

- **CMU Pronouncing Dictionary** - Diccionario de pronunciación de código abierto
- Comunidad de hispanohablantes aprendiendo inglés
- Usuarios que aportaron feedback real para mejorar las reglas fonéticas
- Contribuidores del proyecto

---

## 📧 Contacto

**Nicolás Espejo** - Creador de Jelou

- GitHub: [@N7C0LAS](https://github.com/N7C0LAS)
- Proyecto: [github.com/N7C0LAS/jelou](https://github.com/N7C0LAS/jelou)

---

## ⭐ Si Jelou te ayudó

Si este proyecto te resultó útil, considera:
- ⭐ Darle una estrella en GitHub
- 🐛 Reportar bugs o sugerir mejoras
- 🔀 Contribuir con código
- 📢 Compartir con otros estudiantes de inglés

---

**Hecho con ❤️ para hispanohablantes aprendiendo inglés**

**Versión Web:** [jelou.onrender.com](https://jelou.onrender.com)
