from byte_buffer2 import *
from br import *
from fat_area import *
from dentry import *
from filesystem import *
from node import *
from lfn import *
from stream import *
from collections import namedtuple
Extent = namedtuple('Extent', ['start', 'size'])

class FAT32:
    def __init__(self, path): 
        self.file = open(path, 'rb')
        
        # bootrecord
        b0 = self.file.read(0x200) 
        self.br = BootRecord(b0) 
         
        # fat#1
        self.file.seek(self.br.fat_area_addr) 
        b1 = self.file.read(self.br.fat_area_size)
        self.fat = FatArea(b1)

        # root
        root = Dentry()
        root.is_dir = True
        root.name = '/'
        root.start_cl_no = self.br.root_cluster_no
        root.size = 0
        root.is_empty = False
        self.r_node = self.make_node(root)
        self.search(root, self.r_node)
        
    def __del__(self):
        self.file.close()
        
    def build_file_system(self):
        fs = FileSystem(self.r_node)
        return fs
        
    def search(self, den, node):
        if not den.is_dir: return
        p_den, p_node = den, node
        offs = self.br.to_physical_offset(p_den.start_cl_no)
        while True: # 자식 탐색
            self.file.seek(offs)
            bf = self.file.read(0x20)
            offs += 0x20
            den = Dentry(bf) 
            if den.is_empty: break
            if den.is_lfn:
                self.file.seek(offs)
                bf = bf + self.file.read(0x20 * den.lfncnt)
                offs += 0x20 * den.lfncnt
                lfn = LFN(bf)
                den = lfn.get_dentry()
            elif not den.is_valid: continue
            if den.is_valid:
                c_node = self.make_node(den, p_node)
                p_node.children.append(c_node)
                self.search(den, c_node)
                    
    def make_node(self, den, p_node=None): 
        node = Node(den.name, den.is_dir)
     
        if p_node is None:
            node.full_path = node.name
            return node
        elif p_node.full_path=='/':
            node.full_path = p_node.full_path + node.name
        else:
            node.full_path = p_node.full_path +'/'+ node.name    
          
        node.creation_time = den.creation_time 
        node.lastwritten_time = den.lastwritten_time
        node.size = den.size 
        if den.is_dir:
            node.size = self.block_size(self.br.to_physical_offset(den.start_cl_no)) 
        
        cls = self.fat.get_clusters(den.start_cl_no)
        extents = self.make_extents(cls, node.size)
        node.stream = Stream(self.file, extents)
            
        return node

    def make_extents(self, cls, f_size):
        extents = []
        for c in cls:
            addr = self.br.to_physical_offset(c)
            size = 0x1000 if not c == cls[len(cls)-1] else f_size - (len(cls)-1)*0x1000
            extent = Extent(addr, size)
            extents.append(extent)
        return extents
    
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
    fs = FAT32('../fat/FAT32_simple.mdf')