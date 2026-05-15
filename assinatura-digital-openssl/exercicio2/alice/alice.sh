#!/bin/bash -x
echo "Alice gera as chaves pública e privada"
openssl genrsa -out alice_key.pem 2048
openssl rsa -in alice_key.pem -pubout -out alice_pubkey.pem

echo "Alice assina a mensagem com a chave privada"  
echo "Mensagem de Alice" > alice.txt
openssl dgst -sha256 -sign alice_key.pem -out alice.sign alice.txt

echo "Alice envia a mensagem e a assinatura para Bob"
cp alice.txt ../bob
cp alice.sign ../bob
cp alice_pubkey.pem ../bob
