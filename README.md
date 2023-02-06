
# containerinfo

This demo application written in Python extracts some information from containers across a Kubernetes cluster.

## Usage

### Helm chart

This service is destined to be ran in a Kubernetes cluster. Use this (TBD) Helm chart to deploy the application.

### Docker

You can also use Docker (or podman) to build and test locally.

The application was designed to run under a service account with cluster-wide permissions to read pods. An example `ClusterRole` and `ClusterRoleBinding` for such a service account is as follows:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: containerinfo
  namespace: containerinfo
  labels:
    app.kubernetes.io/component: containerinfo
rules:
  - apiGroups: ["extensions", "apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get","list","watch"]
  - apiGroups: [""]
    resources: ["pods/exec"]
    verbs: ["get","list","watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: containerinfo
  labels:
    app.kubernetes.io/component: containerinfo
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: containerinfo
subjects:
- kind: ServiceAccount
  name: containerinfo
  namespace: containerinfo
```

After [creating the service account](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/), proceed as follows:

```bash
# set the version, can be 'latest'
export VERSION=1.0

# build the image
docker build --platform linux/amd64 -t containerinfo:${VERSION} .

# or use the pre-built image:
docker pull guerzon/containerinfo:${VERSION}
```

You can create a local directory called `data` and put the CA certificate and token inside, as follows:

```bash
lester:containerinfo lester$ tree data
data
|-- ca.crt
|-- namespace
`-- token

1 directory, 3 files
lester:containerinfo lester$
```

Run the container, mount the `data/` directory inside the container:

```bash
export KUBERNETES_SERVICE_HOST=<IP of the Kubernetes API>

docker run --rm -p 5000:5000 \
  -e KUBERNETES_SERVICE_HOST \
  -v $(pwd)/data:/var/run/secrets/kubernetes.io/serviceaccount \
  --name containerinfo \
  guerzon/containerinfo:${VERSION}
```

Access the application:

```bash
curl -s http://localhost:5000/container-resources?pod-label=app.kubernetes.io/component=jenkins-master
```

## References

- <https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md>
- <https://raw.githubusercontent.com/kubernetes-client/python/master/kubernetes/docs/CoreV1Api.md>
