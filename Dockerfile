FROM debian:10.2

ENV DEBIAN_FRONTEND noninteractive
COPY ./tools/install-pyenv.sh /root/
RUN chmod +x /root/install-pyenv.sh
RUN /root/install-pyenv.sh

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

ENV PYTHONUNBUFFERED 1

ENV PYENV_ROOT /root/.pyenv
ENV PATH /root/.pyenv/shims:/root/.pyenv/bin:$PATH

ARG PYTHON_VERSION=3.7.6
ENV PYTHON_CONFIGURE_OPTS "--enable-shared"
RUN pyenv install --force 3.7.6
RUN pyenv global 3.7.6

COPY ./tools/install-pipenv.sh /root/
RUN chmod +x /root/install-pipenv.sh
RUN /root/install-pipenv.sh 3.7.6

WORKDIR /root
RUN curl -O http://www.tbs-x509.com/USERTrustECCCertificationAuthority.crt && \
    curl -O https://raw.githubusercontent.com/ollypwn/CurveBall/master/MicrosoftECCProductRootCertificateAuthority.cer

WORKDIR /chainoffools

COPY . .

RUN pipenv update && \
    chmod +x gen-keys.sh

CMD [ "./gen-keys.sh" ]