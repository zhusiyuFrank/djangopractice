import hashlib
from django.conf import settings


def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))  # SECRET_KEY自动生成随机salt
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
