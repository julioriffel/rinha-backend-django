#  Copyright (c) 2024.
#  Julio Cezar Riffel
#  https://www.linkedin.com/in/julio-cezar-riffel/
#  https://github.com/julioriffel
#
from django.urls import path

from . import views

urlpatterns = [
    path("<int:client_id>/extrato", views.financial, name="extrato"),
    path("<int:client_id>/transacoes", views.transaction, name="transacoes"),
]
