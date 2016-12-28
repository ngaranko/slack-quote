import uuid

import io
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from django.core.files.base import ContentFile


def _get_lines(text, char_limit):
    lines = []
    line = ""

    for word in text.split(' '):

        if len(line) + len(word) > char_limit:
            lines.append(line)
            line = ""

        line += ' {}'.format(word)

    lines.append(line)

    return lines


def create(quote, template, english):

    img = Image.open(template.image)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(str(template.font), template.font_size)
    image_width, image_height = img.size

    char_width, char_height = draw.textsize("H", font)

    # Calculate amount chars per line available
    char_limit = int(image_width / char_width - template.padding_x / char_width)

    # Convert long string in small lines
    lines = _get_lines(quote.get_text(english=english), char_limit)

    # Calculate text Y-position aligned by center
    padding_y = image_height * 0.5 - template.line_height * len(lines) * 0.5 + template.padding_y * 0.5

    for line in lines:
        line_width, _ = draw.textsize(line, font)

        # Calculate text X-position aligned by center
        text_x = image_width * 0.5 - line_width * 0.5

        draw.text((text_x, padding_y), line, (66, 00, 00), font=font)

        padding_y += template.line_height

    output = io.BytesIO()
    img.save(output, format='JPEG')

    tile, _ = quote.tile.get_or_create(template=template, english=english)
    tile.image.save('{}.jpg'.format(uuid.uuid4()), ContentFile(output.getvalue()))

    return tile
