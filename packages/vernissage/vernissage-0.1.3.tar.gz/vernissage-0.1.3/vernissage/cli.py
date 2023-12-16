from argparse import ArgumentParser

from PIL import Image, ImageOps


def cli():

    parser = ArgumentParser()
    parser.add_argument("input_file", help="")
    parser.add_argument("output_file", help="")
    args = parser.parse_args()

    with Image.open(args.input_file) as im:
        im.thumbnail(size=(936, 936))
        ImageOps.expand(
            image=im,
            border=72,
            fill=(250, 250, 250)
        ).save(fp=args.output_file, format="JPEG")


if __name__ == "__main__":
    cli()
