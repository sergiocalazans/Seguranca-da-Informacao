import random as rd

def xor_cipher(plain, key):
    
  cipher = ""
  new_key = key - 1

  for p in plain:
    c = ord(p) ^ new_key
    new_key += rd.randint(0, 5)
    cipher += chr(c)

  return (cipher, new_key)

while True:
    key = input('entre com a chave: ')
    if not key:
        print("saindo ... ")
        break
    else:
        key = int(key)
        plain = input('entre com a mensagem: ')
        cipher, new_key  = xor_cipher(plain, key)
        print("cripto:", cipher)
        print("decripto:", xor_cipher(cipher, key))