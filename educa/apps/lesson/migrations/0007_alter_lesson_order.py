# Generated by Django 4.0.5 on 2022-06-10 16:17

from django.db import migrations
import educa.utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0006_alter_lesson_video_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='order',
            field=educa.utils.fields.LessonOrderField(blank=True),
        ),
    ]