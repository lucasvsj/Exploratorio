import os
import hashlib


def encriptar(contraseña, sal=None):
    sal = os.urandom(8)
    codificacion = contraseña.encode()
    secuencia = sal + codificacion
    resultado = hashlib.sha256(secuencia)
    return [sal, resultado.digest()]

def desencriptar(sal, contraseña):
    codificacion = contraseña.encode()
    secuencia = sal + codificacion
    resultado = hashlib.sha256(secuencia)
    return resultado.digest()


if __name__ == '__main__':
    c1 = encriptar('qwerty')
    c2 = desencriptar(c1[0], 'qwerty')
    # print(f'{c1[1]}\n{c2}')
    print(c2)
    print(c1[1] == c2)
