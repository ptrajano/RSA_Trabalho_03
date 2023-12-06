from random import randrange
from hashlib import sha3_256

BIT_SIZE = 1024
"""
Constante Inteira utilizada para calcular o tamanho do número que será gerado 
"""

gnrt_r_n_bit = lambda n: randrange(2**(n - 1) + 1, 2**n - 1)
"""
Gera um número inteiro aleatório com n bits.

Parâmetros:
- n (int): O número de bits no inteiro aleatório gerado.

Retorna:
int: Um número inteiro gerado aleatoriamente com n bits.
"""

convert_text = lambda text: [ord(char) for char in text]
"""
Converte um texto para um vetor com os códigos unicodes correspondentes do caractér.

Parâmetros:
- text (str): Texto que será convertido.

Retorna:
list: Vetor contendo os códigos unicodes.
"""

encrypt = lambda message, public_key: [pow(chr, public_key[0], public_key[1]) for chr in message]
"""
Criptografa uma mensagem com a chave publica passada.

Parâmetros:
- message (str): Mensagem que será criptografada.
- public_key (tuple): Chave pública do usuário.

Retorna:
list: Mensagem criptografada.
"""

decrypt_vect = lambda encrypted_message, private_key: [pow(char, private_key[0], private_key[1]) for char in encrypted_message] 
"""
Retorna um vetor de caracteres decifrado a partir de uma mensagem encrpitografada utilizando a chave privada passada.

Parâmetros:
- encrypted_message (list): Mensagem encriptografada.
- private_key (tuple): Chave privada do usuário.

Retorna:
list: Vetor de caracteres que serão utilizados para decifrar a mensagem.
"""

decrypt = lambda encrypted_message, private_key: ''.join(chr(number) for number in decrypt_vect(encrypted_message, private_key)) 
"""
Retorna a mensagem a partir de uma mensagem encrpitografada utilizando a chave privada passada.

Parâmetros:
- encrypted_message (list): Mensagem encriptografada.
- private_key (tuple): Chave privada do usuário.

Retorna:
str: Mensagem decifrada.
"""

def read_file(path):
    """
    Retorna o conteúdo de um arquivo a partir de seu caminho.

    Parâmetros:
    - path (str): Caminho do arquivo que será lido.

    Retorna:
    str: Conteúdo do arquivo.
    """
    with open(path, 'r') as file:
        text = file.read()
    return text

def gdc(a, b):
    """
    Retorna um booleano indicando se o máximo divisor comum de dois números é um.

    Parâmetros:
    - a (int): Primeiro número que se calculará o mmc.
    - b (int): Segundo número que se calculará o mmc.

    Retorna:
    bool: Retorna caso os números são coprimos.
    """
    while b != 0:
        a, b = b, a%b
    return a == 1

def divisible_small_prime(number):
    """
    Retorna um booleano indicando se o número é divisivel por um primo pequeno (até 1000).

    Parâmetros:
    - number (int): Número que será analisado.

    Retorna:
    bool: Retorna se o número é divisivel ou não por um primo pequeno.
    """
    primes = [2,29,67,107,157,199,257,311,367,421,467,541,599,647,709,769,829,887,967]
    for prime in primes:
        if number % prime == 0:
            return True
    return False

def trialComposite(number, round_tester, max_2_division, even_n): 
    """
    Testa se um número é composto.

    Parâmetros:
    - number (int): Número que será analisado.
    - round_tester (int): Testador aleatório.
    - max_2_division (int): O número máximo de divisões por 2 permitidas durante o teste.
    - even_n (int): O valor de n para o qual o número é expresso como 2^n * even_n.

    Retorna:
    bool: Retorna caso o número for considerado composto.
    """
    if pow(round_tester, even_n, number) == 1: 
        return False

    for i in range(max_2_division): 
        if pow(round_tester, 2**i * even_n, number) == number - 1: 
            return False
    
    return True

def Miller_Rabin_test(number):
    """
    Realiza o teste de primalidade de Miller-Rabin.

    Parâmetros:
    - number (int): Número que será analisado.

    Retorna:
    bool: Retorna caso o número for considerado provavelmente primo.

    Nota:
    O teste de Miller-Rabin é uma abordagem probabilística para determinar se o número é provavelmente primo.
    """
    max_2_division = 0
    even_n = number - 1
    while even_n % 2 == 0: 
        even_n >>= 1
        max_2_division += 1
   
    for i in range(20): 
        round_tester = randrange(2, number)

        if trialComposite(number, round_tester, max_2_division, even_n): 
            return False

    return True

def generate_n_bit_random_prime():
    """
    Retorna um número primo de tamanho BIT_SIZE.

    Retorna:
    int: Retorna o número provavel primo.
    """
    while True:
        r_number = gnrt_r_n_bit(BIT_SIZE)
        if divisible_small_prime(r_number):
            continue

        if Miller_Rabin_test(r_number):
            break

    return r_number

def generate_coprime(phi_n):
    """
    Retorna um número coprimo do valor da entrada de tamanho BIT_SIZE.

    Parâmetros:
    - phi_n (int): Número que terá um coprimo gerado

    Retorna:
    int: Retorna o número coprimo de phi_n.
    """
    while True:
        r_number = gnrt_r_n_bit(BIT_SIZE)
        if r_number >= phi_n:
            continue

        if gdc(phi_n, r_number):
            break
    return r_number 

def extended_gcd(a, b):
    """
    Calcula o máximo divisor comum estendido de dois.

    Parâmetros:
    - a (int): O primeiro número inteiro.
    - b (int): O segundo número inteiro.

    Retorna:
    tuple: Uma tupla contendo o MDC de a e b, e os coeficientes x e y.
    """
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def modinv(e, phi_n):
    g, x, _ = extended_gcd(e, phi_n)
    if g != 1:
        return 0
    else:
        return x % phi_n

def generate_private_key(e, phi_n):
    """
    Calcula o inverso multiplicativo número em relação a outro.

    Parâmetros:
    - e (int): O número para o qual o inverso mutiplicativo é calculado.
    - phi_n (int): O valor que será comparado.

    Retorna:
    int: O inverso multiplicativo de e em relação a phi_n.
    """
    while True:
        d = modinv(e, phi_n)
        if d != 0:
            break
    return d

def generate_p_q():
    """
    Retorna dois números primos de tamanho BIT_SIZE diferentes.

    Retorna:
    tuple: Retorna os números primos.
    """
    p = generate_n_bit_random_prime()
    while True:
        q = generate_n_bit_random_prime()
        if p != q:
            break
    return p, q  

def sign_message(message, private_key):
    """
    Assina uma mensagem utilizando a chave privada fornecida.

    Parâmetros:
    - message (str): A mensagem que será assinada.
    - private_key (tuple): A chave privada que assinará a mensagem.

    Retorna:
    int: A assinatura da mensagem calculada utilizando a chave privada.
    """
    return pow(int.from_bytes(sha3_256(''.join(message).encode('utf-8')).digest(), byteorder='big'), private_key[0], private_key[1])

def verify_signature(message, signature, public_key):
    """
    Verifica se a assinatura de uma mensagem é válida utilizando a chave pública.

    Parâmetros:
    - message (str): A mensagem que a assinatura será verificada.
    - signature (int): A assinatura que seŕa verificada.
    - public_key (tuple): chave publica que verificará à assinatura.

    Retorna:
    bool: True se a assinatura for válida, False caso contrário.
    """
    return pow(signature, public_key[0], public_key[1]) == int.from_bytes(sha3_256(''.join(message).encode('utf-8')).digest(), byteorder='big')    

def main():
    p, q = generate_p_q()

    n = p * q

    phi_n = n - p - q + 1

    e = generate_coprime(phi_n)

    d = generate_private_key(e, phi_n)

    public_key = (e, n)
    private_key = (d, n)

    text = read_file('texto.txt')
    binary_text = convert_text(text)
    
    signature = sign_message(binary_text, private_key)

    if not verify_signature(binary_text, signature, public_key):
        print("ASSINATURA INVALIDA")
        return

    encrypted_text = encrypt(binary_text, public_key)
    decrypted_text = decrypt(encrypted_text, private_key)

    print(decrypted_text)

if __name__ == '__main__':
    main()