from django.contrib import admin

from educa.apps.content.models import Content


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_display_links = ('id',)
