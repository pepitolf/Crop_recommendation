# Generated by Django 5.0.6 on 2024-07-25 03:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0007_alter_knowledgefuzzyvalue_fuzzy_set_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='knowledge',
            name='crop',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='recommendation.crop'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='knowledgefuzzyvalue',
            name='knowledge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommendation.knowledge'),
        ),
    ]