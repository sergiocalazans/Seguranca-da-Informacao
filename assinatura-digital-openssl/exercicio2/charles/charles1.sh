#!/bin/bash -x
echo "Charles (man-in-the-middle) intercepta a assinatura enviada por Alice"
cp ../alice/alice.sign .

echo "Charles envia uma mensagem falsa para Bob com a assinatura de Alice"  
echo "Mensagem falsa da Alice" > alice.txt
cp alice.txt ../bob
cp alice.sign ../bob