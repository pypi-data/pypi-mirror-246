import random

import microbin


def test_float(i: float, size: int):
    # This is needed due to precision loss in float16/32
    b = microbin.dumps(i, float_size=size)
    i2 = microbin.loads(b)

    b = microbin.dumps(i2, float_size=size)
    i3 = microbin.loads(b)
    if i2 != i3:
        print("Test failed!")
        print(f"{i2} != {i3}")
        print(b.hex(' '))
        print()
        exit(1)
    else:
        print(i, '->', b[8:].hex(' '))


def main():
    for size in (16, 32, 64):
        for _ in range(10):
            i = random.random()
            test_float(i, size)


if __name__ == '__main__':
    main()
