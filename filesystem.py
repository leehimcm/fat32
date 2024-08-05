class FileSystem:
    def __init__(self, root):
        
        self.nodes = {} # K:노드이름, V:노드
        self.search_node(root)
        
    def search_node(self, node): 
        for n in node.children:
            self.nodes[n.full_path] = n
            if n.is_dir:
                self.search_node(n)
                
    def __getitem__(self, key):
        return self.nodes.get(key, 'path not found')