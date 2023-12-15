import sys
import argparse
import microbin
import json

KWARGS_NORMAL = {
    'indent': 2
}
KWARGS_COMPACT = {
    'separators': (',', ':')
}

def main():
    parser = argparse.ArgumentParser('microbin.mb2json', description='Convert MicroBIN file to json', epilog='(c) NekoNekoNyan <me@neko-dev.ru>, 2023')
    parser.add_argument('-V', '--version', action='version', version=microbin.__version__)
    parser.add_argument('-o', '--output', type=argparse.FileType("wt", encoding='utf-8'), default=sys.stdout,
                        help='set output json file (default: standart output)')
    parser.add_argument('-m', '--magic', type=int, default=microbin.DEFAULT_MAGIC,
                        help=f'set application magic (default: {microbin.DEFAULT_MAGIC:04x})')
    parser.add_argument('-c', '--compact', action='store_true',
                        help=f'create compact json')
    parser.add_argument('-a', '--ascii', action='store_true',
                        help=f'create json without any non-ascii characters')
    parser.add_argument('file', type=argparse.FileType('rb'), help='MicroBIN file to convert')
    
    args = parser.parse_args()

    data = microbin.load(args.file, args.magic)
    kwargs = KWARGS_COMPACT if args.compact else KWARGS_NORMAL
    json.dump(data, args.output, ensure_ascii=args.ascii, **kwargs)


if __name__ == '__main__':
    main()
