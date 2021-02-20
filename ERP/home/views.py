from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.urls import reverse, reverse_lazy
# from django.shortcuts import redirect
# from django.core import serializers
from django.core.paginator import Paginator

from .forms import CadastroProdutoForm, CadastrarEstoqueForm, CadastrarVendedorForm, CadastroLojaForm
from .models import Produto, Estoque, Vendedor, Loja


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """
    Mixin que verifica se o usuário está logado e caso esteja,
    verifica se a loja associada na sessão pertence ao usuário.
    Se a loja não pertence ao usuário, associa a loja padrão para a sessão.
    """
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return self.handle_no_permission()
        try:
            user.loja_set.get(pk=request.session['loja'])
        except ObjectDoesNotExist:
            request.session['loja'] = user.loja_set.get(loja_principal=True).pk
        return super().dispatch(request, *args, **kwargs)


class CustomPaginator(Paginator):

    def _get_page(self, *args, **kwargs):
        self.page = super(CustomPaginator, self)._get_page(*args, **kwargs)
        return self.page

    @property
    def page_range(self):
        if not self.page.has_next():
            start = self.page.number - 3
            stop = self.page.number + 1
        elif not self.page.has_previous():
            start = self.page.number
            stop = 5
        elif self.page.number >= 4:
            start = self.page.number - 2
            stop = self.page.number + 2
        else:
            start = 1
            stop = 5
        return range(
            start if start > 0 else 1,
            stop if stop <= self.num_pages else self.num_pages + 1,
            1
        )


class HomeView(CustomLoginRequiredMixin, TemplateView):
    template_name = "home.html"


class CadastrarLojaView(CustomLoginRequiredMixin, CreateView):
    form_class = CadastroLojaForm
    template_name = "cadastrar_loja.html"

    def get_form_kwargs(self):
        """Cria a instancia da loja com a fk do usuário e passa pro form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': Loja(user=self.request.user)})
        return kwargs

    def get_success_url(self):
        return reverse('home')


class CadastroProdutoView(CustomLoginRequiredMixin, CreateView):
    form_class = CadastroProdutoForm
    template_name = "cadastro_produto.html"

    """def get_form(self):
        return self.form_class(instance=Produto(user=self.request.user))"""

    def get_form_kwargs(self):
        """Cria a instancia do produto com a fk da loja e passa pro form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': Produto(loja_id=self.request.session['loja'])})
        return kwargs

    def get_success_url(self):
        return reverse('listar_produtos')


class ListarProdutoView(CustomLoginRequiredMixin, ListView):
    model = Produto
    template_name = "listar_produtos.html"
    paginator_class = CustomPaginator
    paginate_by = 20

    def create_search_queryset(self, search):
        queryset = Produto.objects.filter(
            loja_id=self.request.session.get('loja')
        ).filter(
            Q(codigo__contains=search) | Q(descricao__contains=search)
        )
        return queryset

    def get_queryset(self):
        if self.request.GET.get('search'):
            self.paginate_by = 5
            search = self.request.GET.get('search')
            queryset = self.create_search_queryset(search)
            return queryset
        queryset = Produto.objects.filter(
            loja_id=self.request.session.get('loja')
        ).order_by('-data_cadastro')
        return queryset


@login_required
def produto_json_search(request):
    """
    Esta view é utilizada para a pesquisa dinâmica de produtos na página
    de estoque. Retorna uma listagem de produtos em JSON.
    /listar_produtos/json/?search=(search)
    """
    if request.POST:
        raise Http404
    if request.GET.get('search'):
        search = request.GET.get('search')
        # print(request.user.id)
        queryset = Produto.objects.filter(
            loja_id=request.session['loja']
        ).filter(
            Q(codigo__contains=search) | Q(descricao__contains=search)
        )

        fields = [field.name for field in Produto._meta.get_fields()]
        fields.remove('loja')
        fields.remove('estoque')

        qr_list = list(queryset.values(*fields))

        resp = JsonResponse(qr_list, safe=False, json_dumps_params={'ensure_ascii':False})

        resp['Access-Control-Allow-Origin'] = "*"
        resp['Access-Control-Allow-Headers'] = "Content-Type"
        resp['Access-Control-Allow-Credentials'] = "true"

        return resp
    raise Http404


class AlterarProdutoView(CustomLoginRequiredMixin, UpdateView):
    model = Produto
    template_name = "alterar_produto.html"
    fields = ['descricao', 'preco_venda', 'codigo', 'situacao', 'gtin',
              'data_validade', 'condicao']

    def get_success_url(self):
        return reverse('listar_produtos')

    def get_queryset(self):
        queryset = Produto.objects.filter(loja_id=self.request.session['loja'])
        return queryset


class RemoverProdutoView(CustomLoginRequiredMixin, DeleteView):
    model = Produto
    template_name = "remover_produto.html"
    success_url = reverse_lazy('listar_produtos')

    def get_queryset(self):
        queryset = Produto.objects.filter(loja_id=self.request.session['loja'])
        return queryset


class ListarEstoqueView(CustomLoginRequiredMixin, SingleObjectMixin, ListView):
    # model = Estoque
    template_name = "listar_estoque.html"
    paginator_class = CustomPaginator
    paginate_by = 5

    def get_object(self, *args, **kwargs):
        # Verifica se a PK foi passada na URLConf
        if not self.kwargs.get(self.pk_url_kwarg):
            # Caso não haja PK na URLConf, retorna um objeto vazio
            return Produto.objects.none()
        return super().get_object(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Produto.objects.filter(
            loja_id=self.request.session['loja'])
        )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produto'] = self.object
        return context

    def get_queryset(self):
        try:
            return self.object.estoque_set.all().order_by('-data')
        except AttributeError:
            return self.object.none()


class CadastrarEstoqueView(CustomLoginRequiredMixin, CreateView):
    form_class = CadastrarEstoqueForm
    # template_name = "cadastrar_estoque.html"

    """def get_initial(self):
        return {'produto': self.request.POST.produto}"""
    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        if request.POST['produto']:
            produto = Produto.objects.select_related('loja').get(pk=request.POST['produto'])
            if produto.loja.pk != request.session['loja']:
                raise PermissionDenied
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('listar_estoque', args=[self.request.POST.get('produto', '')])


class RemoverEstoqueView(CustomLoginRequiredMixin, DeleteView):
    model = Estoque

    def get(self, request, *args, **kwargs):
        raise Http404

    def get_object(self, *args, **kwargs):
        if self.request.POST.get('pk'):
            self.kwargs['pk'] = self.request.POST.get('pk')
        return super().get_object(*args, **kwargs)

    def get_queryset(self):
        return Estoque.objects.filter(produto__loja_id=self.request.session['loja'])

    def get_success_url(self):
        return reverse('listar_estoque', args=[self.object.produto.pk])


class CadastrarVendedorView(CustomLoginRequiredMixin, CreateView):
    form_class = CadastrarVendedorForm
    template_name = "cadastrar_vendedor.html"

    def get_form_kwargs(self):
        """Cria a instancia do vendedor com a fk do usuário e passa pro form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': Vendedor(user=self.request.user)})
        return kwargs

    def get_success_url(self):
        return reverse('listar_vendedores')


class ListarVendedoresView(CustomLoginRequiredMixin, ListView):
    model = Vendedor
    template_name = "listar_vendedores.html"
    paginator_class = CustomPaginator
    paginate_by = 5

    def create_search_queryset(self, search):
        queryset = Vendedor.objects.filter(
            user_id=self.request.user.id
        ).filter(
            Q(codigo__contains=search) | Q(descricao__contains=search)
        )
        return queryset

    def get_queryset(self):
        if self.request.GET.get('search'):
            self.paginate_by = 5
            search = self.request.GET.get('search')
            queryset = self.create_search_queryset(search)
            return queryset
        queryset = Vendedor.objects.filter(user_id=self.request.user.id).order_by('-data_cadastro')
        return queryset


class RemoverVendedorView(CustomLoginRequiredMixin, DeleteView):
    model = Vendedor
    template_name = "remover_vendedor.html"
    success_url = reverse_lazy('listar_vendedores')

    def get_queryset(self):
        queryset = Vendedor.objects.filter(user_id=self.request.user.id)
        return queryset
