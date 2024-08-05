from fat32 import *

fat32 = FAT32('fat/FAT32_simple.mdf')
fs = fat32.build_file_system()

node = fs["/DIR1/LEAF.JPG"] # dictionary, __getitem__() 사용
node.export_to("C:\\Users\\leehi\\Desktop\\LEAF.JPG")

node = fs["/DIR1/PORT.JPG"] 
node.export_to("c:\\Users\\leehi\\Desktop\\PORT.JPG")

node = fs["/DIR1/thumb_nail.py"] 
node.export_to("c:\\Users\\leehi\\Desktop\\thumb_nail.py")

node = fs["/?IGER.JPG"] 
node.export_to("c:\\Users\\leehi\\Desktop\\TIGER.JPG")

