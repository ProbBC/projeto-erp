# Generated by Django 3.0.3 on 2020-02-19 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20200219_0040'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='produto',
            constraint=models.UniqueConstraint(fields=('codigo', 'loja'), name='codigo_unico'),
        ),
        migrations.AddConstraint(
            model_name='produto',
            constraint=models.UniqueConstraint(fields=('gtin', 'loja'), name='gtin_unico'),
        ),
    ]
