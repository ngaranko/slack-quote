from django.contrib import admin

from tile.models import Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    pass