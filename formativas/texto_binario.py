# 1) cria o arquivo como TEXTO
f = open('teste.txt','w')
tamanho = f.write('49192')
print('Este arquivo tem ', tamanho, 'bytes')
f.close()

# 2) cria o arquivo como BINARIO
f = open('testeb.txt','wb')
print('Representação de 49192 em HEXA: ', format(49192,'1x'))
tamanho = f.write(bytearray([0xc0, 0x28]))
print('Este arquivo tem ', tamanho, 'bytes')
f.close()

# 3) abre o arquivo em modo TEXTO
f = open('teste.txt','r')
print('texto como texto: ', f.read())
f.close()

# 4) abre o arquivo em modo BINARIO
f = open('testeb.txt','rb')
res = f.read()
print('binario como binario: ', res)
print('o print anterior interpretou os bytes como caracteres')
print('abaixo, os bytes estão sendo intepretado como hexa')
for i in res:
    print(format( i, 'x' ))
f.close()

# Exercicio 1: o que acontece se você abrir o arquivo testeb.txt com o notepad?
# Exercicio 2: como interpretar o resultado do passo 4?
# Exercicio 3: qual desses formatos é texto: PDF, DOC, HTML, JSON

