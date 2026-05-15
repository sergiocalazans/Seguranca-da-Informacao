from base64 import b64encode, b64decode

def xor_cipher(plain, key):
    cripto = ""
    for c in plain:
        cripto += chr(ord(c) ^ key)
    return cripto

def xor_cipher_b64(plain, key):
    c_bytes = bytearray()
    for c in plain:
        c_bytes.append(ord(c) ^ key)
    return b64encode(c_bytes).decode("ascii")

def xor_decipher_b64(cipher_b64, key):
    c_bytes = b64decode(cipher_b64)
    plain = ""
    for b in c_bytes:
        plain += chr(b ^ key)
    return plain


chave = 253
plain = "isto é um teste muito estranho"

print("CHAVE:", chave)
print("PLAIN:", plain)

print("\n--- XOR direto ---")
cipher = xor_cipher(plain, chave)
print("CRIPTO:", cipher)
print("DECRIPTO:", xor_cipher(cipher, chave))

# EXERCICIO 1:
# Copie o valor exibido em CRIPTO e cole em cipher2.
# Veja se a descriptografia continua correta.
cipher2 = "Ý¶ÝÝÝÝ"
print("DECRIPTO 2:", xor_cipher(cipher2, chave))

print("\n--- XOR + Base64 ---")
cipher_b64 = xor_cipher_b64(plain, chave)
print("CRIPTO B64:", cipher_b64)
print("DECRIPTO B64:", xor_decipher_b64(cipher_b64, chave))

# EXERCICIO 2:
# Copie o valor exibido em CRIPTO B64 e cole em cipher_b64_2.
# Veja que agora o copiar e colar preserva a informação.
cipher_b64_2 = 'lI6Jkt0U3YiQ3YmYjomY3ZCIlImS3ZiOiY+ck5WS'
print("DECRIPTO B64 2:", xor_decipher_b64(cipher_b64_2, chave))