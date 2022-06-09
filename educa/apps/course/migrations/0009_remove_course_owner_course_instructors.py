# Generated by Django 4.0.5 on 2022-06-06 15:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0008_alter_course_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='owner',
        ),
        migrations.AddField(
            model_name='course',
            name='instructors',
            field=models.ManyToManyField(related_name='courses_created', to=settings.AUTH_USER_MODEL),
        ),
    ]