import csv
from decimal import Decimal
from home.models import Produto
from accounts.models import CustomUser

def run():
    user = CustomUser.objects.get(pk=1)

    with open("C:\\Users\\Gabriel\\Documents\\produtos_2019-11-26-19-02-34.csv", "r", encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)
        for row in reader:
            print(row)
            obj, create = Produto.objects.get_or_create(
                descricao=row[2],
                preco_venda=Decimal(row[6].replace(',','.')),
                codigo=row[1],
                situacao='A',
                condicao='NO',
                total_estoque=int(row[10].split(',', 1)[0]),
                user=user
            )
