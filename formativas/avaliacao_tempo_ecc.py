# python3 -m pip install cryptography

import base64
import os
import statistics
import time

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def build_message(size: int) -> bytes:
    return bytes((i % 256 for i in range(size)))


def derive_aes_key(shared_secret: bytes) -> bytes:
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"didactic-ecc-demo",
    ).derive(shared_secret)


def measure_once(curve, message_size: int) -> dict:
    message = build_message(message_size)

    # Geração das chaves efêmeras do emissor e do receptor
    t0 = time.perf_counter()
    sender_private = ec.generate_private_key(curve)
    receiver_private = ec.generate_private_key(curve)
    keygen_time = time.perf_counter() - t0

    sender_public = sender_private.public_key()
    receiver_public = receiver_private.public_key()

    # "Cripto": ECDH + HKDF + AES-GCM encrypt
    t1 = time.perf_counter()
    shared_secret_enc = sender_private.exchange(ec.ECDH(), receiver_public)
    aes_key_enc = derive_aes_key(shared_secret_enc)
    aesgcm_enc = AESGCM(aes_key_enc)
    nonce = os.urandom(12)
    cipher = aesgcm_enc.encrypt(nonce, message, None)
    encrypt_time = time.perf_counter() - t1

    payload = nonce + cipher
    b64_text = base64.b64encode(payload).decode("ascii")

    # "Decripto": ECDH + HKDF + AES-GCM decrypt
    t2 = time.perf_counter()
    shared_secret_dec = receiver_private.exchange(ec.ECDH(), sender_public)
    aes_key_dec = derive_aes_key(shared_secret_dec)
    aesgcm_dec = AESGCM(aes_key_dec)
    plain = aesgcm_dec.decrypt(nonce, cipher, None)
    decrypt_time = time.perf_counter() - t2

    total_time = encrypt_time + decrypt_time

    return {
        "curve": curve.name,
        "message_size": len(message),
        "cipher_size": len(payload),
        "base64_size": len(b64_text),
        "ok": plain == message,
        "keygen_time": keygen_time,
        "encrypt_time": encrypt_time,
        "decrypt_time": decrypt_time,
        "total_time": total_time,
        "req_per_sec": 1 / total_time if total_time > 0 else float("inf"),
    }


def benchmark_ecc(curve, message_size: int, repeats: int = 10) -> None:
    results = [measure_once(curve, message_size) for _ in range(repeats)]

    keygen_times = [r["keygen_time"] for r in results]
    encrypt_times = [r["encrypt_time"] for r in results]
    decrypt_times = [r["decrypt_time"] for r in results]
    total_times = [r["total_time"] for r in results]
    req_rates = [r["req_per_sec"] for r in results]

    ref = results[0]

    print(f"ECC curve: {ref['curve']}")
    print(f"message size (bytes): {ref['message_size']}")
    print(f"cipher size (bytes): {ref['cipher_size']}")
    print(f"cipher size (base64 chars): {ref['base64_size']}")
    print(f"decryption ok: {all(r['ok'] for r in results)}")
    print(f"repeats: {repeats}")

    print(f"key generation avg: {statistics.mean(keygen_times):.6f} s")
    print(f"key generation min: {min(keygen_times):.6f} s")
    print(f"key generation max: {max(keygen_times):.6f} s")

    print(f"encryption avg:     {statistics.mean(encrypt_times):.6f} s")
    print(f"decryption avg:     {statistics.mean(decrypt_times):.6f} s")

    print(f"total/request avg:  {statistics.mean(total_times):.6f} s")
    print(f"req/s with new key per access: {statistics.mean(req_rates):.2f}")
    print("-" * 40)


def main() -> None:
    message_size = 32
    repeats = 10

    curves = [
        ec.SECP256R1(),
        ec.SECP384R1(),
        ec.SECP521R1(),
    ]

    for curve in curves:
        benchmark_ecc(curve, message_size, repeats)


if __name__ == "__main__":
    main()