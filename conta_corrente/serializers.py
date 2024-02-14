#  Copyright (c) 2024.
#  Julio Cezar Riffel
#  https://www.linkedin.com/in/julio-cezar-riffel/
#  https://github.com/julioriffel
#
from django.utils.timezone import now
from rest_framework import serializers

from conta_corrente.models import Cliente, Transacao


class ClienteSaldoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['limite', 'saldo']


class TrasacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        fields = ['tipo', 'valor', 'descricao', 'cliente']


class TrasacaoExtratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        fields = ['tipo', 'valor', 'descricao', 'realizada_em']


class ExtratoClienteSerializer(serializers.ModelSerializer):
    total = serializers.IntegerField(source='saldo', read_only=True)
    data_extrato = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cliente
        fields = ['total', 'data_extrato', 'limite', ]

    def get_data_extrato(self, obj):
        return now()


class ExtratoSerializer(serializers.Serializer):
    saldo = serializers.SerializerMethodField(read_only=True)
    ultimas_transacoes = serializers.SerializerMethodField(read_only=True)

    def get_ultimas_transacoes(self, obj):
        transactions = Transacao.objects.all()[:10]
        return TrasacaoExtratoSerializer(transactions, source='transactions', many=True, read_only=True).data

    def get_saldo(self, obj):
        return ExtratoClienteSerializer(obj).data

    class Meta:
        model = Cliente
        fields = ['saldo', 'ultimas_transacoes']
