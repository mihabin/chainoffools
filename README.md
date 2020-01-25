# CVE-2020-0601

I give full credit to https://github.com/kudelskisecurity/chainoffools. This fork just adds a Dockerfile which creates a pre-configured environment.

## Build Docker Image
```bash
docker build -t chainfofools .
```

## Docker container

```bash
docker run -it --rm -v $(pwd):/chainoffools chainoffools
```

## Forging certificate

```bash
pipenv run python gen-key.py
```