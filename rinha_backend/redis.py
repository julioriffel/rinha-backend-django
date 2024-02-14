#  Copyright (c) 2024.
#  Julio Cezar Riffel
#  https://www.linkedin.com/in/julio-cezar-riffel/
#  https://github.com/julioriffel
#

from django.conf import settings
from redis import Redis


class UtilsRedis:
    @staticmethod
    def get_redis():
        return Redis(host=settings.REDIS_HOST, port=6379, db=0)
