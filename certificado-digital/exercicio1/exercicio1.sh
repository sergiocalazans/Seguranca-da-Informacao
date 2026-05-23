#!/bin/bash -x

# a) Gerar uma chave privada
openssl genpkey -algorithm RSA -out chave_privada.pem -pkeyopt rsa_keygen_bits:2048

# b) Gerar um CSR (Certificate Signing Request)
openssl req -new -key chave_privada.pem -out pedido.csr \
-subj "/C=BR/ST=Parana/L=Curitiba/O=Universidade/OU=Redes/CN=www.exemplo.com/emailAddress=teste@exemplo.com"

# c) Mostrar o conteúdo do CSR
openssl req -in pedido.csr -noout -text

# d) Verificar a validade do CSR
openssl req -in pedido.csr -noout -verify

# e) Criar um certificado autoassinado
openssl x509 -req -in pedido.csr -signkey chave_privada.pem -out certificado.crt -days 365

# f) Mostrar o conteúdo do certificado
openssl x509 -in certificado.crt -noout -text
