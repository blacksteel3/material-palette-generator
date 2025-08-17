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
    base_colors = {} if is_css else None
    
    flags = is_all | is_primary | is_complementary | is_analogous | is_triadic

    if not flags:
        output = mpg.get_primary_palette(color, base_colors)
    else:
        types = []
        if is_all:
            types=None
        else:
            if is_primary: types.append('primary')
            if is_complementary: types.append('complementary')
            if is_analogous: types.append('analogous')
            if is_triadic: types.append('triadic')

        output = mpg.get_palettes(color, types=types, base_colors=base_colors)
        
    if is_json:
        import json
        print(json.dumps(output, indent=4))

    elif is_css:
        print(":root {")
        if not flags:
            for code, color in output.items():
                print(f"    --clr-primary-{code}: {color};")
                if color == base_colors['primary']:
                    print(f"    --clr-primary: var(--clr-primary-{code});")
        else:
            for color_type, palette in output.items():
                for code, color in palette.items():
                    ct_low = color_type.lower()
                    print(f"    --clr-{ct_low}-{code}: {color};")
                    if color == base_colors[ct_low]:
                        print(f"    --clr-{ct_low}: var(--clr-{ct_low}-{code});")

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
