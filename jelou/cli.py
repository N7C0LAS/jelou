"""
Interfaz de línea de comandos para Jelou.

Soporta dos modos:
1. Palabra en inglés → busca en diccionario → IPA → español
2. IPA directo → español
"""

import argparse
import sys

from jelou.jelou_api import translate_word, translate_ipa


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="jelou",
        description="Convierte palabras en inglés a representación fonética legible para hispanohablantes.",
        epilog="Ejemplos:\n"
               "  jelou hello          # Busca 'hello' en el diccionario\n"
               "  jelou --ipa θɪŋk     # Convierte IPA directo\n"
               "  jelou --ipa /ʃiː/    # También acepta formato /.../"
    )

    parser.add_argument(
        "input",
        help="Palabra en inglés o expresión en IPA",
    )
    
    parser.add_argument(
        "--ipa",
        action="store_true",
        help="Tratar entrada como IPA directo (sin buscar en diccionario)",
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mostrar información detallada (IPA intermedio)",
    )

    args = parser.parse_args()

    input_text = args.input.strip()

    # Modo IPA directo
    if args.ipa:
        # Limpiar slashes si están presentes
        if input_text.startswith("/") and input_text.endswith("/"):
            input_text = input_text[1:-1]
        
        result = translate_ipa(input_text)
        
        if args.verbose:
            print(f"IPA:     {input_text}")
            print(f"Español: {result}")
        else:
            print(result)
        
        return

    # Modo palabra (por defecto)
    result = translate_word(input_text)
    
    if not result['found']:
        print(f"❌ Palabra '{input_text}' no encontrada en el diccionario.", file=sys.stderr)
        print(f"💡 Usa --ipa si quieres convertir IPA directamente.", file=sys.stderr)
        sys.exit(1)
    
    if args.verbose:
        print(f"Palabra: {result['word']}")
        print(f"IPA:     {result['ipa']}")
        print(f"Español: {result['spanish']}")
    else:
        print(result['spanish'])


if __name__ == "__main__":
    main()
