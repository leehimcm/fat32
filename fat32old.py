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
        bf = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        root = Dentry(bf)
        root.start_cl_no = self.br.root_cluster_no
        c = self.save_child(root)
        self.search(c)  # 루트 디렉토리 처리를 좀 더 깔끔하게 하고싶음.. 저렇게 조작해도 되나..
    
    def save_child(self, den):
        print(f"start cluster num : {hex(den.start_cl_no)}")
        dentries = self.gather([den.start_cl_no])
        dentry_cnt = len(dentries) // 0x20
        c = []
        for i in range(dentry_cnt):
            bf = dentries[0x20*i : 0x20*(i+1)] 
            child = Dentry(bf)
            c.append(child)
        return c
        
    def search(self, children):
        for den in children:
            if not den.is_valid or den.is_empty: 
                continue
            elif den.is_dir:
                print('\nthis is directory')
                print(den.name)
                den.children = self.save_child(den)
                self.search(den.children)
                
            elif den.is_file:
                print('\nthis is file')
                self.make_file(den)
            else:
                print('\ninvalid')

    def make_file(self, den):
        clusters = self.fat.get_clusters(den.start_cl_no) 
        fcontent = self.gather(clusters)     
        f = open(den.name, "wb")
        f.write(fcontent)
        f.close()
        print(den.name)
            
    def gather(self, clusters): # 실제 데이터에 접근하고 합친다.
        out = b''   
        for i in range(len(clusters)):
            offs = self.br.to_physical_offset(clusters[i])
            size = 0x1000
            if i == len(clusters) - 1: # 마지막 클러스터일 때는 0x1000보다 덜 읽어온다.
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
            line = self.file.read(16)
            if pattern == line:
                return i-offs
            i += 16     
    
if __name__ == "__main__":
    FAT32()