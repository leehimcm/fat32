##!/usr/bin/env python

import unittest
from byte_buffer2 import *

class TestByteBuffer2(unittest.TestCase):
    def setUp(self):
        self.t1 = b'\x11\x22\x33\x44'
        self.d0 = b'hello\x00world\x00'
        self.d1 = b'\x20\x00I\x00n\x00f\x00'
        self.bb = ByteBuffer2(self.t1)

    def test_ctor(self):
        self.assertTrue(self.bb is not None)
        self.assertEqual(self.bb.size(), 4)

    def test_uint2_be(self):
        self.assertEqual(self.bb.get_uint2_be(), 0x1122)
        self.assertEqual(self.bb.offset, 2)

    def test_uint2_le(self):
        self.assertEqual(self.bb.get_uint2_le(), 0x2211)
        self.assertEqual(self.bb.offset, 2)

    def test_ascii(self):
        bb = ByteBuffer2(self.d0)
        r0 = bb.get_ascii()
        self.assertEqual(r0, 'hello')
        self.assertEqual(bb.offset, 6)

        r1 = bb.get_ascii()
        self.assertEqual(r1, 'world')
        self.assertEqual(bb.offset, 12)

    def test_ascii2(self):
        bb = ByteBuffer2(self.d0)
        r0 = bb.get_ascii(3)
        self.assertEqual(r0, 'hel')
        self.assertEqual(bb.offset, 3)

    def test_utf16le(self):
        bb = ByteBuffer2(self.d1)
        r0 = bb.get_utf16_le(4)
        self.assertEqual(r0, ' Inf')

    def test_has_remaining(self):
        self.assertEqual(self.bb.get_uint2_be(), 0x1122)
        self.assertEqual(self.bb.offset, 2)
        self.assertEqual(self.bb.has_remaining(), True)
        self.assertEqual(self.bb.get_uint2_be(), 0x3344)
        self.assertEqual(self.bb.offset, 4)
        self.assertEqual(self.bb.has_remaining(), False)

    def test_compare_range(self):
        b = [0 for i in range(0, 0x20)]
        bb = ByteBuffer2(b)
        self.assertEqual(bb.size(), 0x20)
        self.assertEqual(bb.compare_range(0, 0x20, 0), True)

if __name__ == "__main__":
    unittest.main() # run the tests
