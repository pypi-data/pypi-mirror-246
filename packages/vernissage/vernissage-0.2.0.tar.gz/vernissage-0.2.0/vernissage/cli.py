import click

from PIL import Image, ImageOps


@click.group()
def cli():
    pass


@click.command()
@click.argument("input", type=click.File('rb'))
@click.argument("output", type=click.File('wb'))
def image(input, output):
    with Image.open(input) as im:
        im.thumbnail(size=(936, 936))
        ImageOps.expand(
            image=im,
            border=72,
            fill=(250, 250, 250)
        ).save(fp=output, format="JPEG")


cli.add_command(image)
