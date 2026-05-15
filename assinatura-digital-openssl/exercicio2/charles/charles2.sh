#!/bin/bash -x
echo "Charles gera a chave privada"
openssl genrsa -out charles_key.pem 2048

echo "Charles gera uma mensagem falsa para Bob assinada com sua chave privada"  
echo "Mensagem falsa da Alice 2" > alice.txt
openssl dgst -sha256 -sign charles_key.pem -out alice.sign alice.txt

echo "Charles envia a mensagem falsa com sua assinatura para Bob dizendo-se Alice"
cp alice.txt ../bob
cp alice.sign ../bob
