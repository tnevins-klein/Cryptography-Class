from itertools import cycle
from typing import Dict

def singleByteXor(text: bytearray, b: int) -> bytearray:
    out = bytearray()

    for i in text:
        out.append(i ^ b)

    return out


def vigenere(text: bytearray, key: bytearray) -> bytearray:
    out = bytearray()

    for i, j in zip(text, cycle(key)):
        out.append(i ^ j)

    return out


def write_ctext_file(ptext: str, key: bytearray, fname: str) -> None:
    pbytes = bytearray(ptext, 'utf-8')
    cbytes = vigenere(pbytes, key)

    with open(fname, 'wb') as f:
        f.write(cbytes)


def read_ctext_file(key: bytearray, fname: str) -> bytearray:
    with open(fname, 'rb') as f:
        cbytes = bytearray(f.read())
        ptext = vigenere(cbytes, key)
        return ptext


def byte_counts(data: bytearray) -> Dict[int, int]:
    out = {b: 0 for b in data}  # Initialize a count of zero for each byte that appears in the data.
    for b in data:
        out[b] += 1  # Count how many times each byte appears.
    return out


def byte_ranks(data: bytearray) -> bytearray:
    counts = sorted(byte_counts(data).items(),  # Convert dictionary to a list of tuples
                    key=lambda item: item[1],  # Sort on the second item in the tuple (the count)
                    reverse=True  # Reverse order (more common bytes first)
                    )
    return bytearray([k[0] for k in counts])  # Throw away the counts, return bytes as a bytearray


def english_score(test: bytearray, english: bytearray, penalty=1000) -> int:
    return sum([english.index(b) if b in english  # The score of a byte is its position in the english ranks
                else penalty  # If a character does not appear in english then assign a high score
                for b in test])  # Add up the scores from each individual byte in test


def gen_english_ranks(infile='pg2701.txt') -> bytearray:
    with open('pg2701.txt', 'rb') as f:
        data = f.read()
    return byte_ranks(data)


def break_single_byte(cbytes: bytearray, eng_ranks: bytearray) -> (int, bytearray):
    min_score, best_guess, valid_key = float('inf'), bytearray(), 0
    for key in range(0, 255):
        attempt = singleByteXor(cbytes, key)
        
        if (score := english_score(attempt, eng_ranks)) < min_score:
            min_score = score
            best_guess = attempt
            valid_key = key
            print(attempt.decode('utf-8', errors='ignore')[:20], "score", score, "key", hex(key), sep='\t')

    return (valid_key, best_guess)
    
def every_nth_byte(array, n, m):
    return array[m::n]

def decrypt_vingere(cbytes, ranks, KEY_LENGTH=4):
    keys = []
    messages = []
    
    for key_byte in range(KEY_LENGTH):
        messages.append(cbytes[key_byte::KEY_LENGTH])

    for i in range(len(messages)):
        key, messages[i] = break_single_byte(messages[i], ranks)
        keys.append(key)

    out = []
    for index in range(sum([len(message) for message in messages])):
        out.append(messages[index % KEY_LENGTH][index // KEY_LENGTH])

    print("\n" + bytearray(out).decode('utf-8'))
    print("key:", bytearray(keys).decode())

    return bytearray(out), bytearray(keys)


def decrypt_vingere_guess(cbytes, ranks):
    best_keylen = 1
    best_d = float('inf')

    print("len\td")
    for key_length in range(2, 40):
        d = 1/key_length * hamming_distance(cbytes[:key_length], cbytes[key_length:2*key_length])
        print(key_length, round(d, 2), sep='\t')
        if d < best_d:
            best_d = d
            best_keylen = int(key_length)

    print("Guessed keylength:", best_keylen)
    print()

    return decrypt_vingere(cbytes, ranks, KEY_LENGTH=best_keylen)
    

def hamming_distance(a: bytearray, b: bytearray):
    return sum([bin(x ^ y).count("1") for x, y in zip(a, b)])


def main():
    cbytes = read_ctext_file([0b00000000], 'the.bin', )
    eng_ranks = gen_english_ranks()

    # decrypt_vingere(cbytes, eng_ranks)
    decrypt_vingere_guess(cbytes[8:], eng_ranks)



def main_enc():
    plaintext = """In the context of this Game Manual, Teams contain three types of Student roles related to Robot build, design, and programming. See <G2> and <G4> for more information.Adults may not fulfill any of these roles.
Builder – The Student(s) on the Team who assemble(s) the Robot.Adults are permitted to teach the Builder(s) how to use concepts or tools associated with Robot construction, but may never work on the Robot without the Builder(s) present and actively participating. 
Designer – The Student(s) on the Team who design(s) the Robot. Adults are permitted to teach the Designer(s) how to use concepts or tools associated with design, but may never work on the design of the Robot without the Designer(s) present and actively participating. 
Programmer – The Student(s) on the Team who write(s) the computer code that is downloaded onto the Robot. Adults are permitted to teach the Programmer(s) how to use concepts or tools associated with programming, but may never work on the code that goes on the Robot without the Programmer(s) present and actively participating.
"""
    
    b = plaintext.encode('utf-8')
    with open('the.bin', 'wb') as f:
        f.write(vigenere(b, "vexyss".encode()))
        
if __name__ == '__main__':
    main()
