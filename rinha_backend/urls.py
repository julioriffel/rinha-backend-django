#  Copyright (c) 2024.
#  Julio Cezar Riffel
#  https://www.linkedin.com/in/julio-cezar-riffel/
#  https://github.com/julioriffel
#

from django.urls import include, path

urlpatterns = [
    path("clientes/", include("conta_corrente.urls")),
]
