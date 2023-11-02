from Crypto.Random import get_random_bytes


def get_salt(iterations):
    if type(iterations) != int:
        raise TypeError
    for i in range(iterations):
        print(get_random_bytes(32))



get_salt(10000000)