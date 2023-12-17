import microbin


def test_other(i):
    b = microbin.dumps(i)
    i2 = microbin.loads(b)
    if i != i2:
        print("Test failed!")
        print(f"{i!r} != {i2!r}")
        print(b.hex(' '))
        print()
        exit(1)
    else:
        print(repr(i), '->', b[8:].hex(' '))


def main():
    for i in (True, False, None):
        test_other(i)

    for i in range(5):
        i = '#' * i
        test_other(i)
        test_other(i.encode('utf-8'))


if __name__ == '__main__':
    main()
