# 🗣️ Jelou

**Pronunciación de inglés hecha simple para hispanohablantes**

Jelou es un motor de adaptación fonética que convierte palabras en inglés a una representación fonética legible, eliminando la barrera del Alfabeto Fonético Internacional (IPA).

[![Tests](https://github.com/N7C0LAS/jelou/actions/workflows/tests.yml/badge.svg)](https://github.com/N7C0LAS/jelou/actions)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/N7C0LAS/jelou/blob/main/LICENSE)
[![Release](https://img.shields.io/github/v/release/N7C0LAS/jelou)](https://github.com/N7C0LAS/jelou/releases)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
---

## 🎯 Problema que resuelve

El IPA es preciso pero poco intuitivo. **Jelou traduce símbolos fonéticos complejos a una forma visual cercana al español**, reduciendo la fricción en el aprendizaje de pronunciación.

**Ejemplo:**
- IPA tradicional: `θɪŋk` ❌ (¿Cómo se lee esto?)
- Con Jelou: `zink` ✅ (¡Inmediatamente comprensible!)

---

## ✨ Características

- 🎯 **126,052 palabras** del CMU Pronouncing Dictionary
- 🔄 **Conversión automática**: palabra → IPA → español
- 🎨 **Modo IPA directo** para usuarios avanzados
- 📦 **Sistema de caché** (descarga una vez, usa offline)
- 🧪 **34 tests** validando cada componente
- 🐍 **API Python** para integración en otros proyectos

---

## 🚀 Instalación

### Requisitos
- Python 3.9 o superior
- Conexión a internet (solo primera vez)

### Instalación desde código fuente
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/jelou.git
cd jelou

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar en modo desarrollo
pip install -e .
```

---

## 💻 Uso

### 1️⃣ CLI - Modo palabra (recomendado)
```bash
$ jelou hello
halou

$ jelou world
werld

$ jelou computer
kampjúter

$ jelou think
zink
```

### 2️⃣ CLI - Modo verbose
```bash
$ jelou hello --verbose
Palabra: hello
IPA:     hʌloʊ
Español: halou
```

### 3️⃣ CLI - Modo IPA directo

Para usuarios que ya conocen IPA:
```bash
$ jelou --ipa θɪŋk
zink

$ jelou --ipa /ʃiː/
shí
```

### 4️⃣ API Python
```python
from jelou import translate_word, translate_ipa

# Traducir palabra completa
result = translate_word("hello")
print(result)
# {
#     'word': 'hello',
#     'ipa': 'hʌloʊ',
#     'spanish': 'halou',
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

# Cobertura de tests
pytest --cov=jelou
```

**Resultado actual:** ✅ 34/34 tests pasando

---

## 📂 Arquitectura del proyecto
```
jelou/
├── jelou/
│   ├── cli.py                  # Interfaz de línea de comandos
│   ├── phonetic_engine.py      # Motor IPA → Español
│   ├── arpabet_to_ipa.py       # Conversor ARPABET → IPA
│   ├── cmu_dictionary.py       # Diccionario CMU (126k palabras)
│   └── jelou_api.py            # API pública unificada
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
jelou hello    # → halou
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

## ⚙️ Primera ejecución

La primera vez que uses Jelou con una palabra (no IPA), descargará automáticamente el diccionario CMU (~3MB):
```bash
$ jelou hello
📥 Descargando CMU Pronouncing Dictionary...
✅ Diccionario descargado y guardado en: ~/.jelou/cmudict.txt
📖 Cargando diccionario desde: ~/.jelou/cmudict.txt
✅ Diccionario cargado: 126052 palabras
halou
```

Las siguientes ejecuciones serán **instantáneas** (usa caché local).

---

## 🛣️ Roadmap

### ✅ v0.1.0 (Actual - MVP)
- Motor fonético IPA → español
- Integración CMU Dictionary
- CLI con dos modos
- API Python pública
- 34 tests automatizados

### 🚧 v0.2.0 (Próximo)
- [ ] Soporte para frases completas
- [ ] Detección automática de idioma
- [ ] Modo interactivo (REPL)
- [ ] Exportar a archivo (txt, json)

### 🔮 v0.3.0 (Futuro)
- [ ] Generación de audio (TTS)
- [ ] Reconocimiento de voz
- [ ] Aplicación web
- [ ] App móvil (iOS/Android)

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea un branch: `git checkout -b feature/NuevaCaracteristica`
3. Haz commit: `git commit -m 'Agregar NuevaCaracteristica'`
4. Push: `git push origin feature/NuevaCaracteristica`
5. Abre un Pull Request

### Guías para contribuir
- Todos los tests deben pasar
- Agregar tests para código nuevo
- Seguir el estilo de código existente
- Documentar funciones públicas

---

## 📝 Limitaciones actuales

- Solo inglés americano (no británico)
- Solo palabras individuales (no frases completas todavía)
- Palabras no encontradas requieren modo `--ipa` manual
- Requiere conexión a internet la primera vez

---

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles

---

## 🙏 Agradecimientos

- **CMU Pronouncing Dictionary** - Diccionario de pronunciación de código abierto
- Comunidad de hispanohablantes aprendiendo inglés

---

## 📧 Contacto

**Nicolás** - Creador de Jelou

- GitHub: [@tu-usuario](https://github.com/tu-usuario)

---

## ⭐ Si Jelou te ayudó

Si este proyecto te resultó útil, considera:
- ⭐ Darle una estrella en GitHub
- 🐛 Reportar bugs o sugerir mejoras
- 🔀 Contribuir con código
- 📢 Compartir con otros estudiantes de inglés

---

**Hecho con ❤️ para hispanohablantes aprendiendo inglés**
