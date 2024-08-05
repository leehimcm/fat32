from byte_buffer2 import *
from br import *

class Node:
    def __init__(self, name, isdir):
        self.children = []
        self.name = name
        self.creation_time = None
        self.lastwritten_time = None
        self.size = 0
        self.is_dir = isdir # 파일, 디렉토리 구분
        self.is_hidden = False
        self.full_path = ''
        self.stream = None
        
    def export_to(self, path):
        self.stream.seek(0) 
        content = self.stream.read(self.size)
        f = open(path, "wb")
        f.write(content)
    