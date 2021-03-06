from django.contrib import admin
from django.db.models import Q

from tile.models import Template
from .models import Author, Quote

import tile.service


class QuoteHasEnglishTranslationFilter(admin.SimpleListFilter):
    title = 'translated English'
    parameter_name = 'translated_english'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No')
        )

    def queryset(self, request, queryset):

        if self.value() == 'Yes':
            return queryset.filter(
                Q(text_english__isnull=False) | Q(context_english__isnull=False)
            )

        if self.value() == 'No':
            return queryset.filter(
                Q(text_english__isnull=True) | Q(context_english__isnull=True)
            )

        return queryset


class QuoteInlineAdmin(admin.TabularInline):
    model = Quote


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ('name', 'active', 'created', 'quote_count', 'last_hit')
    list_filter = ('active', )
    search_fields = ('name', )
    inlines = [
        QuoteInlineAdmin
    ]


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):

    list_display = ('text', 'has_image', 'has_tile', 'hit_count', 'last_hit')
    list_filter = ('active', QuoteHasEnglishTranslationFilter, 'author')
    search_fields = ('text', 'context', 'author__name')

    def save_model(self, request, obj, form, change):

        obj.save()

        try:
            template = Template.objects.get(is_default=True)
        except (Template.MultipleObjectsReturned, Template.DoesNotExist):
            pass
        else:

            # Generate tile in native language
            tile.service.create(quote=obj, template=template, english=False)

            # Generate tile in english translation
            tile.service.create(quote=obj, template=template, english=True)
