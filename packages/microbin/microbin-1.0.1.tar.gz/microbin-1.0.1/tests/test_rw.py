import io

import microbin


def test_count(count: int):
    with io.BytesIO() as fp:
        w = microbin.Writer(fp, count)
        for i in range(count):
            w.write(i)

        fp.seek(0)

        r = microbin.Reader(fp)
        if r.count != count:
            print("Count mismatch!")
            print(f"{r.count} != {count}")
            exit(1)

        print(f"Reading {count} objects...")
        for _ in range(r.count):
            print(repr(r.read()))


def main():
    for i in range(1, 5):
        test_count(i)
    test_count(0xFFFF)


if __name__ == '__main__':
    main()
