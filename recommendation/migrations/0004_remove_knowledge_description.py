# Generated by Django 5.0.6 on 2024-07-12 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0003_remove_knowledgerule_knowledges_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='knowledge',
            name='description',
        ),
    ]
