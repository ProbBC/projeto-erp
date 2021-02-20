# Generated by Django 3.0.3 on 2020-02-15 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20191126_2046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome Completo')),
                ('email', models.EmailField(blank=True, max_length=110, null=True, verbose_name='Email')),
                ('codigo', models.CharField(blank=True, max_length=30, null=True, verbose_name='Código')),
                ('fantasia', models.CharField(blank=True, max_length=80, null=True, verbose_name='Nome Fantasia')),
                ('tipo', models.CharField(choices=[('J', 'Jurídica'), ('F', 'Física'), ('E', 'Estrangeiro')], default='J', max_length=1, verbose_name='Tipo da Pessoa')),
                ('cnpj', models.CharField(blank=True, max_length=18, null=True, verbose_name='CNPJ')),
                ('cpf', models.CharField(blank=True, max_length=14, null=True, verbose_name='CPF')),
                ('rg', models.CharField(blank=True, max_length=20, null=True, verbose_name='RG')),
                ('cep', models.CharField(blank=True, max_length=9, null=True, verbose_name='CEP')),
                ('cidade', models.CharField(blank=True, max_length=60, null=True, verbose_name='Cidade')),
                ('uf', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, null=True, verbose_name='UF')),
                ('endereco', models.CharField(blank=True, max_length=90, null=True, verbose_name='Endereço/Rua')),
                ('numero', models.PositiveIntegerField(blank=True, null=True, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, max_length=90, null=True, verbose_name='Complemento')),
                ('bairro', models.CharField(blank=True, max_length=90, null=True, verbose_name='Bairro')),
                ('telefone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefone/Celular')),
            ],
        ),
        migrations.AlterField(
            model_name='estoque',
            name='quantidade',
            field=models.PositiveIntegerField(verbose_name='Quantidade'),
        ),
    ]