# Compare - File duplicate finder for big filestore

Problem:
All found programs for comparing files could not cope with the number of files.
Approximate number of files 13,3 millions in 2 millions folders approximate amount of disk space 24,7Tb.
The required amount of memory for operation 6,4Gb

Key parameters for comparison: filesize, first byte, check sum(md5sum)

How to:
1. Group files by size and first byte 
2. Compare check sum in group

Run:
python compare.py (or python3 compare.py)

Compile for Windows:
Install installer "pip install pyinstaller" if not installed :)
... and compile "pyinstaller -F compare.py"
