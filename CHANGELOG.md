# Changelog

Todos los cambios notables de Jelou están documentados aquí.

## [0.3.1] - 2026-02-19

### Corregido
- Transliteración de "vehicle" y palabras con H muda entre vocales
  - cmu_dictionary: ahora guarda IPA con marcadores ~~STRESS~~ intactos
  - cmu_dictionary: variantes (2) sobreescriben a (1) para usar pronunciación más natural del CMU Dictionary
  - phonetic_engine: secuencia íi→íe e ii→ie para producir diptongo correcto (víekal en lugar de víkal)
- Audio en Chrome: botón "Escuchar" mostraba alert incorrecto
  - getVoices() ahora espera onvoiceschanged antes de verificar disponibilidad
  - Chrome carga voces de forma asíncrona — antes se detectaba erróneamente como Brave
  - Brave y navegadores sin voces siguen mostrando el mensaje correctamente
- Doble acento en palabras largas como "impossible" e "information"
  - arpabet_to_ipa: stress secundario (2) se ignora — en español no existe esa distinción
  - cuando hay múltiples stress primarios (1), se conserva únicamente el último
  - corrige palabras como "information" → informéishan, "communication" → kamiúnakéishan

## [0.3.0] - 2026-02-18

### Añadido
- Modo oscuro con persistencia (localStorage)
- Guía contextual de pronunciación — aparece automáticamente según el resultado
- Estadísticas de la app (126,052 palabras, 100% inglés americano)
- Tagline: "Haz que el inglés hable tu idioma"
- Google Analytics (G-85WDV9YVCP)
- Botón de copiar transliteración
- Audio de pronunciación (Web Speech API)
- Linter configurado (Black + Flake8) — 0 errores

### Corregido
- Sistema de acentos: sílaba tónica correcta (coffee → káfi, hello → jalóu)
- Mensaje de error claro para navegadores sin soporte de audio (Brave)

## [0.2.1] - 2025

### Corregido
- /h/ → 'j' (hello → jalou)
- /j/ → 'i' (yes → ies)
- /dʒ/ contextual (age → eish)
- Sistema de marcadores temporales

## [0.2.0] - 2025

### Añadido
- Aplicación web completa con Flask
- Interfaz responsive moderna con Tailwind CSS
- Deploy en producción (Render)
- Código completamente documentado
- Guías para contribuidores

## [0.1.0] - 2025

### Añadido
- Motor fonético IPA → español
- Integración CMU Dictionary (126,052 palabras)
- CLI con modo palabra y modo IPA directo
- API Python pública
- 34 tests automatizados