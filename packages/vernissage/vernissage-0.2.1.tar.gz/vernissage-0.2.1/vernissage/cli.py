from os import listdir
from os.path import isdir, join

import click

from vernissage.functions import image_processing


@click.group()
def cli():
    pass


@click.command()
@click.argument("input", type=click.File('rb'))
@click.argument("output", type=click.File('wb'))
def image(input, output):
    image_processing(input=input, output=output)


@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path(exists=True))
def batch(input, output):
    if isdir(input):
        files = [join(input, file) for file in listdir(input)]
        for index, file in enumerate(files):
            click.echo(file)
            try:
                image_processing(
                    input=file,
                    output=join(output, f"{index}.jpeg")
                )
            except IsADirectoryError:
                pass
    else:
        click.echo(f"'{input}' is not a directory")


cli.add_command(image)
cli.add_command(batch)
