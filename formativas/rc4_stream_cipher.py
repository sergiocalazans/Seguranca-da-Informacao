from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.decrepit.ciphers.algorithms import ARC4

def ksa(key: bytes) -> list[int]:
    """
    Key-Scheduling Algorithm (KSA) for RC4.
    """
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def prga(S: list[int], length: int) -> bytes:
    """
    Pseudo-Random Generation Algorithm (PRGA) for RC4.
    """
    i = 0
    j = 0
    keystream = []
    for _ in range(length):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        keystream_byte = S[(S[i] + S[j]) % 256]
        keystream.append(keystream_byte)
    return bytes(keystream)

def xor_bytes(data: bytes, keystream: bytes) -> bytes:
    return bytes(d ^ k for d, k in zip(data, keystream))

def testa_keystream(chave: str, mensagem: str):
    # Este código é para mostrar o keystream
    chave = chave.encode()
    msg = mensagem.encode()
    S = ksa(chave)
    keystream = prga(S, len(msg))
    print(f'{"Keystream:":24} {keystream.hex()}')
    print(f'{"Mensagem em Plaintext:":24} {msg.hex()}')
    print(f'{"Mensagem cifrada:":24} {xor_bytes(msg, keystream).hex()}')
    


def testa_RC4():

  while True:

      chave = input('Digite a chave secreta: ')
      if not chave:
          break

      chave = chave.encode() # chave em bytes
      allowed = {5, 7, 8, 10, 16, 24, 32}  # bytes

      if len(chave) not in allowed:
          print("Tamanho de chave inválido para ARC4.")
          continue

      # meu_cipher = Cipher( algorithms.ARC4(chave), mode=None)
      meu_cipher = Cipher(ARC4(chave), mode=None)
      cifrador = meu_cipher.encryptor()
      decifrador = meu_cipher.decryptor()

      mensagem = input('Digite a mensagem: ').encode()
      ciphertext = cifrador.update(mensagem)

      print('Mensagem cifrada: ', ciphertext.hex())

      plaintext = decifrador.update(ciphertext)
      print('Mensagem decifrada: ', plaintext.decode())


print('\nO Keystream é uma chave pseudorandomica que tem o tamanho da mensagem')
testa_RC4()