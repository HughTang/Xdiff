# coding=utf-8
from subprocess import Popen, PIPE
import re,os,sys

# regular expression
function_return_type = r'''
            (\s*)
            (\s*(static)?\s*)
            (\s*(const)?\s*)
            (\s*(volatile)?\s*)
            (\s*(inline)?\s*)
            (\s*(extern)?\s*)
            ((VOID)|(void)|(char)|(short)|(int)|(float)|(long)|(double)|(bool)|(enum)|(wait_queue_t)|(wait_queue_head_t)) # 识别函数返回值类型
            (\s*(\*)?\s*)                                                       # 识别返回值是否为指针类型以及中间是否包含空格
            (\w+)                                                               # 识别函数名
            ((\s*)(\()(\n)?)                                                    # 函数开始小括号
            (((\s*)?(const)?(unsigned)?(signed)?(\s*)?                                   # 参数前是否有const、unsigned
            ((void)|(char)|(short)|(int)|(float)|(long)|(double)|(bool)|(enum)|(wait_queue_t)|(wait_queue_head_t)))?
            ((\s*)(const)?(\s*)(struct)(\s*))?(union\s*\w+)?
            (\s*)(\*)?(\s*)?(restrict)?(\s*)?(\w+)(\s*)?(\,)?(\n)?(.*)?)*       # 最后的*表示有多个参数
            ((\s*)(\))(\n)?)                                                    # 函数结束小括号
            '''

#Use the shell
def run_cmd(cmd):
	# Popen call wrapper.return (code, stdout, stderr)
	child = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
	out, err = child.communicate()
	ret = child.wait()
	return (ret, out, err)

def condition(result):
	global func
	f = open('condition_exp','r')
	content = f.read()
	condition_words = content.split('\n')
	num = 0
	if result.find("****\n- ") != -1:
		for x in condition_words:
			s = x.strip()
			index = result.find(s)
			if index != -1:
				num = num + 1
		if num != 0:
			print("\tType: Delete Condition")
			func = 0
	elif result.find("----\n+ ") != -1:
		# print("\tOnly added parts in this block!")
		for x in condition_words:
			s = x.strip()
			index = result.find(s)
			if index != -1:
				num = num + 1
		if num != 0:
			print("\tType: Add Condition")
			func = 0
	else:
		part = result.split("\n--- ")
		num1 = 0
		num2 = 0
		for x in condition_words:
			s = x.strip()
			index = part[0].find(s)
			if index != -1:
				num1 = num1 + 1

		for x in condition_words:
			s = x.strip()
			index = part[1].find(s)
			if index != -1:
				num2 = num2 + 1
		if num1 != 0 and num2 != 0:
			print("\tType: Update Condition")
			func = 0
		elif num1 == 0 and num2 != 0:
			print("\tType: Add Condition")
			func = 0
		elif num1 != 0 and num2 == 0:
			print("\tType: Delete Condition")
			func = 0

def throw_exception(result):
	global func
	f = open('error_exp','r')
	content = f.read()
	error_words = content.split('\n')
	num = 0
	for x in error_words:
		s = x.strip()
		index = result.find(s)
		if index != -1:
			num = num + 1
	if num != 0:
		print("\tType: Throw Exception")
		func = 0

def function(result):
	global func
	pat = re.compile(function_return_type, re.X)
	if result.find("****\n- ") != -1:
		result = re.sub("\-", '', result) #replace -
		ret = pat.search(result)
		if ret != None:
			print("\tType: Delete Function")
			func = 0
	elif result.find("----\n+ ") != -1:
		result = re.sub("\+", '', result) #replace +
		ret = pat.search(result)
		if ret != None:
			print("\tType: Add Function")
			func = 0
	else:
		part = result.split("\n--- ")
		part[0] = re.sub('!', '', part[0])  #replace！
		part[1] = re.sub('!', '', part[1])
		ret_0 = pat.search(part[0])
		ret_1 = pat.search(part[1])
		if ret_0 != None and ret_1 != None:
			print("\tType: Update Function Parameter")
			func = 0
		elif ret_0 == None and ret_1 != None:
			print("\tType: Add Function")
			func = 0
		elif ret_0 != None and ret_1 == None:
			print("\tType: Delete Function")
			func = 0

def function_internal_crud(result):
	global func
	if func == 1:
		print("\tType: Function Internal CRUD")


if __name__ == '__main__':
	try:
		global func
		func = 1
		#Show help
		if sys.argv[1] == "-h":
			print("Usage:")
			print("    python Xdiff.py file1 file2   #Show the diff type between file1 and file2")
			print("    python Xdiff.py dir1 dir2     #Show the diff type between dir1 and dir2")
			print("General Options:")
			print("    python Xdiff.py -h                             #Show help")
			print("    python Xdiff.py [file1/dir1] [file2/dir2] -s   #Show the diff code")
			os._exit(0)
		elif not os.path.exists(sys.argv[1]) or not os.path.exists(sys.argv[2]):
			print("No such file or directory!")
			os._exit(0)
		elif os.path.isdir(sys.argv[1]) and os.path.isdir(sys.argv[2]):
			_,r,_ = run_cmd("diff -c -0 "+sys.argv[1]+" "+sys.argv[2])
			if r[:4] == "Only":
				print(r)
			else:
				file_block = r.split("diff -c -0 ")
				file_block.pop(0)
				for s in file_block:
					print("******************Diff Type**********************")
					file_name = s.split("\n")
					print("Analyze the file: "+file_name[0])
					code_block = s.split("***************")
					code_block.pop(0)
					n = 1
					for x in code_block:
						print("    Analyze the "+str(n)+" code block:")
						# print(s)
						condition(x)
						throw_exception(x)
						function(x)
						function_internal_crud(s)
						n = n + 1
						func = 1
					index = s.find("Only in ")
					if index != -1:
						print("******************File Diff**********************")
						print(s[index:])
					if "-s" in sys.argv:
						print("------------------Diff Code----------------------")
						print(s)

		elif os.path.isfile(sys.argv[1]) and os.path.isfile(sys.argv[2]):
			_,r,_ = run_cmd("diff -c -0 "+sys.argv[1]+" "+sys.argv[2])
			code_block = r.split("***************")
			code_block.pop(0)
			print("******************Diff Type**********************")
			print("Analyze the "+sys.argv[1]+" and "+sys.argv[2]+":")
			n = 1
			for s in code_block:
				print("    Analyze the "+str(n)+" code block:")
				condition(s)
				throw_exception(s)
				function(s)
				function_internal_crud(s)
				n = n + 1
				func = 1
			if "-s" in sys.argv:
					print("------------------Diff Code----------------------")
					print(r)
		else:
			print("ImportError：incorrect input parameter！ Use -h to show help.")
	except:
		print("ImportError：incorrect input parameter！ Use -h to show help.")
