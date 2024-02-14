#  Copyright (c) 2024.
#  Julio Cezar Riffel
#  https://www.linkedin.com/in/julio-cezar-riffel/
#  https://github.com/julioriffel
#
from rest_framework.routers import DefaultRouter

from conta_corrente.views import ClienteView

router_api_v0 = DefaultRouter(trailing_slash=False)
router_api_v0.register(r'clientes', ClienteView, 'clientes')