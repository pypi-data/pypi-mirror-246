from PIL import Image, ImageOps


def image_processing(input: str, output: str):
    with Image.open(input) as im:
        im.thumbnail(size=(936, 936))
        ImageOps.expand(
            image=im,
            border=72,
            fill=(250, 250, 250)
        ).save(fp=output)
