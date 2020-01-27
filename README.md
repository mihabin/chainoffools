# CVE-2020-0601

I give full credit to https://github.com/kudelskisecurity/chainoffools. This fork just adds a Dockerfile which creates a pre-configured environment.

## Build Docker Image
```bash
docker build -t chainoffools .
```

## Docker container

To run the container with a bash shell

```bash
docker run -it --rm -v $(pwd):/chainoffools chainoffools bash
```

## Forging certificate

To forge certificate using default settings

```bash
docker run -it --rm -v $(pwd):/chainoffools chainoffools
```