from django.contrib import admin

from tile.models import Template, Tile


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):

        # Force only one default template available
        if not Template.objects.filter(is_default=True).exists():
            obj.is_default = True
        elif obj.is_default:
            Template.objects.filter(is_default=True).update(is_default=False)

        obj.save()


@admin.register(Tile)
class TileAdmin(admin.ModelAdmin):
    pass
