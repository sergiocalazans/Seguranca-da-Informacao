import comparaRC4AES as AES
import os
from base64 import b64encode

'''
EXERCICIO: 

Faça as chamadas para criptografar e descriptografar com AES em cada um dos 4 modos: ECB, CBC, CTR e GCM 
O modo ECB foi fornecido como exemplo. Inclua o teste para os outros 3 modos CBC, CTR e GCM 
plaintext = 'TESTE DA EQUIPE X' ou 'TESTE DO ESTUDANTE XX' 

PARA ENTREGAR A ATIVIDADE COPIE O RESULTADO DO PRINT NO FINAL DO ARQUIVO

'''
    
msg = 'TESTE DO ESTUDANTE SÉRGIO HENRIQUE DA CUNHA CALAZANS'    
plaintext = msg.encode('UTF-8')

if len(plaintext) % 16 != 0:
    plaintext = plaintext + bytearray(16 - len(msg)%16)
    
chave = os.urandom(16)

# Copie e modifique esta seção para os 3 modos restantes
#-----------------------------------------------------

# Lista dos modos
modos = ['ECB', 'CBC', 'CTR', 'GCM']

# Iteração para cada modo
for modo in modos:

    print(f'\nTESTE DO MODO {modo}')
    print( 'chave:', [ b for b in chave ] )

    # Padding manual para modos de bloco (ECB, CBC)
    if modo in ['ECB', 'CBC'] and len(plaintext) % 16 != 0:
            padding_len = 16 - (len(plaintext) % 16)
            plaintext += bytearray([padding_len] * padding_len)

    try:
        ciphertext, iv, tag = AES.cifra_AES(plaintext, chave, modo)

        if iv is not None: print( 'iv:', [ b for b in iv ] )
        if tag is not None: print( 'tag:', [ b for b in tag ] )
        print('Ciphertext (B64):', b64encode(ciphertext).decode())

        # Adição dos parâmetros iv e tag
        # ECB não usa iv e nem tag
        # CBC e CTR usam iv
        # GCM usa iv e tag
        '''

        Como na função cifra_AES retorna None para os modos que não usa iv ou tag,
        então, adicionei iv e tag diretamente na função decifra_AES.

        Além disso, na definição da função decifra_AES, iv e tag são definidos como None, 
        assim não é obrigatório o uso desses parâmetros.
        
        '''
        plaintext = AES.decifra_AES(ciphertext, chave, modo, iv, tag)
        print('Plaintext:', plaintext.decode())

    except Exception as e:    
        print(e)
#-----------------------------------------------------
'''
--------------------------------------------------------------------------------------------------------
COLOQUE O PRINT COM OS RESULTADOS AQUI

TESTE DO MODO ECB
chave: [68, 27, 11, 186, 92, 49, 175, 17, 178, 203, 127, 38, 184, 234, 16, 179]
O modo ECB critografa cada bloco separadamente
Ciphertext (B64): sKJMUiLFixLruH8Qr2lOWC9cTift6jIrCjZ44rLkVV/K8wkR1mziVATjhN3U8YNSyWP07ifspuxAIv2xHRSQn/yJrAoqwkr9UeIhe7PSmhg=
Plaintext: TESTE DO ESTUDANTE SÉRGIO HENRIQUE DA CUNHA CALAZANS

TESTE DO MODO CBC
chave: [68, 27, 11, 186, 92, 49, 175, 17, 178, 203, 127, 38, 184, 234, 16, 179]
O modo CBC faz um XOR de cada bloco com o anterior e cria um problema de paralelismo
iv: [182, 98, 140, 251, 69, 197, 21, 189, 27, 41, 134, 222, 196, 202, 218, 252]
Ciphertext (B64): gY+fcMZ6GbfdHTN1ug25y7+K1i68WJ4cS2uVUlrut3lHqFdO5zMZqCjqXGoAAzm4uyG8hKQFDg3/WXnEt/Z1u7HJPJsfkVupLgghSOktygE=
Plaintext: TESTE DO ESTUDANTE SÉRGIO HENRIQUE DA CUNHA CALAZANS

TESTE DO MODO CTR
chave: [68, 27, 11, 186, 92, 49, 175, 17, 178, 203, 127, 38, 184, 234, 16, 179]
O modo CTR usa o AES para gerar um keystream para um XOR cipher
iv: [3, 223, 64, 192, 214, 133, 164, 248, 11, 67, 164, 234, 114, 14, 187, 139]
Ciphertext (B64): O+8/Gn0R9NsPc+QpanLGvua4uU9RPPmn6dPFZ/X3vT3ti+omRgvsOONsKrzftDLbUWuHAAZ+VpxvjUWPOWoc9Zt9y9kw0sFcUvU0XKqSXws=
Plaintext: TESTE DO ESTUDANTE SÉRGIO HENRIQUE DA CUNHA CALAZANS

TESTE DO MODO GCM
chave: [68, 27, 11, 186, 92, 49, 175, 17, 178, 203, 127, 38, 184, 234, 16, 179]
O modo GCM é similar ao CTC mais adiciona um tag de autenticacao
iv: [64, 99, 164, 91, 61, 162, 204, 111, 122, 220, 162, 195, 153, 37, 23, 244]
tag: [15, 190, 223, 65, 40, 248, 170, 220, 130, 201, 200, 34, 190, 150, 175, 41]
Ciphertext (B64): Q/B6OajmFkXUrNUx6XaZT0uq2Midst5kNddy7O3pwlI9prwNDSveKi+te5o5HjXJq4dDlYKjTEo0vwiI33MXOmiflaLSBsegpv0sWdpv+k8=        
Plaintext: TESTE DO ESTUDANTE SÉRGIO HENRIQUE DA CUNHA CALAZANS

'''