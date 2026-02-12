# Jelou

Jelou es una herramienta que ayuda a hispanohablantes a pronunciar
palabras en inglés usando una representación fonética basada en el español.

No necesitas saber IPA.
Solo introduces la pronunciación y obtienes cómo decirla.

## Ejemplo rápido

Entrada (IPA): θɪŋk

Salida: zink

Eso se lee tal como suena en español.

# Sistema de representación fonética inglés → español

Este documento define las reglas para convertir pronunciación en IPA
(inglés americano estándar) a una representación fonética basada en
un abecedario español extendido, con el objetivo de facilitar la
pronunciación correcta del inglés a personas hispanohablantes sin
necesidad de aprender el Alfabeto Fonético Internacional (IPA).



# Motor de Adaptación Fonética Inglés → Español

## Propósito
Este motor transforma transcripciones en IPA del inglés
en una representación fonética usando caracteres
familiares para hispanohablantes.

No busca precisión lingüística absoluta, sino
facilidad de lectura y pronunciación.

## Entrada
- String en IPA (ej: "θɪŋk", "ʃiː")

## Salida
- String fonético adaptado al español (ej: "zink", "shí")

## No es
- Un traductor
- Un sistema TTS
- Un reemplazo del IPA académico




## Alcance

- Idioma origen: Inglés americano estándar
- Unidad soportada: Palabras individuales
- El sistema no maneja entonación ni frases completas
- No se busca precisión fonética absoluta, sino claridad y utilidad
- El sistema está diseñado como un MVP y puede evolucionar con feedback



## Principios

1. Un símbolo representa un solo sonido
2. La conversión se basa en sonido (IPA), no en ortografía inglesa
3. El sistema debe ser consistente, determinista y predecible
4. La representación final debe ser pronunciable por un hispanohablante sin contexto adicional
5. El sonido /ʃ/ se representa como sh y no como ch
6. Las vocales largas se indican mediante acento gráfico, sin duplicar vocales



## Alfabeto utilizado

### Vocales
a e i o u  
á é í ó ú  (vocal larga)

### Consonantes
b d f g k l m n p r s t  
v z  
ch sh  
w y



## Conversión de consonantes

| IPA | Adaptado | Ejemplo |
| --- | -------- | ------- |
| p   | p        | pen     |
| b   | b        | book    |
| t   | t        | time    |
| d   | d        | day     |
| k   | k        | cat     |
| g   | g        | go      |
| f   | f        | fun     |
| v   | v        | very    |
| θ   | z        | think   |
| ð   | d        | this    |
| s   | s        | see     |
| z   | z        | zoo     |
| ʃ   | sh       | she     |
| tʃ  | ch       | chair   |
| dʒ  | y        | job     |
| m   | m        | man     |
| n   | n        | no      |
| ŋ   | ng       | sing    |
| l   | l        | light   |
| r   | r        | red     |
| w   | w        | water   |
| ʒ   | sh       | vision |





## Conversión de vocales

| IPA | Adaptado | Ejemplo |
| --- | -------- | ------- |
| i   | i        | sit     |
| iː  | í        | see     |
| ɪ   | i        | sit     |
| e   | e | bed   |
| ɛ   | e | head  |
| æ   | a        | cat     |
| ʌ   | a        | but     |
| ɔ   | o        | law     |
| ɑ   | a        | father  |
| ʊ   | u        | book    |
| uː  | ú        | food    |
| ə   | a        | about   |
| ɝ   | er       | bird    |
| ɚ   | er       | better  |




## Diptongos

|| IPA | Adaptado | Ejemplo |
| --- | -------- | ------- |
| eɪ  | ei       | day     |
| aɪ  | ai       | time    |
| ɔɪ  | oi       | boy     |
| aʊ  | au       | now     |
| oʊ  | ou       | go      |



## Reglas de procesamiento

1. Los sonidos compuestos (diptongos y consonantes dobles) tienen
   prioridad sobre sonidos simples.
2. El símbolo ə (schwa) siempre se convierte en "a"
3. Las vocales largas se representan únicamente con acento gráfico
4. No se realizan adaptaciones basadas en ortografía inglesa
5. El sistema no intenta reflejar sílabas, solo sonidos consecutivos.
6. El resultado debe ser legible y pronunciable por un hispanohablante promedio.


## Ejemplos

| Palabra  | IPA         | Resultado |
| -------- | ----------- | --------- |
| she      | ʃiː         | shí       |
| see      | siː         | sí        |
| think    | θɪŋk        | zink      |
| this     | ðɪs         | dis       |
| computer | kəmˈpjuːtər | kompiúter |
| world    | wɝld        | werld     |
| job      | dʒɑb        | yab       |
| enough   | ɪˈnʌf       | ináf      |




## Reglas internas no pedagógicas

| Regla | Motivo |
| ngk → nk | Evitar pronunciación incorrecta tipo "ngk" en español |
| ngg → ng | Evitar duplicación de g tras sonido /ŋ/ (finger, longer) |
| eər → er | Colapsa vocal + schwa + r en una sola vocal r-coloreada (care, hair) |
| aɪər → air | Colapsa diptongo + schwa + r (fire → fair) |
| aʊər → aur | Colapsa diptongo + schwa + r (our → aur, hour → haur) |





## Notas

Este sistema fonético está diseñado para evolucionar.
Las reglas pueden ajustarse a partir de pruebas con usuarios reales y
retroalimentación pedagógica.