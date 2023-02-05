import os

class Config(object):
    KUBERNETES_SERVICE_HOST = os.environ.get('KUBERNETES_SERVICE_HOST') or ''
    KUBERNETES_BEARER_TOKEN = os.environ.get('KUBERNETES_BEARER_TOKEN') or ''