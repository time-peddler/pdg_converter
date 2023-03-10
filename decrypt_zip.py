import sys
import zipfile
import rarfile
import threading
import datetime
import os
import subprocess
i = 0

class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
        self.result = self.func(*self.args)
    def get_result(self):
        try:
            return self.result
        except Exception:
            return None
            
def extractFile(fileExtr, password, fileType, unzip2path):
    try:
        if (fileType == "zip"):
            fileExtr.extractall(path=unzip2path,pwd=password.encode('utf-8'))
        else:
            fileExtr.extractall(path=unzip2path,pwd=password.encode('utf-8'))
        if password:
            global i
            i = i + 1
            print("search count : %d,real password is : %s" % (i, password))
        return password
    except:
        i = i + 1
        print("search count : %d,test password : %s, failed!" % (i, password))
        pass
        
def extract(file_path,password_file="passwords.txt"):
    try:
        if os.path.exists(file_path) == False:
            print("%s : path error!"%(file_path))
            return
        file_type = os.path.splitext(file_path)[-1][1:].lower()
        # 验证安装包是否有密码
        if file_type == ("zip" or "uvz"):
            zp = zipfile.ZipFile(file_path)
            for l in zp.infolist():
                is_encrypted = l.flag_bits & 0x1
                if is_encrypted:
                    break
        elif file_type == "rar":
            print(file_path)
            zp = rarfile.RarFile(file_path, mode='r')
            is_encrypted = zp.needs_password()
        else:
            print("file not right")
            return
                      
        # 读取 读秀密码本
        with open(password_file,encoding='utf-8') as f:
            pwdLists = f.readlines()
        startTime = datetime.datetime.now()
        
        unzip2path = os.path.splitext(file_path)[0]
        print(unzip2path)
        if is_encrypted:
            print('encrpted!trying to decrypt it with Passbook.')
            for line in pwdLists:
                Pwd = line.strip('\n')
                t = MyThread(extractFile, (zp, Pwd, file_type, unzip2path))
                t.start()
                if (t.get_result() is Pwd):
                    break
            endTime = datetime.datetime.now()
            timeSpan = endTime - startTime
            print("search time:%ss" % (timeSpan.total_seconds()))
        else:
            extractFile(zp,'',file_type,unzip2path)
    except:
       print("err:%s" % sys.exc_info()[0])
           
if __name__ == '__main__':
    
    import tkinter as tk
    from tkinter import filedialog
    file_path = filedialog.askopenfilename()
    extract(file_path)