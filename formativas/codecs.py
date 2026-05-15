codec = 'utf-16'
texto = 'mas é muita emoção'
try:
    embytes = texto.encode(codec)
    print('em bytes:', embytes)
    print('em hexa:', embytes.hex())
    print('em string:', embytes.decode(codec))
except Exception as e:
    print(e, 'não consigo representar isso')  

# OBS:
# utf-16: adiciona um BOM FFFE no início do código
# char: assume que o código convertido é UNICODE

# Exercicio 1: teste os codecs ansi, utf-8 e utf-16?
# Exercicio 2: verifique em que condições ascii não funciona.