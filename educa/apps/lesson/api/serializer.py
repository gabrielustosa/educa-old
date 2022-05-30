from rest_framework import serializers

from educa.apps.lesson.models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'video', 'video_id', 'order']
