import sys
import argparse
import microbin
import json

def main():
    parser = argparse.ArgumentParser('microbin.json2mb', description='Convert json to MicroBIN file',
                                     epilog='(c) NekoNekoNyan <me@neko-dev.ru>, 2023')
    parser.add_argument('-V', '--version', action='version', version=microbin.__version__)
    parser.add_argument('-i', '--input', type=argparse.FileType("rt", encoding='utf-8'), default=sys.stdin,
                        help='set input json file (default: standart input)')
    parser.add_argument('-m', '--magic', type=int, default=microbin.DEFAULT_MAGIC,
                        help=f'set application magic (default: {microbin.DEFAULT_MAGIC:04x})')
    parser.add_argument('-f', '--float-size', type=int, choices=(16, 32, 64), default=64,
                        help=f'set size of float numbers (in bits; default: 64)')
    parser.add_argument('file', type=argparse.FileType('wb'), help='output MicroBIN file')
    
    args = parser.parse_args()

    data = json.load(args.input)
    microbin.dump(data, args.file, magic=args.magic, float_size=args.float_size)


if __name__ == '__main__':
    main()
