import os

class Config(object):
    KUBERNETES_API_ENDPOINT = os.environ.get('KUBERNETES_SERVICE_HOST') or 'i-am-not-running-in-kubernetes'
