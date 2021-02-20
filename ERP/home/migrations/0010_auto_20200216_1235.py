# Generated by Django 3.0.3 on 2020-02-16 15:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0009_auto_20200215_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendedor',
            name='telefone2',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Celular'),
        ),
        migrations.AddField(
            model_name='vendedor',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
