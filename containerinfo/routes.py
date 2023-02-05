from containerinfo import containerapp
from flask import jsonify

@containerapp.route('/')
def index():
    return "Hello world!"

@containerapp.route('/container-resources')
def container_resources():
    return jsonify(
        container_name="jenkins-master-test",
        pod_name="pod-name-test",
        namespace="namespacename-test",
        mem_req="1024Mi",
        mem_limit="4096Mi",
        cpu_req="200m",
        cpu_limit="500m"
    )
