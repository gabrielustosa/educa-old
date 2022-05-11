# Generated by Django 4.0.4 on 2022-05-11 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0001_initial'),
        ('content', '0003_remove_video_owner_remove_content_module'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Video',
        ),
        migrations.AddField(
            model_name='content',
            name='lesson',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='lesson.lesson'),
            preserve_default=False,
        ),
    ]