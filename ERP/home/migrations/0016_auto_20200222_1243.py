# Generated by Django 3.0.3 on 2020-02-22 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_loja_loja_principal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loja',
            name='loja_principal',
            field=models.BooleanField(default=None, null=True, verbose_name='Loja Principal'),
        ),
    ]
