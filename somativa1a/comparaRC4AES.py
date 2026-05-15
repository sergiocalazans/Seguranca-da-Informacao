# https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import b64encode
import os


def cipherRC4(msg, chave):
    algorithm = algorithms.ARC4(chave)
    cipher = Cipher(algorithm, mode=None)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(msg)
    print("Ciphertext (B64):", b64encode(ciphertext))
    print("Ciphertext (BYTES):", [c for c in ciphertext] )
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext)
    print("Plaintext (Decoded):", plaintext.decode())


def chave_iv(segredo, size):
    ivsize = size - len(segredo)*8
    ivsize = int(ivsize/8)
    chave = segredo + os.urandom(ivsize)
    print(f'CHAVE: {[c for c in chave ]}')
    return chave


def testaRC4():
    # pode se usar chaves de 40, 56, 64, 80, 128, 192 ou 256 bits
    segredo = input('\nDigite a chave: ')
    segredo = segredo.encode()
    chave = segredo

    while True:
        # chave = chave_iv(segredo, 128)
        msg = input('\nDigite a mensagem: ')
        if not msg:
            print('bye my friend!!!')
            break
        msg = msg.encode()
        try: 
            cipherRC4(msg, chave)
        except Exception as e:
            print(e)
            break        

def cifra_AES(plaintext, key, modo):
    
    if modo=='ECB':
        print('O modo ECB critografa cada bloco separadamente')
        iv = None
        cipher = Cipher(algorithms.AES(key), modes.ECB())        
    elif modo == 'CBC':
        print('O modo CBC faz um XOR de cada bloco com o anterior e cria um problema de paralelismo')
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))        
    elif modo == 'CTR':
        print('O modo CTR usa o AES para gerar um keystream para um XOR cipher')
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv))  
    elif modo == 'GCM':
        print('O modo GCM é similar ao CTC mais adiciona um tag de autenticacao')
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv))  
    else:
        raise(f'O modo {modo} não existe')
    
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    if modo == 'GCM':
        tag = encryptor.tag
    else: 
        tag = None
    
    return ciphertext, iv, tag


def decifra_AES(ciphertext, key, modo, iv=None, tag=None):

    if modo=='ECB':
        cipher = Cipher(algorithms.AES(key), modes.ECB())        
    elif modo == 'CBC':        
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))        
    elif modo == 'CTR':        
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv))  
    elif modo == 'GCM':
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))  
    else:
        raise(f'O modo {modo} não existe')

    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext



def testaAES():
    # pode se usar chaves de 128, 192 ou 256 bits
    chave = os.urandom(16)
    print( 'chave:', [ b for b in chave ] )
    modos = ['ECB', 'CBC', 'CTR', 'GCM']
    modo = None
    while modo not in modos:
        modo = input(f'Escolha o modo {modos}: ')
        if modo not in modos:
            print('Modo inválido')        
        
    while True:

        msg = input('\nDigite a mensagem: ')
        if not msg:
            print('bye my friend!!!')
            break
        msg = msg.encode('utf-8')

        # Completa o último bloco se não for multiplo de 16 bytes
        if len(msg) % 16 != 0:
            msg = msg + bytearray(16 - len(msg)%16)
        
        print(f'\nMensagem: {msg} com {len(msg)/16} blocos' )


        try: 
            ciphertext, iv, tag = cifra_AES(msg, chave, modo)

            if iv is not None:
                print( 'iv:', [ b for b in iv ] )
            else:
                print('Este modo não usa iv')

            if tag is not None:
                print( 'tag:', [ b for b in iv ] )
            else:
                print('Este modo não gera tag de autenticação')

            print("Ciphertext (B64)", b64encode(ciphertext))
            print("Ciphertext (BYTES)", [c for c in ciphertext])
        except Exception as e:
            print(e)
            break    
    



if __name__ == "__main__":    
    testaRC4()    
    #testaAES()




    



