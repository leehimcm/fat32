from byte_buffer2 import *
from br import *

class Node:
    def __init__(self, metadata=None):
        if metadata is None:
            return
        
        self.node_list = []
        self.name = metadata.name 
        self.start_cl_no = metadata.start_cl_no
        self.creation_time = metadata.creation_time
        self.lastwritten_time = metadata.lastwritten_time
        self.size = metadata.size
        
        self.is_empty = metadata.is_empty
        self.is_dir = metadata.is_dir
        self.is_file = metadata.is_file
        self.is_lfn = metadata.is_lfn
        self.is_volumelabel = metadata.is_volumelabel
        self.is_hidden = metadata.is_hidden
        self.is_valid = metadata.is_valid
        
        
        
        
        
        