# python3 -m pip install cryptography

import base64
import statistics
import time

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def build_message(size: int) -> bytes:
    return bytes((i % 256 for i in range(size)))


def max_rsa_message_size_bytes(bits: int) -> int:
    key_size_bytes = bits // 8
    hash_size_bytes = hashes.SHA256().digest_size
    return key_size_bytes - 2 * hash_size_bytes - 2


def measure_once(bits: int, message_size: int) -> dict:
    message = build_message(message_size)

    t0 = time.perf_counter()
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=bits,
    )
    public_key = private_key.public_key()
    keygen_time = time.perf_counter() - t0

    t1 = time.perf_counter()
    cipher = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    encrypt_time = time.perf_counter() - t1

    b64_text = base64.b64encode(cipher).decode("ascii")

    t2 = time.perf_counter()
    plain = private_key.decrypt(
        base64.b64decode(b64_text.encode("ascii")),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    decrypt_time = time.perf_counter() - t2

    #total_time = keygen_time + encrypt_time + decrypt_time
    total_time = encrypt_time + decrypt_time

    return {
        "bits": bits,
        "message_size": len(message),
        "cipher_size": len(cipher),
        "base64_size": len(b64_text),
        "ok": plain == message,
        "keygen_time": keygen_time,
        "encrypt_time": encrypt_time,
        "decrypt_time": decrypt_time,
        "total_time": total_time,
        "req_per_sec": 1 / total_time if total_time > 0 else float("inf"),
    }


def benchmark_rsa(bits: int, message_size: int, repeats: int = 10) -> None:
    max_msg = max_rsa_message_size_bytes(bits)
    if message_size > max_msg:
        print(f"RSA {bits} bits")
        print(f"message size (bytes): {message_size}")
        print(f"max allowed with OAEP-SHA256: {max_msg}")
        print("message too large for direct RSA encryption")
        print("-" * 40)
        return

    results = [measure_once(bits, message_size) for _ in range(repeats)]

    keygen_times = [r["keygen_time"] for r in results]
    encrypt_times = [r["encrypt_time"] for r in results]
    decrypt_times = [r["decrypt_time"] for r in results]
    total_times = [r["total_time"] for r in results]
    req_rates = [r["req_per_sec"] for r in results]

    ref = results[0]

    print(f"RSA {bits} bits")
    print(f"message size (bytes): {ref['message_size']}")
    print(f"max allowed with OAEP-SHA256: {max_msg}")
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

    for bits in (1024, 2048, 3076):
        benchmark_rsa(bits, message_size, repeats)


if __name__ == "__main__":
    main()