
# containerinfo

This demo application written in Python extracts information from pods and containers across a Kubernetes cluster using the Kubernetes API.

## Usage

### Kubernetes

This demo application, as described above, is supposed to run in a Kubernetes cluster. Use [this](https://github.com/guerzon/containerinfo-helm) Helm chart to deploy the application to Kubernetes.

### Docker

You can also use Docker (or `podman`) to build and test locally, or to run the app on a Docker host external to the Kubernetes cluster

As a prerequisite, create a service account with permissions to read pod information. The following `ClusterRole` and `ClusterRoleBinding` definitions can be used to create the service account:

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
# build the image
docker build --platform linux/amd64 -t containerinfo .

# or use the pre-built image:
docker pull guerzon/containerinfo
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

## License

See [LICENSE](./LICENSE)

## Author

[Lester Guerzon](mailto:lester.guerzon@outlook.com)
