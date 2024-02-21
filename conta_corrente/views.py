#  Copyright (c) 2024.
#  Julio Cezar Riffel
#  https://www.linkedin.com/in/julio-cezar-riffel/
#  https://github.com/julioriffel
#
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.viewsets import GenericViewSet

from conta_corrente.models import Cliente
from conta_corrente.serializers import TrasacaoSerializer, ExtratoSerializer
from conta_corrente.services import ClienteSaldo


class ClienteView(GenericViewSet):
    serializer_class = TrasacaoSerializer
    queryset = Cliente.objects.all()

    @action(detail=True, methods=['post'], url_path='transacoes', url_name='transacoes', name='Cliente - Transação')
    def transacoes(self, request, pk):

        data = JSONParser().parse(request)
        data['cliente'] = pk
        serializer = TrasacaoSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            novo_saldo = ClienteSaldo.increment_saldo(pk, serializer.validated_data['tipo'],
                                                      serializer.validated_data['valor'])
            serializer.save()
            return JsonResponse(novo_saldo, status=200)

    @action(detail=True, methods=['get'], url_path='extrato', url_name='extrato', name='Cliente - Extrato')
    def extrato(self, request, pk):
        try:
            cliente = ClienteSaldo.get_cliente(pk)
            cliente_serializer = ExtratoSerializer(cliente)
            return JsonResponse(cliente_serializer.data, status=200)
        except Cliente.DoesNotExist:
            return HttpResponse(status=404)
