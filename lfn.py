from byte_buffer2 import *
from dentry import *

class LFN:
    def __init__(self, bf):
        self.bb = ByteBuffer2(bf)

        cnt = len(bf) // 0x20 
        name = ''
        for i in range(cnt-1):
            name = self.lfname(i) + name
        
        self.den = Dentry(bf[-0x20:])
        self.den.name = name
        
    def lfname(self, i):
        offs = i * 0x20
        n1, n2, n3, n4 = '','','',''
        
        self.bb.offset = 0x01 + offs
        for _ in range(5):
            n1 += self.bb.get_ascii()
          
        self.bb.offset = 0x0e + offs   
        for _ in range(1):
            n2 += self.bb.get_ascii()
            
        self.bb.offset = 0x10 + offs
        for _ in range(5):
            n3 += self.bb.get_ascii()
            
        self.bb.offset = 0x1c + offs
        for _ in range(2):
            n4 += self.bb.get_ascii()
        return n1+n2+n3+n4
    
    def get_dentry(self):
        return self.den