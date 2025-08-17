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
        help="Output palette as JSON format"
    )
    parser.add_argument(
        "--css", action="store_true",
        help="Output palette as CSS format"
    )
    parser.add_argument(
        "--show", action="store_true",
        help="Preview the palette in an image"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Get all colors palettes"
    )
    parser.add_argument(
        "-p", "--primary", action="store_true",
        help="Get primary color palette"
    )
    parser.add_argument(
        "-c", "--complementary", action="store_true",
        help="Get complementary color palette"
    )
    parser.add_argument(
        "-a", "--analogous", action="store_true",
        help="Get analogous color palettes"
    )
    parser.add_argument(
        "-t", "--triadic", action="store_true",
        help="Get triadic color palettes"
    )
    
    args = parser.parse_args()
    color = args.color if args.color.startswith("#") else f"#{args.color}"
    is_all = args.all
    is_json = args.json
    is_css = args.css
    is_primary = args.primary
    is_complementary = args.complementary
    is_analogous = args.analogous
    is_triadic = args.triadic
    
    flags = is_all | is_primary | is_complementary | is_analogous | is_triadic

    if not flags:
        output = mpg.get_primary_palette(color)
    else:
        types = []
        if is_all:
            types=None
        else:
            if is_primary: types.append('primary')
            if is_complementary: types.append('complementary')
            if is_analogous: types.append('analogous')
            if is_triadic: types.append('triadic')

        output = mpg.get_palettes(color, types=types)
        
    if is_json:
        import json
        print(json.dumps(output, indent=4))
    elif is_css:
        print(":root {")

        if not flags:
            for k, v in output.items():
                print(f"\t--clr-primary-{k}: {v};")
                if v == color:
                    print(f"\t--clr-primary: var(--clr-primary-{k});")
        else:
            for k, k2 in output.items():
                for v in k2.values():
                    k_low = k.lower()
                    print(f"\t--clr-{k_low}-{k2}: {v};")
                    if v == color:
                        print(f"\t--clr-{k_low}: var(--clr-{k_low}-{k2});")

        print("}")
    else:
        from pprint import pprint
        pprint(output, indent=4)

    if args.show:
        if not flags:
            mpg.preview_palettes(output)
        else:
            for palette in output.values():
                mpg.preview_palettes(palette)

if __name__ == "__main__":
    main()
