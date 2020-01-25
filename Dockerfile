FROM python:3.7

RUN pip install pipenv 
    pipenv install git+https://github.com/dlitz/pycrypto#egg=pycrypto