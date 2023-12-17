import microbin


def test_int(i: int):
    b = microbin.dumps(i)
    i2 = microbin.loads(b)
    if i != i2:
        print("Test failed!")
        print(f"{i} != {i2}")
        print(b.hex(' '))
        print()
        exit(1)
    else:
        print(i, '->', b[8:].hex(' '))


def main():
    for i in (1, 4, 11, 18, 25, 32, 64):
        n = 1 << i
        test_int(n - 2)
        test_int(n - 1)
        if i < 64:
            test_int(n)

    for i in (1, 4, 11, 18, 25, 32, 64):
        n = -(1 << i)
        test_int(n + 2)
        test_int(n + 1)
        if i < 64:
            test_int(n)


if __name__ == '__main__':
    main()
