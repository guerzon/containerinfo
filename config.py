import os

class Config(object):
    KUBERNETES_SERVICE_HOST = os.environ.get('KUBERNETES_SERVICE_HOST') or ''
    with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as sa_token:
        KUBERNETES_BEARER_TOKEN = sa_token.read()
    KUBERNETES_CA_CRT = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
