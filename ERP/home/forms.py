from localflavor.br import forms as brForms
from django import forms
from .models import Produto, Estoque, Vendedor, Loja


class CadastroLojaForm(forms.ModelForm):

    class Meta():
        model = Loja
        fields = ['nome', 'cnpj']
        field_classes = {
            'cnpj': brForms.BRCNPJField,
        }


class CadastroProdutoForm(forms.ModelForm):

    class Meta():
        model = Produto
        fields = ['descricao', 'preco_venda', 'codigo', 'situacao', 'gtin',
                  'data_validade', 'condicao']
        """widgets = {
            'user': forms.HiddenInput,
        }"""


class CadastrarEstoqueForm(forms.ModelForm):

    class Meta():
        model = Estoque
        fields = ['produto', 'tipo', 'quantidade', 'preco']
        widgets = {
            'produto': forms.HiddenInput,
        }

    """def save(self, commit=True):
        self.instance.produto.total_estoque += self.instance.quantidade
        print(self.instance.produto.total_estoque)
        print(self.instance.quantidade)
        return super().save()"""


class CadastrarVendedorForm(forms.ModelForm):

    class Meta():
        model = Vendedor
        fields = ['nome', 'email', 'codigo', 'fantasia', 'tipo', 'cnpj', 'cpf', 'rg',
                  'cep', 'cidade', 'uf', 'endereco', 'numero', 'complemento', 'bairro',
                  'telefone', 'telefone2']
        field_classes = {
            'cnpj': brForms.BRCNPJField,
            'cpf': brForms.BRCPFField,
        }
