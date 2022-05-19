# Generated by Django 4.0.4 on 2022-05-16 17:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='comment',
            field=models.TextField(verbose_name='Comentário'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)], verbose_name='Avaliação'),
        ),
    ]