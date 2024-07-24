from byte_buffer2 import *
from br import *
from fat_area import *
from dentry import *
from node import *

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

        # root
        root = Node()
        root.is_dir = True
        root.name = '/'
        root.start_cl_no = self.br.root_cluster_no
        root.size = 0
        self.save_child(root)
        self.search(root)  
    
    def save_child(self, node):
        blocks = self.gather([node.start_cl_no])
        cnt = len(blocks) // 0x20
        c = []
        for i in range(cnt):
            bf = blocks[0x20*i : 0x20*(i+1)] 
            den = Dentry(bf)
            if den.is_valid:
                c_node = Node(den)
                c.append(c_node)
        node.node_list = c
               
    def search(self, node):
        for node in node.node_list:
            if not node.is_valid or node.is_empty:
                continue
            elif node.is_dir:
                print('\nthis is directory')
                print(node.name)
                self.save_child(node)
                self.search(node)
            elif node.is_file:
                print('\nthis is file')
                self.make_file(node)
            else:
                print('\ninvalid')

    def make_file(self, den):
        clusters = self.fat.get_clusters(den.start_cl_no) 
        fcontent = self.gather(clusters)
        fcontent = fcontent[:den.size]
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