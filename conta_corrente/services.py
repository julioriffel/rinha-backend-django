#  Copyright (c) 2024.
#  Julio Cezar Riffel
#  https://www.linkedin.com/in/julio-cezar-riffel/
#  https://github.com/julioriffel
#
from django.db import IntegrityError
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404

from conta_corrente.models import Cliente, Transacao
from rinha_backend.redis import UtilsRedis


class ClienteSaldo:
    redis = UtilsRedis.get_redis()

    @classmethod
    def get_saldo_key(cls, client_id) -> str:
        return f'cliente_saldo_atual_{client_id}'

    @classmethod
    def get_limite_key(cls, client_id) -> str:
        return f'cliente_limite_{client_id}'

    @classmethod
    def get_limite(cls, client_id) -> int:
        limite = cls.redis.get(cls.get_limite_key(client_id))
        if type(limite) is bytes:
            return int(limite.decode('utf-8'))
        else:
            cliente = get_object_or_404(Cliente, id=client_id)
            cls.set_limite(client_id, cliente.limite)
            return cliente.limite

    @classmethod
    def set_limite(cls, client_id: int, limite: int) -> None:
        cls.redis.set(cls.get_limite_key(client_id), limite)

    @classmethod
    def get_cliente(cls, client_id) -> Cliente:
        limite = cls.get_limite(client_id)
        return Cliente(id=client_id, limite=limite)

    @classmethod
    def ajuste_saldo(cls, tipo, valor):
        if tipo == 'c':
            return valor
        elif tipo == 'd':
            return -valor
        else:
            raise Exception('Tipo')

    @classmethod
    def persistir_saldo(cls, client_id: int, valor: int):
        with cls.redis.lock(f'cliente_saldo_lock_{client_id}', timeout=0.2):
            limite = cls.get_limite(client_id)

            novo_saldo = cls.redis.incrby(cls.get_saldo_key(client_id), valor)
            if novo_saldo + limite < 0:
                cls.redis.incrby(cls.get_saldo_key(client_id), -valor)
                raise IntegrityError
            return novo_saldo, limite

    @classmethod
    def increment_saldo(cls, cliente_id, tipo: str, valor: int):
        novo_saldo, limite = cls.persistir_saldo(cliente_id, cls.ajuste_saldo(tipo, valor))
        return {'saldo': novo_saldo, 'limite': limite}

    @classmethod
    def get_saldo(cls, client_id: int) -> int:
        saldo = cls.get_saldo_redis(client_id)
        if saldo is None:
            saldo = cls.get_saldo_db(client_id)
        return saldo

    @classmethod
    def get_saldo_redis(cls, client_id):
        with cls.redis.lock(f'cliente_saldo_lock_{client_id}', timeout=0.2):
            saldo = cls.redis.get(cls.get_saldo_key(client_id))
            if type(saldo) is bytes:
                return int(saldo.decode('utf-8'))

    @classmethod
    def get_saldo_db(cls, client_id: int) -> int:
        valor = 0
        t = (Transacao.objects
             .annotate(cred=Coalesce(Sum('valor', filter=Q(tipo='c')), 0))
             .annotate(deb=Coalesce(Sum('valor', filter=Q(tipo='d')), 0))
             .filter(cliente_id=client_id)).first()
        if t is not None:
            valor = t.cred - t.deb
        cls.redis.set(cls.get_saldo_key(client_id), valor)
        return valor
