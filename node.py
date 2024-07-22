from byte_buffer2 import *
from br import *
import datetime

class Node:
    def __init__(self, *buffer):
        if len(buffer) == 0:
            return
        
        bb = ByteBuffer2(buffer[0])
        self.children = []
        
        # attr 0xb
        bb.offset = 0x0b
        self.attr = bb.get_uint1()     
        
         # fname 0x0~7 (8)
        bb.offset = 0x00
        self.fname = bb.get_ascii(8).rstrip()
        
        self.set_type()
        if not self.is_valid:
            return
        
        # exten 0x8~a (3)
        self.exten = bb.get_ascii(3) .rstrip()
        
        self.name = self.fname
        if len(self.exten) > 0:
            self.name += '.' + self.exten
        
        # start_cl_no 0x14~15 + 1a~1b
        bb.offset = 0x14
        n1 = bb.get_uint2_le()
        n1 = n1 << 16
        bb.offset = 0x1a
        self.start_cl_no = n1 + bb.get_uint2_le()
         
        # date_time 0x0e~12      
        bb.offset = 0x0e
        dt = bb.get_uint4_le()
        self.date_time = datetime.datetime.fromtimestamp(dt)
        
        # size 0x0c~f
        bb.offset = 0x1c
        self.size = bb.get_uint4_le()
    
    
    def set_type(self):
        self.is_empty = (self.attr == 0x00)  
        self.is_dir = (self.attr == 0x10)
        self.is_file = (self.attr == 0x20)
        self.is_lfn = (self.attr == 0x0f)
        self.is_volumelabel = (self.attr == 0x08)
        self.is_hidden = (self.attr == 0x02)
        self.is_valid = not self.fname in ['.', '..'] and not self.attr in [0x0f, 0x08]
     
     
     
     
def print_node(file, addr):
    file.seek(addr)
    buffer = file.read(0x20) 
    n = Node(buffer)
    if n.is_valid:
        print(n.name)
        print(n.start_cl_no)
        print(n.date_time)

if __name__ == "__main__":
    path = '../fat/FAT32_simple.mdf' 
    file = open(path, 'rb')
    print_node(file, 0x404040)
    print_node(file, 0x400080)
    