from django.contrib import admin

from .models import Author, Quote


class QuoteInlineAdmin(admin.TabularInline):
    model = Quote


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        QuoteInlineAdmin
    ]
    pass


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    pass

# Register your models here.
