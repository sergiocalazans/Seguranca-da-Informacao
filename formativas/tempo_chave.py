# caso um computador teste 1000 chaves por segundo
# quanto tempo levará para encontrar uma chave de 64 bits por força bruta?

chaves_segundo = (5000000000/100)*256*1000000
tamanho_chave = 128
espaco_chaves = 2**tamanho_chave
tempo = espaco_chaves / chaves_segundo
tempo_dias = tempo / (60*60*24)
tempo_anos = tempo_dias/365

print(f"Tempo: {tempo_anos} anos")
print(f"Tempo: {tempo_dias} dias")