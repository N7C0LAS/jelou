"""
CLI de Jelou.
Convierte palabras inglesas a fonética española desde la terminal.

Uso:
  jelou hello              # modo palabra
  jelou hello --verbose    # muestra IPA intermedio
  jelou --ipa θɪŋk         # modo IPA directo

Autor: Nicolás Espejo
Proyecto: Jelou
Licencia: MIT
"""

import argparse
import sys

from jelou.jelou_api import translate_word, translate_ipa


def main() -> None:
    """Punto de entrada del CLI. Entry point definido en pyproject.toml."""
    parser = argparse.ArgumentParser(
        prog="jelou",
        description="Convierte palabras en inglés a representación fonética para hispanohablantes.",
        epilog="""
Ejemplos:
  jelou hello          # busca en el diccionario
  jelou --ipa θɪŋk     # convierte IPA directo
  jelou --ipa /ʃiː/    # acepta formato /.../
  jelou hello -v       # muestra IPA intermedio
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("input", help="Palabra en inglés o expresión en IPA")
    parser.add_argument("--ipa", action="store_true", help="Tratar entrada como IPA directo")
    parser.add_argument("--verbose", "-v", action="store_true", help="Mostrar IPA intermedio")

    args = parser.parse_args()
    input_text = args.input.strip()

    if args.ipa:
        if input_text.startswith("/") and input_text.endswith("/"):
            input_text = input_text[1:-1]
        result = translate_ipa(input_text)
        if args.verbose:
            print(f"IPA:     {input_text}")
            print(f"Español: {result}")
        else:
            print(result)
        return

    result = translate_word(input_text)

    if not result["found"]:
        print(f"❌ Palabra '{input_text}' no encontrada en el diccionario.", file=sys.stderr)
        print("💡 Usa --ipa si quieres convertir IPA directamente.", file=sys.stderr)
        print("   Ejemplo: jelou --ipa θɪŋk", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(f"Palabra: {result['word']}")
        print(f"IPA:     {result['ipa']}")
        print(f"Español: {result['spanish']}")
    else:
        print(result["spanish"])


if __name__ == "__main__":
    main()