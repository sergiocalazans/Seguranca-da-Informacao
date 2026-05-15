#!/bin/bash -x
echo "Bob verifica a mensagem de Alice usando a chave pública"
openssl dgst -sha256 -verify alice_pubkey.pem -signature alice.sign alice.txt