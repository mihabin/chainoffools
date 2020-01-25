from OpenSSL import crypto

# read file

# path = "/root/MicrosoftECCProductRootCertificateAuthority.cer"
path = "/root/USERTrustECCCertificationAuthority.crt"
with open(path, "r") as f:
    cert = f.read()

ca = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
ca_key = ca.get_pubkey()
pub_key = crypto.dump_publickey(crypto.FILETYPE_PEM, ca_key)

print(pub_key)
pubkey = b"1aac545aa9f96823e77ad5246f53c65ad84babc6d5b6d1e67371aedd9cd60c61fddba08903b80514ec57ceee5d3fe221b3cef7d48a79e0a3837e2d97d061c4f199dc259163ab7f30a3b470e2c7a1339cf3bf2e5c53b15fb37d327f8a34e37979"
