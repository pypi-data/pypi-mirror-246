import microbin


def main():
    # Serialize int, float, bool, None, str, bytes, list, dict
    b = microbin.dumps({
        'key': 'value'
    })

    print(b)
    data = microbin.loads(b)
    print(data)
    # microbin.dumps / microbin.loads works with bytes object

    with open('file.bin', 'rb') as f:
        print(microbin.load(f))
    # microbin.dump / microbin.load works with file object (from open())

    print(microbin.dumps([1, 2, 3]))
    print(microbin.dumps_all([1, 2, 3]))
    # dump(s)_all serializes items of collection (list or tuple)
    # to multiple global objects while dump(s) with list
    # serializes to one list global object.
    print(microbin.dumps(1) == microbin.dumps_all([1]))  # True
    # Result of dumps_all() with collection of length > 1 cannot
    # be deserialized with loads().

    b = microbin.dumps_all([1, 2, 3])
    for i in microbin.loads_iter(b):
        print(i)
    # load(s)_iter is like load(s)_all, but returns iterable object
    # for lazy loading (it really works for load_iter, not for loads_iter).

    # Count of global objects is limited by 65535 (0xFFFF), so if you have
    # MicroBIN file with many global object you can use something like
    # this to save some memory:
    with open('file.bin', 'rb') as f:
        for obj in microbin.load_iter(f):
            # Do something with obj
            print(obj)
    # With this code only one global object will be in memory in one time


if __name__ == '__main__':
    main()
