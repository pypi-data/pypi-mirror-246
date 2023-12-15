import struct
import typing
import io

from microbin.type import Type, Flags, DEFAULT_MAGIC


__all__ = ['Writer', 'dump', 'dump_all', 'dumps', 'dumps_all']


class Writer:
    def __init__(self, fp: typing.BinaryIO, count: int = 1, magic: int = DEFAULT_MAGIC, flags: Flags = 0):
        self._fp = fp
        self._magic = magic
        self._flags = flags
        self._count = count
        self._write_header()

    @property
    def count(self):
        """
        Remaining count of global objects in file.
        """
        return self._count

    @property
    def flags(self):
        """
        File flags.
        """
        return self._flags

    def _write_header(self):
        self._fp.write(struct.pack('>2sHBBH', b'mb', self._magic, 0, self._flags, self._count))
    
    def _write_object_header(self, typ: Type, value: int, globl: bool):
        if globl:
            if not self._count:
                raise ValueError("")

            self._count -= 1

        if typ > 7:
            value = typ & 0b1111
            typ = Type.SPECIAL
        
        t = int(typ) << 5

        bits = value.bit_length()
        i = 0
        while bits > 4 and i < 5:
            bits -= 8
            i += 1
        
        t |= (0xFF << (5 - i)) & 0b11111
        if i == 5:
            i = 8
        t |= value >> (8 * i)
        t = t.to_bytes()

        value &= (1 << (8 * i)) - 1

        t += value.to_bytes(i)

        self._fp.write(t)

    def write_rational(self, value, _globl=True):
        raise NotImplementedError()  # TODO
        self._write_object_header(Type.RATIONAL, value, _globl)

    def write_int(self, value: int, *, _globl=True):
        if value >= 0:
            self._write_object_header(Type.INT, value, _globl)
        else:
            self._write_object_header(Type.NINT, -value, _globl)

    def write_string(self, value: str,*,  _globl=True):
        value = value.encode('utf-8')
        self._write_object_header(Type.STRING, len(value), _globl)
        self._fp.write(value)

    def write_bytes(self, value: bytes, *, _globl=True):
        self._write_object_header(Type.BYTES, len(value), _globl)
        self._fp.write(value)
    
    def write_none(self, *, _globl=True):
        self._write_object_header(Type.NONE, None, _globl)

    def write_bool(self, value: bool, *, _globl=True):
        self._write_object_header(Type.TRUE if value else Type.FALSE, None, _globl)
    
    def write_float(self, value: float, *, size: int = 64, _globl=True):
        if size == 16:
            self._write_object_header(Type.FLOAT16, None, _globl)
            self._fp.write(struct.pack('>e', value))
        elif size == 32:
            self._write_object_header(Type.FLOAT32, None, _globl)
            self._fp.write(struct.pack('>f', value))
        elif size == 64:
            self._write_object_header(Type.FLOAT64, None, _globl)
            self._fp.write(struct.pack('>d', value))
        else:
            raise ValueError(f"Float size must be 16, 32 or 64, not {size}")

    def write_list_header(self, count: int, *, _globl=True):
        self._write_object_header(Type.LIST, count, _globl)

    def write_map_header(self, count: int, *, _globl=True):
        self._write_object_header(Type.MAP, count, _globl)

    def write_default(self, value, *, _globl=True):
        raise TypeError(f"Cannot encode object of type {type(value).__name__} to MicroBIN")

    def write(self, obj, *, float_size: int = 64, _globl=True):
        """
        Serialize ``obj`` to MicroBIN format and write to file.

        ``float_size`` is a size of float numbers in bits. Can be 16, 32 or 64.
        """
        if obj is None:
            self.write_none(_globl=_globl)

        elif isinstance(obj, bool):
            self.write_bool(obj, _globl=_globl)

        elif isinstance(obj, int):
            self.write_int(obj, _globl=_globl)

        elif isinstance(obj, str):
            self.write_string(obj, _globl=_globl)

        elif isinstance(obj, bytes):
            self.write_bytes(obj, _globl=_globl)

        elif isinstance(obj, float):
            self.write_float(obj, size=float_size, _globl=_globl)

        elif hasattr(obj, '__len__') and hasattr(obj, 'items'):
            self.write_map_header(len(obj), _globl=_globl)
            for k, v in obj.items():
                self.write(k, float_size=float_size, _globl=False)
                self.write(v, float_size=float_size, _globl=False)

        elif hasattr(obj, '__len__') and hasattr(obj, '__iter__'):
            self.write_list_header(len(obj), _globl=_globl)
            for i in obj:
                self.write(i, float_size=float_size, _globl=False)

        else:
            self.write_default(obj)


def dump(obj, fp: typing.BinaryIO, *, magic: int = DEFAULT_MAGIC, flags: Flags = 0,
         float_size: int = 64, cls: typing.Type[Writer] = None):
    """
    Serialize ``obj`` as a single global object in MicroBIN format to ``fp``
    (a ``.write()``-supporting file-like object).
    
    ``magic`` is an application magic number used in MicroBIN file.

    ``flags`` is a MicroBIN flags.

    ``float_size`` is a size of float numbers in bits. Can be 16, 32 or 64.
    
    To use a custom ``Writer`` subclass (e.g. one that overrides the
    ``.write_default()`` method to serialize additional types), specify it with
    the ``cls`` kwarg; otherwise ``Writer`` is used.
    """

    if cls is None:
        cls = Writer

    w = cls(fp, count=1, magic=magic, flags=flags)
    w.write(obj, float_size=float_size)


def dump_all(objs: typing.Collection, fp: typing.BinaryIO, *, magic: int = DEFAULT_MAGIC,
             flags: Flags = 0, float_size: int = 64, cls: typing.Type[Writer] = None):
    """
    Serialize all items of ``objs`` as global objects in MicroBIN format
    to ``fp`` (a ``.write()``-supporting file-like object).
    
    ``magic`` is an application magic number used in MicroBIN file.

    ``flags`` is a MicroBIN flags.

    ``float_size`` is a size of float numbers in bits. Can be 16, 32 or 64.
    
    To use a custom ``Writer`` subclass (e.g. one that overrides the
    ``.write_default()`` method to serialize additional types), specify it with
    the ``cls`` kwarg; otherwise ``Writer`` is used.
    """

    if cls is None:
        cls = Writer
    
    w = cls(fp, count=len(objs), magic=magic, flags=flags)
    for obj in objs:
        w.write(obj, float_size=float_size)


def dumps(obj, *, magic: int = DEFAULT_MAGIC, flags: Flags = 0,
          float_size: int = 64, cls: typing.Type[Writer] = None) -> bytes:
    """
    Serialize ``obj`` as a single global object in MicroBIN format to ``bytes``.
    
    ``magic`` is an application magic number used in MicroBIN file.

    ``flags`` is a MicroBIN flags.

    ``float_size`` is a size of float numbers in bits. Can be 16, 32 or 64.
    
    To use a custom ``Writer`` subclass (e.g. one that overrides the
    ``.write_default()`` method to serialize additional types), specify it with
    the ``cls`` kwarg; otherwise ``Writer`` is used.
    """

    with io.BytesIO() as fp:
        dump(obj, fp, magic=magic, flags=flags, float_size=float_size, cls=cls)
        return fp.getvalue()


def dumps_all(objs: typing.Collection, *, magic: int = DEFAULT_MAGIC, flags: Flags = 0,
              float_size: int = 64, cls: typing.Type[Writer] = None) -> bytes:
    """
    Serialize all items of ``objs`` as global objects in MicroBIN format
    to ``bytes``.
    
    ``magic`` is an application magic number used in MicroBIN file.

    ``flags`` is a MicroBIN flags.

    ``float_size`` is a size of float numbers in bits. Can be 16, 32 or 64.
    
    To use a custom ``Writer`` subclass (e.g. one that overrides the
    ``.write_default()`` method to serialize additional types), specify it with
    the ``cls`` kwarg; otherwise ``Writer`` is used.
    """

    with io.BytesIO() as fp:
        dump_all(objs, fp, magic=magic, flags=flags, float_size=float_size, cls=cls)
        return fp.getvalue()
