# -*- coding: utf-8 -*- 
import os
import sys
import hashlib
from datetime import datetime

start_time = datetime.now()
filetree = {}
temptree = {}
dubles = {}
nullfiles = []
exceptions = []
file_count = 0
nest_count = 0
pair_nest_count = 0
mayby_dubles = 0


#@profile #use decorator with "python -m memory_profiler compare.py"
def listfolder(current_directory):
    global file_count
    files = os.listdir(current_directory) 
    for current_filename in files:
        current_full_filename = current_directory + current_filename
        if os.access(current_full_filename, os.R_OK) == True: #access check 
            if os.path.isdir(current_full_filename):
                try:
                    listfolder(current_full_filename + "/")
                except IOError as e:
                    print("Error: '" + e + "', Args: " + e.errno)
                    exceptions.append("Error: '" + e + "', Args: " + e.errno)
            else:
                file_count += 1
                try:
                    fsize = os.path.getsize(current_full_filename)
                    if fsize == 0:
                        nullfiles.append(current_full_filename)
                    else:
                        """
                        # group files with first byte. more precisely groups, but longer 
                        f = open(current_full_filename, 'rb', 0)
                        byte = int.from_bytes(f.read(1), byteorder='big')
                        f.close()
                        filetree.setdefault(byte + fsize, [])
                        filetree[byte + fsize].append(current_full_filename)
                        """
                        # group files w/o first byte. groups faster, hash longer
                        filetree.setdefault(fsize,[])
                        filetree[fsize].append(current_full_filename)
                                                
                except IOError as e:
                    print("Error: '" + e + "', Args: " + e.errno)
                    exceptions.append("Error: '" + e + "', Args: " + e.errno)
        else:
            exceptions.append("Access denied: " + current_full_filename)


#@profile
def md5(fname): # this function is taken from the internet
    hash_md5 = hashlib.md5()
    try:
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except IOError as e: 
        print("Error: '" + e + "', Args: " + e.errno)
        exceptions.append("Error: '" + e + "', Args: " + e.errno)


if sys.argv[1]:
    start_directory = sys.argv[1]
else:
    start_directory = input("Input path like 'c:/program files/' or /home/user/:")

if os.path.isdir(start_directory):
    print ("I work, I eat memory\n")
    listfolder(start_directory)
else:
    print("Not a directory")
    exit()


nest_count = len(filetree)
print ("File nesting complete.")
print ("Nesting time: " + datetime.now() - start_time + " \nNest count: " + nest_count)


for key,val in filetree.items():
    if len(val)>1:
        mayby_dubles += len(val)
        pair_nest_count += 1
        for md5file in val:
            # nest files into a temporary dictionary by md5.
            temptree.setdefault(md5(md5file),[])
            temptree[md5(md5file)].append(md5file)
        # go through the dictionary and transfer lists where there is more than one element 
        for kmd5,vmd5 in temptree.items(): 
            if len(vmd5)>1:
                dubles.update({ kmd5 : vmd5})
        temptree.clear()
filetree.clear()
# remove temporary dictionary, remove nest from filetree
print ("search complete, saving\n")


with open('dubles.txt', 'w', encoding='utf8') as i:
    i.write("[" + start_directory + "]\n")
    for hashmd5, file_list in dubles.items():
        i.write("[" + hashmd5 + "]\n")
        for filename in file_list:
            i.write(filename + "\n")
        i.write("\n")
    i.write("\n[Stat]\nFile count: " + file_count + ", ")
    i.write("Nest_count: " + nest_count + ", ")
    i.write("Nest count w pair: " + pair_nest_count + "\n")
    i.write("Total time: " + (datetime.now() - start_time) + "\n")
 
print("[Stat]\nFile count: " + file_count + ", Nest_count: " + nest_count)
print("Nest count w pair: " + pair_nest_count + "\nTotal time: " + datetime.now() - start_time)
print("Mayby dubles: " + mayby_dubles + "\nDubles: " + len(dubles))


with open('exceptions.txt', 'w', encoding='utf8') as i:
    # Save collected exceptions 
    for exception in exceptions:
        i.write(exception + "\n")

with open('nulfiles.txt', 'w', encoding='utf8') as i:
    # Save list with empty files 
    for file in nullfiles:
        i.write(file + "\n")

