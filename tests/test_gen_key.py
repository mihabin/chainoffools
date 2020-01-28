# pylint: disable=line-too-long
"""
test_gen_key module is a simple test module
"""
from unittest import TestCase

from gen_key import get_public_key

EXPEXCTED_ENCODED_PUB_KEY = b"1aac545aa9f96823e77ad5246f53c65ad84babc6d5b6d1e67371aedd9cd60c61fddba08903b80514ec57ceee5d3fe221b3cef7d48a79e0a3837e2d97d061c4f199dc259163ab7f30a3b470e2c7a1339cf3bf2e5c53b15fb37d327f8a34e37979"


class TestGenKey(TestCase):
    """
    TestGenKey sets up tests for public key
    """

    def test_public_key(self):
        """
        testing to make sure we get the expected encoded public key
        """
        p_k = get_public_key("./tools/USERTrustECCCertificationAuthority.crt")
        self.assertEqual(p_k, EXPEXCTED_ENCODED_PUB_KEY)
