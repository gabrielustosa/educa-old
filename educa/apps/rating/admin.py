from django.contrib import admin

from educa.apps.rating.models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_display_links = ('id',)
