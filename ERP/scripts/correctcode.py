from home.models import Produto
from django.db.models import F

def run():
    # for produto in Produto.objects.filter(user__id=1)
    Produto.objects.filter(user__id=1).update(codigo=F('codigo').replace('\t', ""))
