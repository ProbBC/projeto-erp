# Generated by Django 3.0.3 on 2020-02-21 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20200219_0100'),
    ]

    operations = [
        migrations.AddField(
            model_name='loja',
            name='loja_principal',
            field=models.BooleanField(default=False, verbose_name='Loja Principal'),
        ),
    ]
