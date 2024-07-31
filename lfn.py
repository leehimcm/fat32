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
        
    def lfname(self, i): # 디코딩 에러 수정하기
        offs = i * 0x20
        
        self.bb.offset = 0x01 + offs
        n1 = self.bb.get_utf16_le(5).rstrip('\uffff')
          
        self.bb.offset = 0x0e + offs   
        n2 = self.bb.get_utf16_le(6).rstrip('\uffff')
            
        self.bb.offset = 0x1c + offs
        n3 = self.bb.get_utf16_le(2).rstrip('\uffff')
        
        return (n1+n2+n3).replace('\x00','')
    
    def get_dentry(self):
        return self.den