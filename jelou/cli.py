"""
Interfaz de Línea de Comandos (CLI) de Jelou
=============================================

Este módulo proporciona la interfaz de terminal para usar Jelou.
Soporta dos modos de operación para diferentes casos de uso.

Modos de uso:
-------------
1. MODO PALABRA (por defecto):
   - Usuario escribe palabra en inglés
   - Jelou busca en diccionario CMU
   - Muestra IPA + pronunciación en español
   - Ejemplo: `jelou hello` → "halou"

2. MODO IPA (avanzado):
   - Usuario escribe notación IPA directamente
   - Jelou convierte a español
   - No requiere diccionario
   - Ejemplo: `jelou --ipa θɪŋk` → "zink"

Ejemplos de uso:
----------------
```bash
# Modo palabra básico
$ jelou hello
halou

# Modo palabra verbose (muestra IPA)
$ jelou hello --verbose
Palabra: hello
IPA:     hʌloʊ
Español: halou

# Modo IPA directo
$ jelou --ipa θɪŋk
zink

# IPA con slashes opcionales
$ jelou --ipa /ʃiː/
shí
```

Autor: Nicolás Espejo
Proyecto: Jelou
Licencia: MIT
"""

import argparse
import sys

from jelou.jelou_api import translate_word, translate_ipa

# =========================
# FUNCIÓN PRINCIPAL
# =========================


def main() -> None:
    """
    Punto de entrada del CLI de Jelou.

    Procesa argumentos de línea de comandos, ejecuta la traducción
    correspondiente y muestra resultados al usuario.

    Flujo de ejecución:
    -------------------
    1. Parsear argumentos de línea de comandos
    2. Determinar modo (palabra o IPA)
    3. Ejecutar traducción correspondiente
    4. Formatear y mostrar resultado
    5. Manejar errores apropiadamente

    Exit codes:
    -----------
    0: Éxito
    1: Error (palabra no encontrada, entrada inválida, etc.)

    Note:
        Esta función es el entry point definido en pyproject.toml:
        [project.scripts]
        jelou = "jelou.cli:main"
    """
    # ==================
    # CONFIGURAR PARSER
    # ==================

    parser = argparse.ArgumentParser(
        prog="jelou",
        description=(
            "Convierte palabras en inglés a representación fonética"
            " legible para hispanohablantes."
        ),
        epilog="""
Ejemplos de uso:
  jelou hello          # Busca 'hello' en el diccionario
  jelou --ipa θɪŋk     # Convierte IPA directo
  jelou --ipa /ʃiː/    # También acepta formato /.../
  jelou hello -v       # Modo verbose (muestra IPA intermedio)
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,  # noqa: E501
    )

    # Argumento posicional: la palabra o IPA a traducir
    parser.add_argument(
        "input",
        help="Palabra en inglés o expresión en IPA",
    )

    # Flag: --ipa para modo IPA directo
    parser.add_argument(
        "--ipa",
        action="store_true",
        help="Tratar entrada como IPA directo (sin buscar en diccionario)",
    )

    # Flag: --verbose para mostrar información detallada
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Mostrar información detallada (IPA intermedio)",
    )

    # Parsear argumentos
    args = parser.parse_args()

    # Limpiar entrada (remover espacios en blanco)
    input_text = args.input.strip()

    # ==================
    # MODO IPA DIRECTO
    # ==================

    if args.ipa:
        # Limpiar slashes opcionales del formato /IPA/
        # Algunos usuarios están acostumbrados a escribir IPA entre slashes
        if input_text.startswith("/") and input_text.endswith("/"):
            input_text = input_text[1:-1]

        # Convertir IPA a español
        result = translate_ipa(input_text)

        # Mostrar resultado según modo (verbose o simple)
        if args.verbose:
            print(f"IPA:     {input_text}")
            print(f"Español: {result}")
        else:
            print(result)

        # Salir exitosamente
        return

    # ==================
    # MODO PALABRA
    # ==================

    # Traducir palabra usando diccionario CMU
    result = translate_word(input_text)

    # Verificar si la palabra se encontró
    if not result["found"]:
        # Palabra no encontrada: mostrar error y sugerencia
        print(
            f"❌ Palabra '{input_text}' no encontrada en el diccionario.",
            file=sys.stderr,
        )
        print("💡 Usa --ipa si quieres convertir IPA directamente.", file=sys.stderr)
        print("   Ejemplo: jelou --ipa θɪŋk", file=sys.stderr)

        # Salir con código de error
        sys.exit(1)

    # Palabra encontrada: mostrar resultado según modo
    if args.verbose:
        # Modo verbose: mostrar palabra, IPA y español
        print(f"Palabra: {result['word']}")
        print(f"IPA:     {result['ipa']}")
        print(f"Español: {result['spanish']}")
    else:
        # Modo simple: solo mostrar pronunciación en español
        print(result["spanish"])


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    """
    Permite ejecutar el módulo directamente:
    python -m jelou.cli hello

    En producción, se usa el entry point del pyproject.toml:
    jelou hello
    """
    main()
