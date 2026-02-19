# Changelog

Todos los cambios notables de Jelou están documentados aquí.

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
