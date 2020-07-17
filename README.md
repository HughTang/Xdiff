## Xdiff
##### Xdiff is a tool to identify diff modification types. The operating environment and usage are as follows.Please make sure that the two filenames that you compare are the same. And you should make sure the file names are the same in both folders.

#### Environment： 
	python-linux-2.7
#### Usage:
    python Xdiff.py file1 file2   #Show the diff type between file1 and file2
    python Xdiff.py dir1 dir2     #Show the diff type between dir1 and dir2
#### General Options:
    python Xdiff.py -h                             #Show help
    python Xdiff.py [file1/dir1] [file2/dir2] -s   #Show the diff code
#### diff modification types:
##### 1.Add Condition
##### 2.Delete Condition
##### 3.Update Condition
##### 4.Throw Exception
##### 5.Add Function
##### 6.Delete Function
##### 7.Update Function Parameter
##### 8.Function Internal CRUD
