from byte_buffer2 import *
from br import *
from fat_area import *
from dentry import *
from collections import namedtuple

class Stream:
    def __init__(self, file, extents, offset=0):
        self.file = file 
        self.extents = extents
        self.offset = offset
        
    def read(self, to_read): 
        out = b''
        remained = to_read
        cursor = 0   
        
        for ext in self.extents:
            
            cursor += ext.size
            if self.offset > cursor:
                continue
            
            so = ext.start + self.offset - (cursor - ext.size)
            chunk_size = min(remained, ext.size - (so - ext.start))
            
            self.file.seek(so)
            chunk = self.file.read(chunk_size)
            
            self.offset += chunk_size
            remained -= chunk_size
            out += chunk
                    
            if remained <= 0: return out
        
    def seek(self, offset): 
        self.offset = offset    
      
if __name__ == "__main__":
    
    Extent = namedtuple('Extent', ['start', 'size'])  
    
    path = 'fat/FAT32_simple.mdf'
    file = open(path, 'rb') 
    
    # bootRecord
    extents = [Extent(0x0, 0x100), Extent(0x100, 0x100)]  
    s = Stream(file, extents, 0)
    bf = s.read(0x200)
    br = BootRecord(bf)
    print(hex(br.to_physical_offset(0x102))) # 0x500000
    
    # # dentry
    # extents = [Extent(0x400000, 0xb0)]  
    # s = Stream(file, extents)
    # s.seek(0x80)
    # bf = s.read(0x20)
    # den = Dentry(bf)
    # print(den.name)
    