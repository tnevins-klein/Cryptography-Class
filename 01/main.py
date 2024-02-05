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
    


def main():
    cbytes = read_ctext_file([0b00000000], 'awesome_pt.bin', )
    eng_ranks = gen_english_ranks()
    key, message = break_single_byte(cbytes, eng_ranks)
    print("\n" + message.decode('utf-8', errors='ignore'))


"""
def main():
    b = plaintext.encode('utf-8')
    with open('awesome_pt.bin', 'wb') as f:
        f.write(singleByteXor(b, 49))
"""

if __name__ == '__main__':
    main()
