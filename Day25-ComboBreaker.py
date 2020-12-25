def get_loop_size(key:int, subject:int=7, modulo:int=20201227):
    value = 1
    loop = 0
    while value != key:
        value *= subject
        value %= modulo
        loop += 1
    
    return loop

def encrypt(subject:int, loops:int, modulo:int=20201227):
    value = 1
    for _ in range(loops):
        value *= subject
        value %= modulo
    return value

def get_encrypt_key(pk1, pk2):
    loop1 = get_loop_size(pk1)
    return encrypt(pk2, loop1)
    

if __name__ == '__main__':
    with open('input25.txt') as f:
        card_key, door_key = map(int, f.readlines())

    print(get_encrypt_key(card_key, door_key))
