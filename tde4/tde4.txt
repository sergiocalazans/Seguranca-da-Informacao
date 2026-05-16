#!/bin/bash -x

# QUIZ DOS THREE STOOGES:

# Qual dos Stooges enviou a mensagem?
# R: Foi o Larry, conforme o teste.

# Resolução:

echo "Can you can a can as a canner can can a can?" > mensagem.txt

echo "-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDqdsSULdJXwpvB8usHwf1kGoy+
UKD7ErT4tTRifhk/gqElet63aSVz0lOyMpJ8D0lQfuoTi6csKpPPjEZwiRpE6Rs/
mlOWMaRkHQ0G1BtWLcdZp+u9JOXm486if5lrpe9r7mLgk25xY1pbMamZKOaMv7hT
PkDIRq1CvurpMa7QGQIDAQAB
-----END PUBLIC KEY-----" > moe_pubkey.pem

echo "-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDSK1tQG94Q2wlpIsBqHVYDkc/Q
pM+oEowK2JyddIlopKr/rO54A3ZpSTBLVAMrA5cn6hQafoe7BFQWXQKCag43FZT5
s4BIIS3oD0Nh5F+yNgm+NyDPM0q6kRy0I1FjRKvf2oT2BxiFsNLhFcrOGwEbdsgt
n1WWtRlh5PnoD+8CdwIDAQAB
-----END PUBLIC KEY-----" > larry_pubkey.pem

echo "-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDr8RaVF7olyizNV6lMawu7xBa
Ak7TpyJEX6DWKpQw/q2BchVnBkvKCiKEYqiaPAMDufQUge4LkfDTWVNfqz+7K2zQ
cAyQxQ/d/XVy+6rOp78RzAEZZfkGF02D6yTRtzw8f9smOtkbLiR3MUylTkGy2ON5
wrjaY12SIBpNU0gqQQIDAQAB
-----END PUBLIC KEY-----" > curly_pubkey.pem

echo "SS7k3TumWrVN35rSbxPcKnrD1sgwNQLvs6B7Tqrss7cwFwQYEGVk07u0u49wwY2c
kDyYN4QbL/E4l+Yrpif0bpha5Z9aE2i3Pzmt2t+riopX2s34Voy78Hd6uQR9MQzW
f5GZBCNsD4ofjaPuzopYHtTsAh54+RiNk8wAnS3V75c=" > assinatura.pem

openssl base64 -d -in assinatura.pem -out assinatura.bin

# Algoritmo de Hashing: SHA256
# Algoritmo de Assinatura: RSA

echo "Teste do Moe"
openssl dgst -sha256 -verify moe_pubkey.pem -signature assinatura.bin mensagem.txt
# Verification failure
# 4027AEADEF7B0000:error:0200008A:rsa routines:RSA_padding_check_PKCS1_type_1:invalid padding:../crypto/rsa/rsa_pk1.c:79:
# 4027AEADEF7B0000:error:02000072:rsa routines:rsa_ossl_public_decrypt:padding check failed:../crypto/rsa/rsa_ossl.c:697:
# 4027AEADEF7B0000:error:1C880004:Provider routines:rsa_verify:RSA lib:../providers/implementations/signature/rsa_sig.c:774:

echo "Teste do Larry"
openssl dgst -sha256 -verify larry_pubkey.pem -signature assinatura.bin mensagem.txt
# Verified OK

echo "Teste do Curly"
openssl dgst -sha256 -verify curly_pubkey.pem -signature assinatura.bin mensagem.txt
# Verification failure
# 4017B40A47790000:error:0200008A:rsa routines:RSA_padding_check_PKCS1_type_1:invalid padding:../crypto/rsa/rsa_pk1.c:79:
# 4017B40A47790000:error:02000072:rsa routines:rsa_ossl_public_decrypt:padding check failed:../crypto/rsa/rsa_ossl.c:697:
# 4017B40A47790000:error:1C880004:Provider routines:rsa_verify:RSA lib:../providers/implementations/signature/rsa_sig.c:774: