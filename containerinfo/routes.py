from containerinfo import containerapp
from flask import request, jsonify
from kubernetes import client, config

@containerapp.route('/')
def index():
    return jsonify([{"message": "Welcome, I am the index page!"}])

@containerapp.route('/container-resources')
def container_resources():
    if containerapp.config['KUBERNETES_SERVICE_HOST'] == '' or containerapp.config['KUBERNETES_BEARER_TOKEN'] == '':
        return "Sorry, I don't think was configured properly :( please see my README for required variables.\n"

    if request.args.get('pod-label') is not None:
        label_search = request.args.get('pod-label')
    else:
        return jsonify([{"message": "No label specified in query. Please specify a label using 'pod-label', example: /container-resources?pod-label=app.kubernetes.io/part-of=kube-prometheus"}])

    # create a config object
    configuration = client.Configuration()
    
    # set authentication via bearer token
    configuration.api_key = {"authorization": "Bearer " + containerapp.config['KUBERNETES_BEARER_TOKEN']}
    
    # set the kubernetes https endpoint
    configuration.host =  "https://" + containerapp.config['KUBERNETES_SERVICE_HOST']
    
    # specify the ca cert
    configuration.ssl_ca_cert = containerapp.config['KUBERNETES_CA_CRT']
    
    # create an api client using the config object
    apiClient = client.ApiClient(configuration)
    
    # do the api call
    v1 = client.CoreV1Api(apiClient)
    pods = v1.list_pod_for_all_namespaces(label_selector=label_search)
    if len(pods.items) == 0:
        return jsonify([{"message": "Sorry, your query did not return any results."}])

    pod_result = []
    for pod in pods.items:
        pod_dict = {
            'container_name':pod.spec.containers[0].name,
            'pod_name':pod.metadata.name,
            'namespace':pod.metadata.namespace,
            'mem_req': pod.spec.containers[0].resources.requests["memory"],
            'mem_limit':pod.spec.containers[0].resources.limits["memory"],
            'cpu_req':pod.spec.containers[0].resources.requests["cpu"],
            'cpu_limit':pod.spec.containers[0].resources.limits["cpu"]}
        pod_result.append(pod_dict)

    return jsonify(pod_result)