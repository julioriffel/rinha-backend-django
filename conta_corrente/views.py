#  Copyright (c) 2024.
#  Julio Cezar Riffel
#  https://www.linkedin.com/in/julio-cezar-riffel/
#  https://github.com/julioriffel
#
import json
from datetime import datetime

from django.http import HttpResponse, JsonResponse

from conta_corrente.models import Transacao
from conta_corrente.services import ClienteSaldo


def transaction(request, client_id):
    try:
        if request.method == 'POST':
            cliente = ClienteSaldo.get_cliente(client_id)
            data = json.loads(request.body)
            if len(data['descricao']) < 1 or len(data['descricao']) > 10:
                raise Exception
            novo_saldo = ClienteSaldo.increment_saldo(client_id, data['tipo'], data['valor'])
            transacao = Transacao(cliente=cliente, tipo=data['tipo'], valor=int(data['valor']),
                                  descricao=data['descricao'])
            transacao.save()
            return JsonResponse(novo_saldo, status=200)
    except Exception:
        return HttpResponse(status=422)


def financial(request, client_id):
    if request.method == 'GET':
        cliente = ClienteSaldo.get_cliente(client_id)
        transactions = Transacao.objects.filter(cliente_id=client_id).values('valor', 'tipo', 'descricao',
                                                                             'realizada_em')[:10]

        saldo = {"total": cliente.saldo, "limite": cliente.limite, "data_extrato": str(datetime.now())}
        payload = {"saldo": saldo, "ultimas_transacoes": list(transactions)}
        return JsonResponse(payload, status=200)
