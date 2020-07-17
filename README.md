## Xdiff
Xdiff is a tool for identifying diff modification types. The operating environment and usage are as follows.Please make sure that the two filenames that you compare are the same. And make sure the file names are the same in both folders.

Environment： 
	python-linux-2.7
Usage:
    python Xdiff.py file1 file2   #Show the diff type between file1 and file2
    python Xdiff.py dir1 dir2     #Show the diff type between dir1 and dir2
General Options:
    python Xdiff.py -h                             #Show help
    python Xdiff.py [file1/dir1] [file2/dir2] -s   #Show the diff code
