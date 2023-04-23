import random
from math import gcd
import base64


def byte_length(n):
    return (n.bit_length() + 7) // 8

def is_prime(num):  # fast
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num ** 0.5) + 2, 2):
        if num % n == 0:
            return False
    return True

def find_two_primes():
    a = random.randint(2000, 9999)
    while not is_prime(a):
        a += 1 
    check = True
    while check:
        b = random.randint(2000, 9999)
        while (not is_prime(b)):
            b += 1
        if b != a:
            check = False
    return (a, b)

def genkey():
    p, q = find_two_primes()
    n = p * q
    m = (p - 1) * (q - 1)
    e = random.randint(200, 1999)  
    while gcd(e, m) != 1:   
        e = random.randint(200, 1999)
    d = pow(e, -1, m) # d = e^-1 mod m
    return (e, n, d)


def padding(data, byte_len):
    remainder = len(data) % byte_len
    if (remainder != 0):
        data = data + bytes(byte_len - remainder)
    return data


def remove_padding(data, byte_len): 
    index = len(data) - 1
    while (data[index] == 0):
        index -= 1
    return data[0: index + 1]

 
def encrypt(data, key): 
    [k, n] = key
    cipher = bytes()
    # determine block length
    keylen = byte_length(n)
    blocklen = keylen - 1
    data = padding(data, blocklen)
    for i in range(0, len(data), blocklen):
        block = data[i    :     i + blocklen]
        a = int.from_bytes(block) 
        c = int(pow(a, k, n)) # c = a^k mod n
        cipher = cipher + c.to_bytes(keylen)
    return cipher
 
def decrypt(cipher, key): 
    [k, n] = key
    plain = bytes()
    keylen = byte_length(n)
    blocklen = keylen - 1
    for i in range(0, len(cipher), keylen):
        block = cipher[i    :       i + keylen]
        c = int.from_bytes(block)
        a = pow(c, k, n) # a = c^k mod n
        plain = plain + a.to_bytes(blocklen)
    return remove_padding(plain, blocklen)

def encrypt_b64(bytes_data, key): 
    cipher = encrypt(bytes_data, key)
    return base64.b64encode(cipher).decode() 

def decrypt_b64(b64cipher, key): 
    cipher = base64.b64decode(b64cipher)
    return decrypt(cipher, key)