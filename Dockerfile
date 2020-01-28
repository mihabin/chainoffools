FROM python:3.7.6-stretch

WORKDIR /app

RUN apt update && \
    apt install --yes libmpc-dev && \
    pip install fastecdsa && \
    pip install gmpy2 && \
    pip install pycryptodome && \
    pip install click

COPY . .

ENV EC_CERT="/app/tools/MicrosoftECCProductRootCertificateAuthority.cer"

CMD [ "python", "gen_key.py"]