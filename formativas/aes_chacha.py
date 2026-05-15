from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import b64encode
import os

def cipherChaCha20(msg, key):
    # ChaCha20 requer um Nonce de 16 bytes (128 bits)
    nonce = os.urandom(16)
    
    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None) # ChaCha20 não usa modos como CBC/ECB
    
    # Cifragem
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(msg)
    
    print(f"Nonce (HEX): {nonce.hex()}")
    print("Ciphertext (B64):", b64encode(ciphertext).decode())
    print("Ciphertext (BYTES):", [c for c in ciphertext])

    # Decifragem (Exige o mesmo Nonce e Chave)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext)
    print("Plaintext (Decoded):", plaintext.decode())

def testaChaCha20():
    # ChaCha20 utiliza chaves de 256 bits (32 bytes)
    print("--- Teste ChaCha20 (Stream Cipher) ---")
    segredo = input('Digite a senha (será preenchida/truncada para 32 bytes): ')
    
    # Ajuste da chave para 32 bytes (256 bits)
    key = segredo.encode().ljust(32, b'\0')[:32]
    print(f'CHAVE (HEX): {key.hex()}')

    while True:
        msg = input('\nDigite a mensagem: ')
        if not msg:
            print('Saindo...')
            break
        
        try:
            cipherChaCha20(msg.encode(), key)
        except Exception as e:
            print(f"Erro: {e}")
            break

def cifra_AES(plaintext, key, modo):
    if modo == 'ECB':
        print('O modo ECB criptografa cada bloco separadamente (Inseguro para padrões)')
        iv = None
        cipher = Cipher(algorithms.AES(key), modes.ECB())
    elif modo == 'CBC':
        print('O modo CBC faz um XOR de cada bloco com o anterior (Requer IV)')
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    elif modo == 'CTR':
        print('O modo CTR transforma o AES em um cifrador de fluxo')
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv))
    elif modo == 'GCM':
        print('O modo GCM oferece cifragem e autenticação (AEAD)')
        iv = os.urandom(12) # GCM tipicamente usa IV de 12 bytes
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
    else:
        raise ValueError(f'O modo {modo} não existe')

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    tag = encryptor.tag if modo == 'GCM' else None
    return ciphertext, iv, tag

def testaAES():
    # AES suporta 128, 192 ou 256 bits
    chave = os.urandom(32) # 256 bits
    print('\n--- Teste AES (Block Cipher) ---')
    print('Chave (HEX):', chave.hex())
    
    modos = ['ECB', 'CBC', 'CTR', 'GCM']
    modo = input(f'Escolha o modo {modos}: ').upper()
    
    if modo not in modos:
        print('Modo inválido')
        return

    while True:
        msg = input('\nDigite a mensagem: ')
        if not msg:
            break
        
        msg_bytes = msg.encode('utf-8')
        
        # Padding manual para modos de bloco (ECB, CBC)
        if modo in ['ECB', 'CBC'] and len(msg_bytes) % 16 != 0:
            padding_len = 16 - (len(msg_bytes) % 16)
            msg_bytes += bytearray([padding_len] * padding_len)
            
        try:
            ciphertext, iv, tag = cifra_AES(msg_bytes, chave, modo)
            if iv: print('IV (HEX):', iv.hex())
            if tag: print('Tag (HEX):', tag.hex())
            print("Ciphertext (B64):", b64encode(ciphertext).decode())
        except Exception as e:
            print(f"Erro: {e}")
            break

if __name__ == "__main__":
    op = input("Escolha o teste: [1] ChaCha20 (Stream) [2] AES (Block): ")
    if op == '1':
        testaChaCha20()
    else:
        testaAES()  