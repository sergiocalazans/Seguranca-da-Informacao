from base64 import b64encode


def xor_bytes(data, key):
    result = []
    j = 0
    for b in data:
        result.append(b ^ key[j])
        j += 1
        if j == len(key):
            j = 0
    return bytes(result)


def xor_text(text, key):
    data = text.encode("utf-8")
    k = key.encode("utf-8")
    return xor_bytes(data, k)


def teste1():
    while True:
        key = input("entre com a chave: ")
        if not key:
            print("saindo...")
            break

        plain = input("entre com a mensagem: ")

        cipher = xor_text(plain, key)
        print("bytes cifrados:", list(cipher))
        print("base64:", b64encode(cipher).decode())

        decoded = xor_bytes(cipher, key.encode("utf-8")).decode("utf-8")
        print("decripto:", decoded)


def teste2():
    while True:
        key = input("entre com a chave: ")
        if not key:
            print("saindo...")
            break

        plain1 = input("entre com a mensagem 1: ")
        plain2 = input("entre com a mensagem 2: ")

        cipher1 = xor_text(plain1, key)
        cipher2 = xor_text(plain2, key)

        x = xor_bytes(cipher1, cipher2)

        print("c1 xor c2:", list(x))
        print("se eu conheço a mensagem 2, recupero a 1:")
        print(xor_bytes(x, plain2.encode("utf-8")).decode("utf-8"))

        print("se eu conheço a mensagem 1, recupero a 2:")
        print(xor_bytes(x, plain1.encode("utf-8")).decode("utf-8"))


def teste3():
    plain = "voce ofereceu R$ 0001,00 reais pelo meu notebook usado que nao funciona"
    key = input("entre com a chave: ")

    print("mensagem original (plain):", plain)
    cipher = xor_text(plain, key)
    print("mensagem transmitida (base64):", b64encode(cipher).decode())

    inicio = plain.index("0001")
    fim = inicio + 4

    original = "0001".encode("utf-8")
    desejado = "9999".encode("utf-8")

    trecho_cifrado = cipher[inicio:fim]
    mascara = xor_bytes(original, trecho_cifrado)
    novo_trecho = xor_bytes(desejado, mascara)

    cipher_mod = cipher[:inicio] + novo_trecho + cipher[fim:]

    print("mensagem modificada (base64):", b64encode(cipher_mod).decode())
    print("mensagem recuperada:",
          xor_bytes(cipher_mod, key.encode("utf-8")).decode("utf-8"))


teste3()
