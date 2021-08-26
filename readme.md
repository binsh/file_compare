# Compare - File duplicate finder for big filestore

Problem:
All found programs for comparing files could not cope with the number of files.
Approximate number of files 13,3 millions in 2 millions folders approximate amount of disk space 24,7Tb.
The required amount of memory for operation 6,4Gb

Key parameters for comparison: filesize, first byte, check sum(md5sum)

### How to:
1. Group files by size and first byte 
2. Compare check sum in group

### Run:
python compare.py (or python3 compare.py)  

### Run with argument:
python compare.py d:/folder/

### Compile for Windows:
Install installer "pip install pyinstaller" if not installed :)  
... and compile "pyinstaller -F compare.py"


### Result example (dubles.txt):

[e44aed1ab245bfeb1054becc3520d0f1]  
d:/dev/WebServ/denwer/utils/run.ico  
d:/dev/webServ2/etc/utils/run.ico  

[a00d284782cce54f083c8bd628dcd978]  
d:/dev/WebServ/usr/local/apache/bin/Apache.ico  
d:/dev/webServ2/usr/local/apache/Apache.ico  
