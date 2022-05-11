from django.contrib import admin

from educa.apps.lesson.models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_display_links = ('id',)
