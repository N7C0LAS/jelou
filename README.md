# Jelou

**Haz que el inglés hable tu idioma.**

Jelou es un motor de transliteración fonética Inglés → Español para hispanohablantes. Convierte palabras inglesas a una representación pronunciable usando el alfabeto español, eliminando la barrera del Alfabeto Fonético Internacional (IPA).

[![Tests](https://github.com/N7C0LAS/jelou/actions/workflows/tests.yml/badge.svg)](https://github.com/N7C0LAS/jelou/actions)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/N7C0LAS/jelou/blob/main/LICENSE)
[![Version](https://img.shields.io/badge/version-0.4.9-indigo)](https://github.com/N7C0LAS/jelou/releases)

---

## El problema

El IPA es preciso pero poco intuitivo para el hispanohablante promedio. Ver `θɪŋk` no le dice a nadie cómo pronunciar *think*.

Jelou resuelve eso:

```
think  →  zink
hello  →  jalóu
water  →  wóter
schedule  →  skéchual
```

Sin símbolos raros. Sin conocimiento previo de fonética. Solo lees y pronuncias.

---

## Aplicación web

**[jelou.onrender.com](https://jelou.onrender.com)**

- Interfaz responsive — funciona en móvil, tablet y desktop
- 126,052 palabras disponibles (CMU Pronouncing Dictionary)
- Modo palabra en inglés + modo IPA directo
- Audio de pronunciación en inglés nativo
- Guía contextual de pronunciación por resultado
- URL compartible — `jelou.onrender.com/?w=hello`
- Modo oscuro
- Sin instalación requerida

---

## Instalación (CLI y API)

### Requisitos

- Python 3.9 o superior
- Conexión a internet (solo la primera vez, para descargar el diccionario CMU)

### Desde código fuente

```bash
git clone https://github.com/N7C0LAS/jelou.git
cd jelou
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

---

## Uso

### Aplicación web

Accede a [jelou.onrender.com](https://jelou.onrender.com) — no requiere instalación.

### CLI

```bash
# Transliteración básica
jelou think
# → zink

# Con verbose (muestra IPA)
jelou hello --verbose
# Palabra: hello
# IPA:     hʌloʊ
# Español: jalóu

# Modo IPA directo
jelou --ipa θɪŋk
# → zink
```

### API Python

```python
from jelou import translate_word, translate_ipa, batch_translate

# Palabra completa
result = translate_word("hello")
# {'word': 'hello', 'ipa': 'hʌloʊ', 'spanish': 'jalóu', 'found': True}

# IPA directo
spanish = translate_ipa("θɪŋk")
# 'zink'

# Múltiples palabras
results = batch_translate(["hello", "world", "think"])
```

### API REST

```bash
POST /api/translate
Content-Type: application/json

{"word": "hello", "mode": "word"}

# Respuesta
{"success": true, "word": "hello", "ipa": "hʌloʊ", "spanish": "jalóu", "found": true}
```

---

## Sistema de transliteración

### Sonidos especiales

| IPA | Español | Ejemplo |
|-----|---------|---------|
| θ / ð | z | think → **zink**, this → **zís** |
| ʃ / ʒ | sh | she → **shí**, vision → **víshan** |
| dʒ | dch | job → **dchab**, edge → **édch** |
| tʃ | ch | chair → **cher**, church → **chérch** |
| h | j | hello → **jalóu** |
| ŋ | ng | sing → **síng** |
| ɝ / ɚ | er | water → **wóter** |
| z nativa | s | zone → **sóun** |

### Sistema de acento

- La sílaba tónica se marca con acento gráfico español
- Se usa el último stress primario del CMU (resuelve casos como *information*)
- El stress secundario se ignora

### Correcciones contextuales

| Patrón | Corrección | Ejemplo |
|--------|------------|---------|
| ngk | nk | think → zínk |
| ngkz | ngz | strength → stréngz |
| ngg | ng | — |
| zs | s | clothes → klóus |

---

## Arquitectura

```
jelou/
├── jelou/
│   ├── __init__.py          # API pública, versión actual
│   ├── jelou_api.py         # translate_word(), translate_ipa(), batch_translate()
│   ├── phonetic_engine.py   # Motor IPA → español
│   ├── cmu_dictionary.py    # Integración CMU Dictionary
│   ├── arpabet_to_ipa.py    # Conversor ARPABET → IPA
│   └── cli.py               # CLI: jelou <palabra> --verbose
├── web/
│   ├── app.py               # Backend Flask + API REST
│   ├── templates/
│   │   ├── index.html       # Frontend principal
│   │   ├── 404.html         # Página de error 404
│   │   └── 500.html         # Página de error 500
│   └── static/
│       ├── app.js           # Lógica frontend
│       ├── favicon.svg      # Favicon
│       └── og-image.png     # Imagen para redes sociales
└── tests/                   # 49 tests automatizados
```

### Stack

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3.9+ + Flask |
| Motor fonético | CMU Pronouncing Dictionary (126,052 palabras) |
| Frontend | HTML + Tailwind CSS + Vanilla JavaScript |
| Audio | Web Speech API |
| Deploy | Render (auto-deploy desde GitHub) |
| CI/CD | GitHub Actions |
| Servidor | Gunicorn |

### Flujo de datos

```
Palabra en inglés
       ↓
CMU Dictionary → ARPABET
       ↓
Conversor → IPA con marcadores de stress
       ↓
Motor fonético (phonetic_engine.py)
       ↓
Transliteración en español con acento gráfico
```

---

## Tests

```bash
# Todos los tests
pytest

# Con detalle
pytest -v

# Suite específica
pytest tests/test_integration.py
pytest tests/test_phonetic_engine.py
pytest tests/test_web.py
```

**Estado actual:** 49/49 tests pasando en Python 3.9–3.12.

---

## Calidad de código

```bash
# Formatear
black jelou/ web/

# Linting
flake8 jelou/ web/
```

Estado: 0 errores de linting.

---

## Contribuir

Las contribuciones son bienvenidas. Ver [CONTRIBUTING.md](CONTRIBUTING.md) para guías detalladas.

```bash
git checkout -b feature/nueva-feature
git commit -m "feat: descripción del cambio"
git push origin feature/nueva-feature
# Abrir Pull Request
```

Requisitos para PR:
- Todos los tests deben pasar (`pytest`)
- Código formateado con Black
- Sin errores de Flake8
- Tests nuevos para funcionalidad nueva
- Funciones públicas documentadas con docstrings

---

## Roadmap

### Completado

- **v0.1.0** — Motor fonético + CLI + API Python + 34 tests
- **v0.2.0** — Aplicación web Flask + deploy en Render
- **v0.3.0** — Modo oscuro + guía contextual de pronunciación + sistema de acentos
- **v0.4.x** — Precisión fonética (dʒ→dch, θ/ð→z) + URL compartible + og:image + responsivo móvil

### Próximo — v0.5.0

- Historial de búsquedas recientes
- GitHub Release actualizado

### Futuro

- Soporte para frases completas
- Extensión de navegador
- App móvil nativa

---

## Limitaciones

- Solo inglés americano (no británico)
- Solo palabras individuales (frases en desarrollo)
- Palabras no encontradas en el diccionario requieren modo `--ipa`
- CLI requiere internet la primera vez (descarga del diccionario CMU ~3MB)

---

## Licencia

MIT — ver [LICENSE](LICENSE) para detalles.

---

## Créditos

- **CMU Pronouncing Dictionary** — diccionario de pronunciación de código abierto de Carnegie Mellon University
- Comunidad de hispanohablantes aprendiendo inglés

---

**Nicolás Espejo** · [github.com/N7C0LAS](https://github.com/N7C0LAS)