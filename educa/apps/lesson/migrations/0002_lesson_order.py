# Generated by Django 4.0.4 on 2022-05-11 12:15

from django.db import migrations
import educa.utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='order',
            field=educa.utils.fields.OrderField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
