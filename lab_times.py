import json
import os, django
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rinha_backend.settings")
django.setup()
#  Copyright (c) 2024.
#  Julio Cezar Riffel
#  https://www.linkedin.com/in/julio-cezar-riffel/
#  https://github.com/julioriffel
from conta_corrente.services import ClienteSaldo
from conta_corrente.models import Transacao

client_id = 1
body = '{"tipo":"c","valor":10000,"descricao":"xpto"}'

# start = datetime.now()
#
# ClienteSaldo.get_cliente(client_id)
# print(datetime.now() - start)
#
# data = json.loads(body)
# print(datetime.now() - start)
#
# if len(data['descricao']) < 1 or len(data['descricao']) > 10:
#     raise Exception
# print(datetime.now() - start)
#
# novo_saldo = ClienteSaldo.increment_saldo(client_id, data['tipo'], data['valor'])
# print(datetime.now() - start)
#
# Transacao.objects.create(cliente_id=client_id, tipo=data['tipo'], valor=int(data['valor']),
#                           descricao=data['descricao'])
#
# print(datetime.now() - start , '\n --------')
start = datetime.now()

cliente = ClienteSaldo.get_cliente(client_id)
print(datetime.now() - start)
transactions = Transacao.objects.filter(cliente_id=client_id).values('valor', 'tipo', 'descricao',
                                                                     'realizada_em')[:10]
print(datetime.now() - start)
saldo = {"total": cliente.saldo, "limite": cliente.limite, "data_extrato": str(datetime.now())}
print(datetime.now() - start)
b = list(transactions)
print(datetime.now() - start)
payload = {"saldo": saldo, "ultimas_transacoes": b}
print(datetime.now() - start)