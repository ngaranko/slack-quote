from django.contrib import admin

from tile.models import Template
from .models import Author, Quote

import tile.service

class QuoteInlineAdmin(admin.TabularInline):
    model = Quote


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ('name', 'active', 'created', 'quote_count', 'last_hit')

    inlines = [
        QuoteInlineAdmin
    ]
    pass


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):

    list_display = ('text', 'has_image', 'has_tile', 'hit_count', 'last_hit')

    list_filter = ('author',)

    def save_model(self, request, obj, form, change):

        obj.save()

        try:
            template = Template.objects.get(is_default=True)
        except (Template.MultipleObjectsReturned, Template.DoesNotExist):
            pass
        else:
            tile.service.create(quote=obj, template=template)

