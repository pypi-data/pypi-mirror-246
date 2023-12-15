import microbin
import collections
import argparse


def print_stats(types, objects_size, objects_count, total_size, total_count):
    print("Type          Count   Total     BpO")
    for typ in types:
        count = objects_count[typ]
        size = objects_size[typ]

        print(f"{typ.name: <11} {count: >7} {size:>7} {size / count: >7.3f}")
    
    print(f"-- Total -- {total_count: >7} {total_size: >7} {total_size / total_count: >7.3f}")


def get_stats(file):
    objects_size = collections.defaultdict(int)
    objects_count = collections.defaultdict(int)
    total_count = 0

    with file as f:
        d = microbin.Reader(f)
        old_pos = f.tell()  # not zero, skip header
        
        while True:
            try:
                typ, value = d._read_object_header(globl=False)
            except EOFError:
                break

            if typ in {microbin.Type.STRING, microbin.Type.BYTES}:
                f.read(value)

            elif typ == microbin.Type.FLOAT16:
                f.read(2)
            elif typ == microbin.Type.FLOAT32:
                f.read(4)
            elif typ == microbin.Type.FLOAT64:
                f.read(8)
            
            pos = f.tell()
            objects_size[typ] += pos - old_pos
            old_pos = pos

            objects_count[typ] += 1
            total_count += 1
            
        total_size = pos

    return objects_size, objects_count, total_size, total_count



def main():
    parser = argparse.ArgumentParser('microbin.mbstart', description='Analyze MicroBIN file', epilog='(c) NekoNekoNyan <me@neko-dev.ru>, 2023')
    parser.add_argument('-V', '--version', action='version', version=microbin.__version__)
    parser.add_argument('-s', '--sort', action='store', choices=('count', 'size', 'bpo'), default='size', help='set field to sort (default: size)')
    parser.add_argument('file', type=argparse.FileType('rb'), help='MicroBIN file to analyze')
    
    args = parser.parse_args()

    objects_size, objects_count, total_size, total_count = get_stats(args.file)

    if args.sort == 'count':
        types = sorted(objects_size, key=lambda x: objects_count[x], reverse=True)
    elif args.sort == 'bpo':
        types = sorted(objects_size, key=lambda x: objects_size[x] / objects_count[x], reverse=True)
    else:
        types = sorted(objects_size, key=lambda x: objects_size[x], reverse=True)
    
    print_stats(types, objects_size, objects_count, total_size, total_count)


if __name__ == '__main__':
    main()
