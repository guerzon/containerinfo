
# containerinfo

Extract some information from containers using Python.

## Development

```bash
docker build -t containerinfo:0.1 .
docker run -d -it -p 5000:5000 --name containerinfo containerinfo:0.1

curl http://localhost:5000/container-resources
```
