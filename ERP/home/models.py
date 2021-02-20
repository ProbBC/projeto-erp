from localflavor.br.br_states import STATE_CHOICES
from django.db import models


class Loja(models.Model):
    nome = models.CharField('Nome da Loja', max_length=100, null=True, blank=True)
    cnpj = models.CharField('CNPJ da Loja', max_length=18, null=True, blank=True)
    user = models.ForeignKey('accounts.CustomUser', editable=True, on_delete=models.CASCADE)
    loja_principal = models.BooleanField('Loja Principal', null=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['loja_principal', 'user'],
                                    name='loja_principal_unica')
        ]


class Produto(models.Model):
    SITUACAO_CHOICES = [('A', 'Ativo'), ('I', 'Inativo')]
    CONDICAO_CHOICES = [('NE', 'Não Especificado'),
                        ('NO', 'Novo'), ('US', 'Usado')]

    descricao = models.CharField('Descrição', max_length=60)
    preco_venda = models.DecimalField('Preço de Venda', max_digits=10, decimal_places=2)
    codigo = models.CharField('Código', max_length=30)
    situacao = models.CharField('Situação', max_length=1,
                                choices=SITUACAO_CHOICES,
                                default='A')  # (A - Ativo, I - Inativo)
    gtin = models.CharField('Código GTIN', max_length=14, null=True, blank=True)
    data_validade = models.DateField('Data de Validade', blank=True, null=True)
    condicao = models.CharField('Condição', max_length=2, choices=CONDICAO_CHOICES,
                                default='NO')
    # total_estoque é calculado automaticamente quando um lançamento de estoque
    # é realizado. (método save() e delete() do Model Estoque)
    total_estoque = models.IntegerField('Estoque', editable=False, default=0)
    data_cadastro = models.DateTimeField('Data do cadastro', editable=False, auto_now_add=True)
    # user = models.ForeignKey('accounts.CustomUser', editable=True, on_delete=models.CASCADE)
    loja = models.ForeignKey('Loja', editable=True, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['codigo', 'loja'], name='codigo_unico'),
            models.UniqueConstraint(fields=['gtin', 'loja'], name='gtin_unico')
        ]


class Estoque(models.Model):
    TIPO_CHOICES = [('E', 'Entrada'), ('S', 'Saída')]

    produto = models.ForeignKey(Produto, editable=True, on_delete=models.CASCADE)
    tipo = models.CharField('Tipo', max_length=1, choices=TIPO_CHOICES,
                            default='E')
    quantidade = models.PositiveIntegerField('Quantidade')
    preco = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    data = models.DateTimeField('Data', editable=False, auto_now_add=True)

    def save(self, *args, **kwargs):
        """Sobrescrita do método para incrementar ou decrementar o total
        do estoque do produto relacionado ao estoque."""

        for field in self._meta.concrete_fields:
            if field.is_relation:
                produto = getattr(self, field.name, None)

        if produto:
            # se não possui pk, o estoque está sendo cadastrado
            if not self.pk:
                if self.tipo == "E":
                    produto.total_estoque += self.quantidade
                else:
                    produto.total_estoque -= self.quantidade
            else:
                old_estoque = Estoque.objects.get(pk=self.pk)
                if self.tipo != old_estoque.tipo:
                    if self.tipo == "S":
                        # se o estoque antigo é entrada
                        # então o novo é saída
                        produto.total_estoque -= old_estoque.quantidade
                        produto.total_estoque -= self.quantidade
                    else:
                        # se o estoque antigo é saída
                        # então o novo é entrada
                        produto.total_estoque += old_estoque.quantidade
                        produto.total_estoque += self.quantidade
                else:
                    if self.tipo == "E":
                        produto.total_estoque -= old_estoque.quantidade
                        produto.total_estoque += self.quantidade
                    else:
                        produto.total_estoque += old_estoque.quantidade
                        produto.total_estoque -= self.quantidade
            produto.save(update_fields=['total_estoque'])
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        r = super().delete(*args, **kwargs)
        produto = self.produto
        if self.tipo == "E":
            produto.total_estoque -= self.quantidade
        else:
            produto.total_estoque += self.quantidade
        produto.save(update_fields=['total_estoque'])
        return r


class Vendedor(models.Model):
    TIPO_CHOICES = [('J', 'Jurídica'), ('F', 'Física'), ('E', 'Estrangeiro')]

    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

    nome = models.CharField('Nome Completo', max_length=100)
    email = models.EmailField('Email', max_length=110, null=True, blank=True)
    codigo = models.CharField('Código', max_length=30, null=True, blank=True)
    fantasia = models.CharField('Nome Fantasia', max_length=80, null=True, blank=True)
    tipo = models.CharField('Tipo da Pessoa', max_length=1, choices=TIPO_CHOICES,
                            default='J')
    cnpj = models.CharField('CNPJ', max_length=18, null=True, blank=True)
    cpf = models.CharField('CPF', max_length=14, null=True, blank=True)
    rg = models.CharField('RG', max_length=20, null=True, blank=True)
    cep = models.CharField('CEP', max_length=9, null=True, blank=True)
    cidade = models.CharField('Cidade', max_length=60, null=True, blank=True)
    uf = models.CharField('UF', max_length=2, null=True, blank=True,
                          choices=STATE_CHOICES)
    endereco = models.CharField('Endereço/Rua', max_length=90, null=True, blank=True)
    numero = models.PositiveIntegerField('Número', null=True, blank=True)
    complemento = models.CharField('Complemento', max_length=90, null=True, blank=True)
    bairro = models.CharField('Bairro', max_length=90, null=True, blank=True)
    telefone = models.CharField('Telefone/Celular', max_length=15, null=True, blank=True)
    telefone2 = models.CharField('Celular', max_length=15, null=True, blank=True)
    data_cadastro = models.DateTimeField('Data do cadastro', editable=False, auto_now_add=True)
