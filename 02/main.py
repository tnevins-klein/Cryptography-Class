from matplotlib import pyplot as plt

class lcg:
    def __init__(self, seed, a=1, c=0, m=2**64-1):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m
        self.current_val = seed
        self.counter = 0

    def roll(self):
        self.current_val = (self.a*self.current_val + self.c) % self.m
        self.counter += 1
        return self.current_val
    
    def roll_byte(self):
        return self.roll() % 2**8

    def roll_norm(self):
        return self.roll()/self.m

"""
def main():
    prng = lcg(344, a=16598013, c=12820163, m=2**24)
    sample = [prng.roll_norm() for _ in range(1_000_000)]
    plt.hist(sample, bins=30)
    plt.show()


if __name__ == '__main__':
    main()
"""

def lcg_cipher(bytes: bytearray, seed: int) -> bytearray:
    random_ctx = lcg(seed)
    
    out = bytearray()

    k = random_ctx.roll_byte()

    for byte in bytes:
        out.append(byte ^ k)
        k = random_ctx.roll_byte()

    return out

def main():
    # prng = lcg(3453252345, 723325234)
    # for _ in range(10):
    #    print(prng.roll())

    pt = "https://emojiisland.com/cdn/shop/products/Nerd_with_Glasses_Emoji_2a8485bc-f136-4156-9af6-297d8522d8d1_large.png?v=1571606036"

    with open('out.bin', 'wb') as f:
        f.write(lcg_cipher(pt.encode(), 1550551))


def main_dec():
    with open('out.bin', 'rb') as f:
        ctext = f.read()
    
    pt = lcg_cipher(ctext, 1550551)
    
    print(pt.decode())

"""
def main():
    ax = plt.figure().add_subplot(projection='3d')
    prng = lcg(344, a=16598013, c=12820163, m=2**8)

    xs = []
    ys = []
    zs = []
    for i in range(0, 1000):
        x, y, z = prng.roll_norm(), prng.roll_norm(), prng.roll_norm()

        xs.append(x)
        ys.append(y)
        zs.append(z)
    
    ax.scatter(xs, ys, zs=zs)
    plt.show()
"""


if __name__ == '__main__':
    main_dec()
