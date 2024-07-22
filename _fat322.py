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
        self.search(c)
    
    def save_child(self, den):
        print(f"den.start_cl_no: {hex(den.start_cl_no)}")
        dentries = self.gather([den.start_cl_no])
        dentry_cnt = len(dentries) // 0x20
        print(f"dentry_cnt: {dentry_cnt}")
        c = []
        for i in range(dentry_cnt):
            bf = dentries[0x20*i : 0x20*(i+1)] 
            child = Dentry(bf)
            c.append(child)
        return c
        
    def search(self, children):
        i = 0
        for den in children:
            i += 1
            if (not den.is_valid) or den.is_empty: 
                continue
            elif den.is_dir:
                print('\nthis is directory')
                den.children = self.save_child(den)
                self.search(den.children)
            elif den.is_file:
                print('\nthis is file')
                self.make_file(den)

    def make_file(self, den):
        clusters = self.fat.get_clusters(den.start_cl_no) 
        fcontent = self.gather(clusters)     
        
        #leaf가 안 나오는 원인이 아님
        beg_pattern = b'\xFF\xD8\xFF'
        end_pattern = b'\xFF\xD9'  
        if fcontent[:3] == beg_pattern:
            end = len(fcontent) - 16
            for _ in range(15):
                if fcontent[end:end+2] == end_pattern:
                    fcontent = fcontent[:end+2]
                end += 1
        
        f = open(den.name, "wb")
        f.write(fcontent)
        f.close()
        print(den.name)
        print(fcontent[:3])
        print(hex(len(fcontent)))
    
            
    def gather(self, clusters): # 실제 데이터에 접근하고 합친다 # 얘 때매 느렸음, leaf 원인인데 정확한 이유는 모름
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
    
if __name__ == "__main__":
    FAT32()