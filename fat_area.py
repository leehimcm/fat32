from byte_buffer2 import *
from br import *

class FatArea:
    def __init__(self, buffer):
        self.bb = ByteBuffer2(buffer)
        
        self.entries = []
        self.entries_len = len(buffer) // 4
        for _ in range(self.entries_len):
            self.entries.append(self.bb.get_uint4_le())
    
    def get_clusters(self, cl_no): 
        clusters = []
        while cl_no > 1 and cl_no != 0xfffffff: # 0번, 1번 클러스터는 데이터가 아님.
            clusters.append(cl_no)
            cl_no = self.entries[cl_no]
        return clusters
    
    def __str__():
        pass
        

if __name__ == "__main__":
    path = '../fat/FAT32_simple.mdf'
    file = open(path, 'rb')
    file.seek(0x215c00) 
    b0 = file.read(0x07a9 * 0x200)
    fat = FatArea(b0)
    
    cls = fat.get_clusters(0x07)
    for c in cls[:5]:
        print(hex(c))
    