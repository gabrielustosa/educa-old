# Generated by Django 4.0.5 on 2022-06-21 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0011_alter_lesson_video_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video_duration',
            field=models.FloatField(null=True),
        ),
    ]