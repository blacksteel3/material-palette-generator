import argparse
import material_palette_generator as mpg

def main():
    parser = argparse.ArgumentParser(
        description="Generate Material Design color palette from a base hex color."
    )
    parser.add_argument(
        "color",
        help="Base color in hex format (e.g. #3f51b5)"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output palette as JSON instead of plain text"
    )
    parser.add_argument(
        "--primary", action="store_true",
        help="Get primary color"
    )
    parser.add_argument(
        "--complementary", action="store_true",
        help="Get complementary color"
    )
    parser.add_argument(
        "--analogous", action="store_true",
        help="Get analogous color"
    )
    parser.add_argument(
        "--triadic", action="store_true",
        help="Get triadic color"
    )
    
    args = parser.parse_args()
    flags = flags = args.primary or args.complementary or args.analogous or args.triadic

    if not flags:
        output = mpg.get_primary_palette(args.color)
    else:
        types = []
        if args.primary: types.append('primary')
        if args.complementary: types.append('complementary')
        if args.analogous: types.append('analogous')
        if args.triadic: types.append('triadic')

        output = mpg.get_palettes(args.color, types=types)
        
    if args.json:
        import json
        print(json.dumps(output, indent=4))
    else:
        from pprint import pprint
        pprint(output, indent=4)

if __name__ == "__main__":
    main()
