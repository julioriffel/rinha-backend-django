#  Copyright (c) 2024.
#  Julio Cezar Riffel
#  https://www.linkedin.com/in/julio-cezar-riffel/
#  https://github.com/julioriffel
#
from django.db import IntegrityError

from conta_corrente.models import Cliente
from rinha_backend.redis import UtilsRedis


class ClienteSaldo:
    redis = UtilsRedis.get_redis()

    @classmethod
    def ajuste_saldo(cls, tipo, valor):
        if tipo == 'c':
            return valor
        else:
            return -valor

    @classmethod
    def limite_saldo(cls, client_id):
        key_saldo_limite = f'saldo:{client_id}'
        limite = cls.redis.get(key_saldo_limite)
        if limite is None:
            cliente = Cliente.objects.get(id=client_id)
            cls.redis.set(f'cliente_saldo_limite{client_id}', cliente.limite)
            limite = cliente.limite
        return limite

    @classmethod
    def persistir_saldo(cls, client_id: int, valor: int):
        with cls.redis.lock(f'cliente_saldo_lock_{client_id}', timeout=60):
            key_saldo_atual = f'cliente_saldo_atual_{client_id}'
            novo_saldo = cls.redis.incrby(key_saldo_atual, valor)
            limite = cls.limite_saldo(client_id)
            if novo_saldo < -limite:
                cls.redis.incrby(key_saldo_atual, -valor)
                raise IntegrityError
            Cliente.objects.filter(pk=client_id).update(saldo=novo_saldo)
            return novo_saldo, limite

    @classmethod
    def increment_saldo(cls, cliente_id, tipo: str, valor: int):
        novo_saldo, limite = cls.persistir_saldo(cliente_id, cls.ajuste_saldo(tipo, valor))

        return {'saldo': novo_saldo, 'limite': limite}
