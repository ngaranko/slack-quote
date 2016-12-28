from django.conf import settings
from django.db import models


class Template(models.Model):
    name = models.CharField(max_length=100)
    line_height = models.PositiveIntegerField(default=20)
    char_color = models.CharField(max_length=7, default='000000')
    font = models.FileField(upload_to=settings.STATIC_ROOT + '/uploads/', null=True, blank=True)
    font_size = models.PositiveIntegerField(default=16)
    padding_x = models.IntegerField(default=0)
    padding_y = models.IntegerField(default=0)
    image = models.FileField(upload_to=settings.STATIC_ROOT + '/uploads/', null=True, blank=True)
    is_default = models.BooleanField(default=False)


class Tile(models.Model):
    quote = models.ForeignKey('quote.Quote', related_name='tile')
    template = models.ForeignKey('tile.Template')
    created = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to=settings.STATIC_ROOT + '/uploads/', null=True, blank=True)
    english = models.BooleanField(default=False)
