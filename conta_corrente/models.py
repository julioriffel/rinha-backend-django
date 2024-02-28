#  Copyright (c) 2024.
#  Julio Cezar Riffel
#  https://www.linkedin.com/in/julio-cezar-riffel/
#  https://github.com/julioriffel
#
from django.db import models
from django.utils import timezone




class Cliente(models.Model):
    limite = models.PositiveIntegerField(default=0)

    @property
    def saldo(self):
        if self.id:
            from conta_corrente.services import ClienteSaldo
            return ClienteSaldo.get_saldo(self.id)
        else:
            return 0


class Transacao(models.Model):
    cliente_id = models.IntegerField()
    tipo = models.CharField(max_length=1)
    valor = models.PositiveIntegerField()
    descricao = models.CharField(max_length=10)
    realizada_em = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-id',)

    @property
    def to_dict(self):
        return {
            "valor": self.valor,
            "tipo": self.tipo,
            "descricao": self.descricao,
            "realizada_em": str(self.realizada_em)
        }
