from byte_buffer2 import *

class Dentry:
    def __init__(self, *buffer):
        if len(buffer) == 0: 
            return
        
        self.bb = ByteBuffer2(buffer[0])
        self.lfncnt = 0
        
        # attr 0xb
        self.bb.offset = 0x0b
        self.attr = self.bb.get_uint1()     
        
        # fname 0x0~7 (8)
        self.bb.offset = 0x00
        self.fname = self.bb.get_ascii(8).rstrip()
        
        self.set_type()
        if not self.is_valid or self.is_empty:
            return
        if self.is_lfn:
            self.bb.offset = 0x00
            cnt = self.bb.get_uint1()
            self.lfncnt = cnt ^ 0x40 # lfn 개수 
            return
        
        # exten 0x8~a (3)
        self.bb.offset = 0x08
        self.exten = self.bb.get_ascii(3) .rstrip()
        
        self.name = self.fname
        if len(self.exten) > 0:
            self.name += '.' + self.exten
        
        # start_cl_no 0x14~15 + 1a~1b
        self.bb.offset = 0x14
        n1 = self.bb.get_uint2_le()
        n1 = n1 << 16
        self.bb.offset = 0x1a
        self.start_cl_no = n1 + self.bb.get_uint2_le()

        # creation_time 0x0e~12      
        self.bb.offset = 0x0e
        time = self.bb.get_uint2_le()
        date = self.bb.get_uint2_le()
        self.creation_time = self.hex2datetime(date, time)
        
        # lastwritten_time 0x16~19    
        self.bb.offset = 0x16
        time = self.bb.get_uint2_le()
        date = self.bb.get_uint2_le()
        self.lastwritten_time = self.hex2datetime(date, time)
        
        # size 0x0c~f
        self.bb.offset = 0x1c
        self.size = self.bb.get_uint4_le()
        
    def hex2datetime(self, d, t):
        date = bin(d)[2:] # 0000 000/0 000/0 0000 
        time = bin(t)[2:] # 0000 0/000 000/0 0000
       
        year = 1980 + int(date[:-9], 2)
        month = int(date[-9:-5], 2)
        day = int(date[-5:], 2)
        
        hour = int(time[:-11], 2)
        minute = int(time[-11:-5], 2)
        sec = int(time[-5:], 2) * 2
        
        return f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{sec:02d}"
        
    def set_type(self):
        self.is_empty = (self.attr == 0x00)  
        self.is_dir = (self.attr & 0x10 == 0x10)
        self.is_file = (self.attr & 0x20 == 0x20)
        self.is_lfn = (self.attr == 0x0f)
        self.is_system_file = (self.attr & 0x04 == 0x04)
        self.is_volumelabel = (self.attr & 0x08 == 0x08)
        self.is_hidden = (self.attr & 0x02 == 0x02)
        self.is_valid = not self.fname in ['.', '..'] and not self.attr in [0x08]
    
def print_dentry(file, addr):
    file.seek(addr) 
    buffer = file.read(0x20) 
    d1 = Dentry(buffer)
    if d1.is_lfn:
        print(d1.lfncnt)
    elif d1.is_valid:
        print(d1.name)
        print(d1.creation_time)
        print(d1.lastwritten_time)

if __name__ == "__main__":
    path = '../fat/FAT32_simple.mdf' 
    file = open(path, 'rb')
    print_dentry(file, 0x4010a0)
    