# EXERCICIO 2. Assinatura Digital de Chave Pública
## Complete os seguintes passos no script abaixo conforme as instruções:

---
## PASSO 1: CRIE A ESTRUTURA DE PASTA CONFORME INDICADO

rm -R -f exercicio2
mkdir exercicio2
cd exercicio2
mkdir alice
mkdir bob
mkdir charles

---
## PASSO 2: SCRIPT alice.sh (coloque na pasta alice)

#!/bin/bash -x
echo "Alice gera as chaves pública e privada"
echo "Alice assina a mensagem com a chave privada"  
echo "Alice envia a mensagem e a assinatura para Bob"

---
## PASSO 3: SCRIPT bob.sh (coloque na pasta bob)
#!/bin/bash -x
echo "Bob verifica a mensagem de Alice usando a chave pública"
 
---
## PASSO 4: SCRIPT charles1.sh (coloque na pasta charles)
#!/bin/bash -x
echo "Charles (man-in-the-middle) intercepta a assinatura enviada por Alice"
echo "Charles envia uma mensagem falsa para Bob com a assinatura de Alice"  

---
## PASSO 5: SCRIPT charles2.sh (coloque na pasta charles)
#!/bin/bash -x
echo "Charles gera a chave privada"
echo "Charles gera uma mensagem falsa para Bob assinada com sua chave privada"  
echo "Charles envia a mensagem falsa com sua assinatura para Bob dizendo-se Alice"

---
## USE OS COMANDOS ABAIXO PARA COMPLETAR O EXERCICIO

---
## Ações da Alice:

openssl genrsa -out alice_key.pem 2048
openssl rsa -in alice_key.pem -pubout -out alice_pubkey.pem
echo "Mensagem de Alice" > alice.txt
openssl dgst -sha1 -sign alice_key.pem -out alice.sign alice.txt
cp alice_pubkey.pem ../bob
cp alice.txt ../bob
cp alice.sign ../bob

---
## Ações do Bob:

openssl dgst -sha1 -verify alice_pubkey.pem -signature alice.sign alice.txt

---
## Ações do Charles (Ataque 1):

cp ../alice/alice.sign .
echo "Mensagem falsa da Alice" > alice.txt
cp alice.txt ../bob
cp alice.sign ../bob

---
## Ações do Charles (Ataque 2):
echo "Mensagem falsa da Alice 2" > alice.txt
openssl genrsa -out charles_key.pem 2048
openssl dgst -sha1 -sign charles_key.pem -out alice.sign alice.txt
cp alice.txt ../bob
cp alice.sign ../bob
