# Changelog

Todos los cambios notables de Jelou están documentados aquí.

## [0.4.2] - 2026-02-24

### Mejorado
- Tagline como eslogan independiente: cursiva, centrado, sin tarjeta
- Emojis reemplazados por iconos SVG en toda la interfaz
- Estadísticas: "instantánea" → "< 1s respuesta"
- Botón "Traducir" → "Transliterar" — terminología más precisa
- Ícono de luna en color indigo coherente con el diseño

## [0.4.1] - 2026-02-23

### Corregido
- Guía contextual: CH eliminado por ser redundante para hispanohablantes
- Guía contextual: NG mensaje explica cómo suena en lugar de qué no hacer
- Guía contextual: T flap mensaje general y opcional relacionado con R suave
- Guía contextual: Z solo aparece cuando IPA contiene θ o ð
- Guía contextual: vocales suaves aparece cuando hay 3+ vocales átonas
- Guía contextual: T flap detecta correctamente vocales IPA como ɝ y ɚ

### Mejorado
- Mensajes de pronunciación más claros y coherentes para hispanohablantes

## [0.4.0] - 2026-02-23

### Corregido
- θ y ð siempre generan Z — z nativa inglesa → S (zone→sóun, example→igsámpal)
- dʒ ante consonante → ch (vegetable→véchtabal)
- dʒ ante marcador temporal no se convierte a ch (suggestion→sayéschan)
- Días de la semana usan variante EY → dei (monday→mándei, friday→fráidei)
- saturday con override manual → sáterdei
- Guía contextual de Z solo aparece cuando IPA contiene θ o ð

### Mejorado
- Tests ampliados de 45 a 49 cubriendo todos los casos corregidos

## [0.3.2] - 2026-02-20

### Corregido
- Doble acento en palabras con iː/uː átonas como "communication" y "education"
  - VOWEL_RULES: iː→i y uː→u por defecto (átonas)
  - translate_ipa inserta ~~STRESS~~ automáticamente en vocales largas
  - cmu_dictionary: score con 3 criterios independientes HH > AH0 > UW0
  - Elimina definitivamente el doble acento en palabras largas

### Mejorado
- Tests ampliados de 41 a 46 cubriendo todos los casos corregidos
  - Nuevos tests: vehicle, impossible, communication, education, information

## [0.3.1] - 2026-02-19

### Corregido
- Transliteración de "vehicle" y palabras con H muda entre vocales
- Audio en Chrome: botón "Escuchar" mostraba alert incorrecto
- Doble acento en palabras largas como "impossible" e "information"

## [0.3.0] - 2026-02-18

### Añadido
- Modo oscuro con persistencia (localStorage)
- Guía contextual de pronunciación
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