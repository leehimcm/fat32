from byte_buffer2 import *
from br import *
from dentry import *
from fat_area import *

class FAT32:
    def __init__(self): 
        path = '../fat/FAT32_simple.mdf'
        self.file = open(path, 'rb')
        
        # bootrecord
        b0 = self.file.read(0x200) 
        self.br = BootRecord(b0) 
         
        # fat#1
        self.file.seek(self.br.fat_area_addr) 
        b1 = self.file.read(self.br.fat_area_size)
        self.fat = FatArea(b1)

        # dentry
        self.search(self.br.root_cluster_no)
        
    def search(self, cl_no, den=0): 
        
        if den==0 or den.is_dir:
            scn = 0
            if cl_no == self.br.root_cluster_no:
                print('\nthis is root directory')
                clusters = [self.br.root_cluster_no]
            else: 
                print('\nthis is directory')
                clusters = self.fat.get_clusters(den.start_cl_no)
                scn = den.start_cl_no
            
            for c in clusters[:5]:
                print(f"cluster_no:{hex(c)}")  
            
            dentries = self.gather(clusters)
            dentry_cnt = len(dentries) // 0x20
            print(f"dentry_cnt: {dentry_cnt}")
            
            
            for i in range(dentry_cnt):
                print(f"i:{i}")
                bf = dentries[0x20*i : 0x20*(i+1)] 
                den = Dentry(bf)
                if den.is_valid and scn != den.start_cl_no and den.start_cl_no !=0:
                    self.search(den.start_cl_no, den)
                     
        elif den.is_file:
            print('\nthis is file')
            clusters = self.fat.get_clusters(den.start_cl_no) # 일부가 index out of range
            fcontent = self.gather(clusters)
            self.write_file(den.name, fcontent) 
            return
        else:
            return
            
    def gather(self, clusters): # 실제 데이터에 접근하고 합친다
        out = b''
        for cls in clusters:
            offs = self.br.to_physical_offset(cls)
            size = self.block_size(offs)
            self.file.seek(offs)
            block = self.file.read(size)
            out += block
        return out    
    
    def block_size(self, offs):
        pattern = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'        
        
        i = offs
        while True:
            self.file.seek(i)
            line = self.file.read(len(pattern))
            if pattern == line: 
                return i-offs
            i += len(pattern)

    def write_file(self, fname, bf):
        f = open(fname, "wb")
        f.write(bf)
        f.close()
           
if __name__ == "__main__":
    FAT32()