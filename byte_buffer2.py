# #!/usr/bin/env python3

from struct import *

class ByteBuffer2:
    def __init__(self, bs):
        self.m_data = bs
        self.m_offset = 0
        self.m_limit = len(bs)

    def has_remaining(self):
        return self.m_offset < self.m_limit

    def remained_size(self):
        return self.m_limit - self.m_offset

    def size(self):
        return len(self.m_data)

    def limit(self): 
        return len(self.m_data)

    @property
    def offset(self):
        return self.m_offset

    @offset.setter
    def offset(self, pos):
        self.m_offset = pos
        return self

    def unget(self, pos):
        self.m_offset -= pos
        return self

    def skip(self, count):
        self.m_offset += count
        return self

    def get_uint2_be(self):
        s = self.m_offset
        r = self.m_data[s:s+2]
        self.m_offset += 2
        return unpack('>H', r)[0]

    def get_uint1(self):
        r = self.m_data[self.m_offset]
        self.m_offset += 1
        return r

    def get_uint2_le(self):
        s = self.m_offset
        r = self.m_data[s:s+2]
        self.m_offset += 2
        return unpack('<H', r)[0] # <:le, H:2byte u_int, [0]:0번 튜플 반환

    def get_uint4_le(self):
        s = self.m_offset
        r = self.m_data[s:s+4]
        self.m_offset += 4
        return unpack('<I', r)[0] # I:4byte u_int

    def get_uint4_be(self):
        s = self.m_offset
        r = self.m_data[s:s+4]
        self.m_offset += 4
        return unpack('>I', r)[0]

    def get_ascii(self, *args):
        if len (args) == 0: return self.__get_ascii0()
        if len (args) == 1: return self.__get_ascii1(int(args[0]))
        return None

    def __get_ascii1(self, size):
        try:
            s = self.m_offset
            e = self.m_offset + size
            res = self.m_data[s:e].decode('utf-8')
        except Exception as e:
            res = "?"
        finally:
            self.m_offset += size

        return res

    def __get_ascii0(self):
        index = self.m_data.find(b'\x00', self.m_offset) # x00이 처음 나타나는 위치 찾기
        if index == -1:
            self.m_offset = self.m_limit
            try:
                return self.m_data[self.m_offset:].decode('utf-8')
            except Exception as e:
                return ""

        try:
            res = self.m_data[self.m_offset:index].decode('utf-8')
        except Exception as e:
            res = ""
        finally:
            self.m_offset = index + 1

        return res

    def get_utf16_le(self, size):
        o = self.m_offset
        res = self.m_data[o:o+size*2].decode('utf-16le')
        self.m_offset += size*2
        return res

    def compare_range(self, offset, count, val):
        if offset + count > self.m_limit:
            return False

        for i in range(offset, offset+count):
            if self.m_data[i] != val:
                return False

        return True

    def change_cur_to(self, ch): # m_data 값 변경
        b = bytearray(self.m_data) # mutable byte seq
        b[self.m_offset] = ord(ch) # ord():ascii 또는 유니코드 값 반환
        self.m_data = bytes(b) # immutable byte seq
        return self

