from unittest import TestCase
from gen_key2 import pub_key
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PublicFormat

EXPECTED_PUB_KEY = b"""-----BEGIN PUBLIC KEY-----
MHYwEAYHKoZIzj0CAQYFK4EEACIDYgAExxEWKnYdVo6+uWJl1MPOtPDDMOyPbddu
ObzISauruONDeNWBBl3vx32fztazkHXeDLCQ3iO6yNE+Z+AZqRuGMR5fNC3uF/0V
+34nijKh6smPyX4Yyy87LEh6fab0AQes
-----END PUBLIC KEY-----
"""

class TestGenKey(TestCase):
    def test_public_key(self):
        """
        testing to make sure we get the right public key
        """
        pk = pub_key("./tools/MicrosoftECCProductRootCertificateAuthority.cer")
        public_key = pk.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
        self.assertEqual(EXPECTED_PUB_KEY, public_key)