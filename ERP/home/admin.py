from django.contrib import admin

from .models import Produto, Estoque, Vendedor, Loja

admin.site.register(Produto)
admin.site.register(Estoque)
admin.site.register(Vendedor)
admin.site.register(Loja)

# Register your models here.
