# Changelog

Todos los cambios notables de Jelou están documentados aquí.

## [0.5.0] - 2026-02-27

### Corregido
- Audio en Brave: reemplazar alert() por mensaje inline con instrucciones específicas para Brave

## [0.4.9] - 2026-02-25

### Corregido
- Eliminar referencia a tip y_fuerte inexistente en app.js
- Validación de longitud de input (máximo 100 caracteres) en posición correcta
- Icono de tema reemplazado por SVG consistente — elimina emoji ☀️/🌙

### Mejorado
- Estadísticas responsivas en móvil — texto y padding adaptados a pantalla pequeña
- URL compartible ?w= — transliterar hello genera jelou.onrender.com/?w=hello
- og:image agregada para preview en WhatsApp, Twitter y redes sociales

## [0.4.8] - 2026-02-24

### Corregido
- ngkz → ngz: strength transliterado como stréngz en lugar de strénkz
- throughout → zruáut validado como correcto
- quarter → kwórter validado como aceptable (T flap no aplicada al output para evitar regresiones)

## [0.4.7] - 2026-02-24

### Corregido
- T flap: ahora detecta correctamente vocal larga uː antes de T — computer, future,itutor

## [0.4.6] - 2026-02-23

### Mejorado
- Guía de pronunciación: tip DCH agregado para transliteración de dʒ
- Guía de pronunciación: tip y_fuerte eliminado — ya no aplica

## [0.4.5] - 2026-02-22

### Mejorado
- dʒ transliterado como 'dch' en lugar de 'y' — más preciso fonéticamente
- job → dchob, edge → édch, knowledgeable → náladchabal
- Tip de Y detecta 'y' en resultado en lugar de dʒ en IPA
- Tests actualizados para nueva transliteración

## [0.4.4] - 2026-02-20

### Corregido
- Modo IPA directo: ocultar botón Escuchar — no hay palabra original para pronunciar
- Modo IPA directo: limpiar IPA externo automáticamente (slashes, puntos, ː, ˈ, ˌ)
- Usuario puede pegar IPA de cualquier diccionario externo sin errores

## [0.4.3] - 2026-02-19

### Mejorado
- Guía de pronunciación: nuevo tip para Y fuerte (dʒ) — aparece en palabras como "knowledgeable", "job", "june"
- Guía de pronunciación: mensaje de Z actualizado referenciando pronunciación española

## [0.4.2] - 2026-02-18

### Mejorado
- Tagline como eslogan independiente: cursiva, centrado, sin tarjeta
- Emojis reemplazados por iconos SVG en toda la interfaz
- Estadísticas: "instantánea" → "< 1s respuesta"
- Botón "Traducir" → "Transliterar" — terminología más precisa
- Ícono de luna en color indigo coherente con el diseño

## [0.4.1] - 2026-02-17

### Corregido
- Guía contextual: CH eliminado por ser redundante para hispanohablantes
- Guía contextual: NG mensaje explica cómo suena en lugar de qué no hacer
- Guía contextual: T flap mensaje general y opcional relacionado con R suave
- Guía contextual: Z solo aparece cuando IPA contiene θ o ð
- Guía contextual: vocales suaves aparece cuando hay 3+ vocales átonas
- Guía contextual: T flap detecta correctamente vocales IPA como ɝ y ɚ

### Mejorado
- Mensajes de pronunciación más claros y coherentes para hispanohablantes

## [0.4.0] - 2026-02-16

### Corregido
- θ y ð siempre generan Z — z nativa inglesa → S (zone→sóun, example→igsámpal)
- dʒ ante consonante → ch (vegetable→véchtabal)
- dʒ ante marcador temporal no se convierte a ch (suggestion→sayéschan)
- Días de la semana usan variante EY → dei (monday→mándei, friday→fráidei)
- saturday con override manual → sáterdei
- Guía contextual de Z solo aparece cuando IPA contiene θ o ð

### Mejorado
- Tests ampliados de 45 a 49 cubriendo todos los casos corregidos

## [0.3.2] - 2026-02-13

### Corregido
- Doble acento en palabras con iː/uː átonas como "communication" y "education"
  - VOWEL_RULES: iː→i y uː→u por defecto (átonas)
  - translate_ipa inserta ~~STRESS~~ automáticamente en vocales largas
  - cmu_dictionary: score con 3 criterios independientes HH > AH0 > UW0
  - Elimina definitivamente el doble acento en palabras largas

### Mejorado
- Tests ampliados de 41 a 46 cubriendo todos los casos corregidos
  - Nuevos tests: vehicle, impossible, communication, education, information

## [0.3.1] - 2026-02-12

### Corregido
- Transliteración de "vehicle" y palabras con H muda entre vocales
- Audio en Chrome: botón "Escuchar" mostraba alert incorrecto
- Doble acento en palabras largas como "impossible" e "information"

## [0.3.0] - 2026-02-11

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