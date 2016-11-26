from django.contrib import admin

from .models import Author, Quote


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

    list_display = ('author', 'text', 'context', 'has_image', 'has_tile', 'hit_count', 'last_hit')

    list_filter = ('author',)

    pass

# Register your models here.
