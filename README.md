
# containerinfo

Extract some information from containers using Python.

## Usage

### Docker

Build the image:

```bash
docker build --platform linux/amd64 -t containerinfo: .
```

Or use the pre-built image:

```bash
docker pull guerzon/containerinfo
```

Export the following environment variables. For now the supported authentication method is bearer token.

- `KUBERNETES_SERVICE_HOST`: the IP address or domain name of the `https` endpoint for the Kubernetes API, example: **10.10.10.1**.
- `KUBERNETES_BEARER_TOKEN`: Bearer token to authenticate to the Kubernetes API, example: **eyJhbGciOiJSUzI1NiIsIm...**

```bash
docker run --rm -p 5000:5000 -e KUBERNETES_SERVICE_HOST -e KUBERNETES_BEARER_TOKEN --name containerinfo guerzon/containerinfo:${VERSION}
```

Access the application:

```bash
curl -s http://localhost:5000/container-resources?pod-label=app.kubernetes.io/component=jenkins-master
```

### Helm chart

Todo.

## References

- <https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md>
- <https://raw.githubusercontent.com/kubernetes-client/python/master/kubernetes/docs/CoreV1Api.md>
