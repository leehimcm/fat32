#!/usr/bin/env python

import unittest
import io
from stream import *
from byte_buffer2 import *
from collections import namedtuple
Extent = namedtuple('Extent', ['start', 'size'])  

class TestStream(unittest.TestCase):
    def setUp(self):
        self.data = (b'\xebX\x90MSDOS5.0\x00\x02\x08\xae\x10\x02\x00\x00\x00\x00\xf8\x00\x00'
                     b'?\x00\xff\x00\x00\x00\x00\x00\x00\xc0\x1e\x00\xa9\x07\x00\x00'
                     b'\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x06\x00\x00\x00\x00\x00'
                     b'\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00)\x9c\xb9}\xb4NO NAME    FAT32 '
                     b'  3\xc9\x8e\xd1\xbc\xf4{\x8e\xc1\x8e\xd9\xbd\x00|\x88V@\x88N\x02\x8aV'
                     b'@\xb4A\xbb\xaaU\xcd\x13r\x10\x81\xfbU\xaau\n\xf6\xc1\x01t\x05\xfeF\x02'
                     b'\xeb-\x8aV@\xb4\x08\xcd\x13s\x05\xb9\xff\xff\x8a\xf1f\x0f\xb6\xc6@f\x0f\xb6'
                     b'\xd1\x80\xe2?\xf7\xe2\x86\xcd\xc0\xed\x06Af\x0f\xb7\xc9f\xf7\xe1f'
                     b'\x89F\xf8\x83~\x16\x00u9\x83~*\x00w3f\x8bF\x1cf\x83\xc0\x0c\xbb'
                     b'\x00\x80\xb9\x01\x00\xe8,\x00\xe9\xa8\x03\xa1\xf8}\x80\xc4|\x8b\xf0\xac'
                     b'\x84\xc0t\x17<\xfft\t\xb4\x0e\xbb\x07\x00\xcd\x10\xeb\xee\xa1\xfa}'
                     b'\xeb\xe4\xa1}\x80\xeb\xdf\x98\xcd\x16\xcd\x19f`\x80~\x02\x00\x0f\x84 \x00fj'
                     b'\x00fP\x06Sfh\x10\x00\x01\x00\xb4B\x8aV@\x8b\xf4\xcd\x13fXfXfXfX\xeb3f;'
                     b'F\xf8r\x03\xf9\xeb*f3\xd2f\x0f\xb7N\x18f\xf7\xf1\xfe\xc2\x8a\xcaf\x8b'
                     b'\xd0f\xc1\xea\x10\xf7v\x1a\x86\xd6\x8aV@\x8a\xe8\xc0\xe4\x06\n\xcc'
                     b'\xb8\x01\x02\xcd\x13fa\x0f\x82t\xff\x81\xc3\x00\x02f@Iu\x94\xc3BOOTMGR    '
                     b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                     b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                     b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                     b'\x00\x00\x00\x00\r\nDisk error\xff\r\nPress any key to restart\r'
                     b'\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                     b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                     b'\x00\x00\x00\x00\xac\x01\xb9\x01\x00\x00U\xaa')

        # io.BytesIO shared same interface of raw file i/o
        # https://docs.python.org/3/library/io.html#io.BufferedIOBase
        self.file = io.BytesIO(self.data)

    def test_br(self):
        bb = ByteBuffer2(self.data)
        bb.offset = 0x200 - 2
        self.assertEqual(bb.get_uint2_be(), 0x55aa)

    def test_extent1(self):
        extents = [Extent(0, 0x200)]
        s  = Stream(self.file, extents, 0)
        bb = ByteBuffer2(s.read(0x200))

        bb.offset = 0x0b
        self.assertEqual(bb.get_uint2_le(), 0x200)
        self.assertEqual(bb.get_uint1(), 8)

        bb.offset = 0x30 - 4
        self.assertEqual(bb.get_uint4_le(), 2)

    def test_extent2(self):
        extents = [Extent(0, 0x100), Extent(0x100, 0x100)]
        s  = Stream(self.file, extents, 0)
        bb = ByteBuffer2(s.read(0x200))

        bb.offset = 0x0b
        self.assertEqual(bb.get_uint2_le(), 0x200)
        self.assertEqual(bb.get_uint1(), 8)

        bb.offset = 0x30 - 4
        self.assertEqual(bb.get_uint4_le(), 2)

if __name__ == "__main__":
    unittest.main()