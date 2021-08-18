# -*- coding: utf-8 -*- 

# поиск дубликатов файлов. примерное количество файлов 13,3млн в 2млн папок. 24,7Тб, необходимый объём памяти 6,4Гб
# ключевые параметры для сравнения - имя файла, размер, первый байт, контрольная сумма(может даже md5sum)
# определить параметр для группировки, искать повторы в группах. 


import copy
import os
import hashlib

from datetime import datetime
start_time = datetime.now()

start_directory = input("Input path like 'c:/program files/' or /home/user/:")
print ("I work, I eat memory\n")
filetree={}
temptree={}
dubles={}
nullfiles=[]
exceptions=[]

def listfolder(current_directory):
        files = os.listdir(current_directory) 
        #print (type(files))
        for current_filename in files:
            if os.access(current_directory + current_filename, os.R_OK) == True: #access check 
                if os.path.isdir(current_directory + current_filename):
                    try:
                        listfolder(current_directory + current_filename + "/")
                    except IOError as e:
                        print("Error: '{}', Args: {} ".format(e, e.errno))
                        exceptions.append("Error: '{}', Args: {} ".format(e, e.errno))
                else:
                    try:
                        fsize = os.path.getsize(current_directory + current_filename)
                        if fsize == 0:
                            nullfiles.append(current_directory + current_filename)
                        else:
                            f = open(current_directory + current_filename, 'rb', 0)
                            byte = int.from_bytes(f.read(1), byteorder='big')
                            f.close()
                            filetree.setdefault(str(byte)+ "." + str(fsize),[])
                            filetree[str(byte)+ "." + str(fsize)].append(current_directory + current_filename)
                            #print ("{} - {} - {}\n".format(current_filename, byte, fsize))
                    except IOError as e:
                        print("Error: '{}', Args: {} ".format(e, e.errno))
                        exceptions.append("Error: '{}', Args: {} ".format(e, e.errno))
            else:
                pass

def md5(fname): # эта функция взята целиком с интернета
    hash_md5 = hashlib.md5()
    try:
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except IOError as e: 
        print("Error: '{}', Args: {} ".format(e, e.errno))
        exceptions.append("Error: '{}', Args: {} ".format(e, e.errno))



listfolder(start_directory)
print ("file nesting complete\n")

for key,val in filetree.items():
    if len(val)>1:
        for md5file in val:
            # nest files into a temporary dictionary by md5.
            temptree.setdefault(md5(md5file),[])
            temptree[md5(md5file)].append(md5file)
        for kmd5,vmd5 in temptree.items(): # пробегаем по словарю, и переносим списки где больше одного элемента
            if len(vmd5)>1:
                dubles.update({ kmd5 : vmd5})
        temptree.clear()
filetree.clear()
# удаляем временный словарь, удалеям гнездо из filetree
print ("search complete, saving\n")


with open('dubles.txt', 'w', encoding='utf8') as i:
    i.write('[{}]\n'.format(start_directory))
    for hashmd5,file_list in dubles.items():
        i.write('[{}]\n'.format(hashmd5))
        for filename in file_list:
            i.write('{}\n'.format(filename))
        i.write('\n')
    i.write('Total time: {}\n'.format(datetime.now() - start_time)) # script execution time


with open('exceptions.txt', 'w', encoding='utf8') as i:
    # Save collected exceptions 
    for ex in exceptions:
        i.write('{}\n'.format(ex))

with open('nulfiles.txt', 'w', encoding='utf8') as i:
    # Save list with empty files 
    for file in nullfiles:
        i.write('{}\n'.format(file))

