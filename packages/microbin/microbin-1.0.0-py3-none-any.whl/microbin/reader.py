import struct
import typing
import io

from microbin.type import Type, Flags, DEFAULT_MAGIC


__all__ = ['DecodeError', 'Reader', 'load', 'load_iter', 'load_first', 'load_all', 'loads', 'loads_iter', 'loads_first', 'loads_all']


class DecodeError(Exception):
    pass


class Reader:
    def __init__(self, fp: typing.BinaryIO, allowed_magic: typing.Union[int, typing.Iterable[int]] = DEFAULT_MAGIC):
        """
        Initialize Reader to deserialize MicroBIN from ``fp``
        (a ``.read()``-supporting file-like object, opened in binary mode).

        ``allowed_magic`` is an application magic number or sequence of
        magic numbers, which are allowed to load.
        """
        self._fp = fp

        if isinstance(allowed_magic, int):
            allowed_magic = (allowed_magic, )

        mb_magic, magic, version, flags, count = struct.unpack('>2sHBBH', self._read(8))
        if mb_magic != b'mb':
            raise DecodeError('Invalid magic bytes')

        if version != 0:
            raise DecodeError('Unsupported version')

        if magic not in allowed_magic:
            raise DecodeError('Invalid application magic bytes: ' + hex(magic))

        self._flags = Flags(flags)
        self._count = count

    @property
    def count(self) -> int:
        """
        Remaining count of global objects in file.
        """
        return self._count

    @property
    def flags(self) -> Flags:
        """
        File flags.
        """
        return self._flags

    def _read(self, n):
        data = self._fp.read(n)
        if len(data) != n:
            raise EOFError()
        return data

    def _read_object_header(self, globl):
        if globl:
            if not self._count:
                raise EOFError()
            self._count -= 1

        t = int.from_bytes(self._read(1), 'big')
        tag = Type(t >> 5)
        t &= 0b11111

        i = 0
        while i != 5 and t & (1 << (4 - i)):
            i += 1
        
        t &= (1 << (5 - i)) - 1
        if i == 5:
            i = 8
        t <<= i * 8
        t |= int.from_bytes(self._read(i), 'big')

        if tag == Type.SPECIAL:
            return Type((1 << 4) | t), None
        return tag, t
    
    def read(self, *, _globl=True):
        """
        Read next global object from file and deserialize
        it to a Python object.
        """
        tag, var = self._read_object_header(globl=_globl)
        if tag == Type.NONE:
            return None
        if tag == Type.TRUE:
            return True
        if tag == Type.FALSE:
            return False

        if tag == Type.FLOAT16:
            return struct.unpack('>e', self._read(2))
        if tag == Type.FLOAT32:
            return struct.unpack('>f', self._read(4))
        if tag == Type.FLOAT64:
            return struct.unpack('>d', self._read(8))
        
        if tag == Type.RATIONAL:
            raise NotImplementedError()  # TODO
        
        if tag == Type.INT:
            return var
        if tag == Type.NINT:
            return -var
        
        if tag == Type.STRING:
            return self._read(var).decode('utf-8')
        if tag == Type.BYTES:
            return self._read(var)
        
        if tag == Type.LIST:
            return list(self._read_list_iter(var))
        if tag == Type.MAP:
            return dict(self._read_map_iter(var))
        
    def _read_list_iter(self, count):
        for _ in range(count):
            yield self.read(_globl=False)
        
    def _read_map_iter(self, count):
        for _ in range(count):
            k = self.read(_globl=False)
            v = self.read(_globl=False)
            yield k, v


def load_iter(fp: typing.BinaryIO,
              allowed_magic: typing.Union[int, typing.Iterable[int]] = DEFAULT_MAGIC,
              *, cls: typing.Type[Reader] = None):
    """
    Iterate over Python objects deserialized from global objects of ``fp``
    (a ``.read()``-supporting file-like object, opened in binary mode).

    ``allowed_magic`` is an application magic number or sequence of magic numbers,
    which are allowed to load.

    To use a custom ``Reader`` subclass, specify it with the ``cls`` kwarg;
    otherwise ``Reader`` is used.
    """

    if cls is None:
        cls = Reader
    
    r = cls(fp, allowed_magic=allowed_magic)
    for _ in range(r.count):
        yield r.read()


def load(fp: typing.BinaryIO,
         allowed_magic: typing.Union[int, typing.Iterable[int]] = DEFAULT_MAGIC,
         *, cls: typing.Type[Reader] = None):
    """
    Deserialize ``fp`` (a ``.read()``-supporting file-like object, opened in
    binary mode) to a Python object.

    ``allowed_magic`` is an application magic number or sequence of magic numbers,
    which are allowed to load.

    To use a custom ``Reader`` subclass, specify it with the ``cls`` kwarg;
    otherwise ``Reader`` is used.

    File must contain only one global object.
    """
    
    if cls is None:
        cls = Reader
    
    r = cls(fp, allowed_magic=allowed_magic)
    if r.count != 1:
        raise ValueError("MicroBIN file has more than one global objects. Use load_first() or load_all()")
    return r.read()


def load_first(fp: typing.BinaryIO,
               allowed_magic: typing.Union[int, typing.Iterable[int]] = DEFAULT_MAGIC,
               *, cls: typing.Type[Reader] = None):
    """
    Deserialize first global object of ``fp`` (a ``.read()``-supporting
    file-like object, opened in binary mode) to a Python object.

    ``allowed_magic`` is an application magic number or sequence of magic numbers,
    which are allowed to load.

    To use a custom ``Reader`` subclass, specify it with the ``cls`` kwarg;
    otherwise ``Reader`` is used.
    """
    
    if cls is None:
        cls = Reader
    
    r = cls(fp, allowed_magic=allowed_magic)
    return r.read()


def load_all(fp: typing.BinaryIO,
             allowed_magic: typing.Union[int, typing.Iterable[int]] = DEFAULT_MAGIC,
             *, cls: typing.Type[Reader] = None):
    
    """
    Deserialize all global objects from ``fp`` (a ``.read()``-supporting
    file-like object, opened in binary mode) to a list of Python objects.

    ``allowed_magic`` is an application magic number or sequence of magic numbers,
    which are allowed to load.

    To use a custom ``Reader`` subclass, specify it with the ``cls`` kwarg;
    otherwise ``Reader`` is used.
    """

    return list(load_iter(fp, allowed_magic, cls=cls))


def loads_iter(data: bytes,
               allowed_magic: typing.Union[int, typing.Iterable[int]] = DEFAULT_MAGIC,
               *, cls: typing.Type[Reader] = None):
    """
    Iterate over Python objects deserialized from global objects of ``s``
    (a ``bytes`` or ``bytearray`` instance).

    ``allowed_magic`` is an application magic number or sequence of magic numbers,
    which are allowed to load.

    To use a custom ``Reader`` subclass, specify it with the ``cls`` kwarg;
    otherwise ``Reader`` is used.
    """

    with io.BytesIO(data) as fp:
        yield from load_iter(fp, allowed_magic, cls=cls)


def loads(data: bytes,
          allowed_magic: typing.Union[int, typing.Iterable[int]] = DEFAULT_MAGIC,
          *, cls: typing.Type[Reader] = None):
    """
    Deserialize ``s`` (a ``bytes`` or ``bytearray`` instance) to a Python object.

    ``allowed_magic`` is an application magic number or sequence of magic numbers,
    which are allowed to load.

    To use a custom ``Reader`` subclass, specify it with the ``cls`` kwarg;
    otherwise ``Reader`` is used.

    File must contain only one global object.
    """

    with io.BytesIO(data) as fp:
        return load(fp, allowed_magic, cls=cls)


def loads_first(data: bytes,
                allowed_magic: typing.Union[int, typing.Iterable[int]] = DEFAULT_MAGIC,
                *, cls: typing.Type[Reader] = None):
    """
    Deserialize first global object of  ``s`` (a ``bytes`` or ``bytearray``
    instance) to a Python object.

    ``allowed_magic`` is an application magic number or sequence of magic numbers,
    which are allowed to load.

    To use a custom ``Reader`` subclass, specify it with the ``cls`` kwarg;
    otherwise ``Reader`` is used.
    """

    with io.BytesIO(data) as fp:
        return load_first(fp, allowed_magic, cls=cls)


def loads_all(data: bytes,
              allowed_magic: typing.Union[int, typing.Iterable[int]] = DEFAULT_MAGIC,
              *, cls: typing.Type[Reader] = None):
    """
    Deserialize all global objects from  ``s`` (a ``bytes`` or ``bytearray``
    instance) to a Python object.

    ``allowed_magic`` is an application magic number or sequence of magic numbers,
    which are allowed to load.

    To use a custom ``Reader`` subclass, specify it with the ``cls`` kwarg;
    otherwise ``Reader`` is used.
    """

    with io.BytesIO(data) as fp:
        return load_all(fp, allowed_magic, cls=cls)
