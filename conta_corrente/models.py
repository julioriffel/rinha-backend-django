#  Copyright (c) 2024.
#  Julio Cezar Riffel
#  https://www.linkedin.com/in/julio-cezar-riffel/
#  https://github.com/julioriffel
#
from django.db import models
from django.utils import timezone

TIPO_CHOICE = [('c', 'Credit'), ('d', 'Debit')]


class Cliente(models.Model):
    limite = models.PositiveIntegerField(default=0)
    saldo = models.IntegerField(default=0)


class Transacao(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICE)
    valor = models.IntegerField()
    descricao = models.CharField(max_length=10)
    realizada_em = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-id',)
