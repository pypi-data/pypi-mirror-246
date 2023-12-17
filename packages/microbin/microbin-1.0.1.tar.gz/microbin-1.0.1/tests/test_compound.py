import microbin


def test_compound(i):
    b = microbin.dumps(i)
    i2 = microbin.loads(b)
    if i != i2:
        print("Test failed!")
        print(f"{i!r} != {i2}")
        print(b.hex(' '))
        print()
        exit(1)
    else:
        print(repr(i), '->', b[8:].hex(' '))


def main():
    for i in range(5):
        r = []
        for _ in range(i):
            r.append(r.copy())

        test_compound(r)

    for i in range(5):
        r = {}
        for x in range(i):
            r[x] = r.copy()

        test_compound(r)

    test_compound({i: repr(i) for i in (1, -1, True, False, None, 's', b'b')})


if __name__ == '__main__':
    main()
