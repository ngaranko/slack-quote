from django.contrib import admin

from tile.models import Template, Tile


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    pass


@admin.register(Tile)
class TileAdmin(admin.ModelAdmin):
    pass