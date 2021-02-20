from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('cadastro_produto/', views.CadastroProdutoView.as_view(), name='cadastro_produto'),
    path('cadastrado/', TemplateView.as_view(template_name='cadastrado.html'), name='cadastrado'),
    path('listar_produtos/json/', views.produto_json_search, name='produto_json_search'),
    path('listar_produtos/', views.ListarProdutoView.as_view(), name='listar_produtos'),
    path('alterar_produto/<int:pk>/', views.AlterarProdutoView.as_view(), name='alterar_produto'),
    path('remover_produto/<int:pk>/', views.RemoverProdutoView.as_view(), name='remover_produto'),
    path('listar_estoque/<int:pk>/', views.ListarEstoqueView.as_view(), name='listar_estoque'),
    path('listar_estoque/', views.ListarEstoqueView.as_view(), name='listar_estoque'),
    path('cadastrar_estoque/', views.CadastrarEstoqueView.as_view(), name='cadastrar_estoque'),
    path('remover_estoque/', views.RemoverEstoqueView.as_view(), name='remover_estoque'),
    path('cadastrar_vendedor/', views.CadastrarVendedorView.as_view(), name='cadastrar_vendedor'),
    path('listar_vendedores/', views.ListarVendedoresView.as_view(), name='listar_vendedores'),
    path('remover_vendedor/<int:pk>/', views.RemoverVendedorView.as_view(), name='remover_vendedor'),
    path('cadastrar_loja', views.CadastrarLojaView.as_view(), name='cadastrar_loja')
]
