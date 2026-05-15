import random

max_chave = 40000
espaco_chaves = range(1, max_chave)

def cripto(mensagem, chave):
    cripto = ""
    for c in mensagem:
        codigo = ord(c) + chave
        cripto += chr(codigo)
    return cripto

plain = 'Nada de novo no front'
check = hash(plain)
print(f"código de verificação: {check}")

chave = random.randint(1, max_chave)
print(chave)
cipher = cripto(plain, chave)
print(cipher)


# 1) Decodifique a mensagem Sfif%ij%st{t%st%kwtsy

def forca_bruta(cipher, espaco_chaves, check):
    for chave in espaco_chaves:
        
        try:
          plain = cripto(cipher, -chave)
          print(f"{chave}: {plain}")
          if check == hash(plain):
              print(f"A chave certa é {chave}")
              return
        except:
          print(f"A chave é menor que {chave}")
          return

# cipher = 'Sfif%ij%st{t%st%kwtsy'
#forca_bruta(cipher, espaco_chaves, check)        

# 2) Qual o espaço de chaves do algoritmo? Qual o tamanho da chave?
# 3) Este algoritmo mantem padrão, como isso simplifica a quebra da criptografia?
# 4) É possível decifrar a mensagem sem testar todas as chaves?

def analise_frequencia(cipher):
    codigo = [ ord(c) for c in cipher ]
    freq = {}

    for c in codigo:
        if c not in freq:
            freq[c] = 1
        else:
            freq[c] = freq[c] + 1
            
    return sorted(freq.items(), key=lambda item: item[1])


res = analise_frequencia(cipher)
print(res)

h1 = res[-1][0] - ord('a')
h2 = res[-1][0] - ord(' ')
h3 = res[-2][0] - ord('a')
h4 = res[-2][0] - ord(' ')

print()
print(h1)
print(h2)
print(h3)
print(h4)