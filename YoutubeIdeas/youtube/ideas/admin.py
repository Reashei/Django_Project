from django.contrib import admin
from django.utils.html import format_html # importujemy, aby uzyskac tylko link htmlowy
from .models import Idea, Vote

class VoteInline(admin.StackedInline): # pokaze nam voty w zakladce idea
    model = Vote # deklarujemy nazwe modelu, ktory chcemy pokazac


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin): # dziedziczymy po klase z django model.admin
    search_fields = ['title'] # wyszukiwarka search bar
    list_display = ['title', 'status', 'show_youtube_url'] # muszą się zgadzać z zadeklarowanymi polami z models
    list_filter = ['status'] # wlacza liste filtrowania po statusie
    inlines = [VoteInline]

    def show_youtube_url(self, obj):
        if obj.youtube_url is not None:
            return format_html(f'<a href="{obj.youtube_url}" target="_blank">{obj.youtube_url}</a>')
            # target="_blank" uruchomi nam link w nowej karcie
        else:
            return ""

    show_youtube_url.short_description = "Youtube URL" # to nam zmieni nazwe nagłówka na krótszą

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'idea','reason'] # zmieni nam nazwy w panelu admina tj. doda tabele z naglowkami id i reason
    list_filter = ['idea'] # dodajemy filtr wbudowany z django po nagłówki idea
