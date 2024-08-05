from byte_buffer2 import *
from br import *
from fat_area import *
from dentry import *
from collections import namedtuple

class Stream:
    def __init__(self, file, extents, offset=0):
        self.file = file 
        self.extents = extents
        self.offs = offset
        
    def read(self, to_read): 
        out = b''
        remain = to_read
        so, eo = 0, 0   # start offset, end offset
        for e in self.extents:
            if self.offs > e.start:
                continue
            
            so = e.start if self.offs==0 else e.start + self.offs 
            self.offs = 0
            eo = e.size if remain > e.size else remain
            
            self.file.seek(so)
            chunk = self.file.read(eo)
            out += chunk
                    
            remain -= eo
            if remain <= 0: return out
        
    def seek(self, offs):
        self.offs = offs    
      
if __name__ == "__main__":
    
    Extent = namedtuple('Extent', ['start', 'size'])  
    
    path = '../fat/FAT32_simple.mdf'
    file = open(path, 'rb') 
    
    # bootRecord
    extents = [Extent(0x0, 0x100), Extent(0x100, 0x100)]  
    s = Stream(file, extents, 0)
    bf = s.read(0x200)
    br = BootRecord(bf)
    print(hex(br.to_physical_offset(0x102))) # 0x500000
    
    # # dentry
    # extents = [Extent(0x400000, 0xb0)]  
    # s = Stream(file, extents, 0x80)
    # bf = s.read(0x20)
    # den = Dentry(bf)
    # print(den.name)
    