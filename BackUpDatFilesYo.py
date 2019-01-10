# Created by https://github.com/fourminute
# It may look sloppy, but it gets the job done

from shutil import copyfile
import hashlib
import os
sources = []
mirrors = []
hashtype = "MD5"
fileshashed = 0
filescopied = 0
filesfailed = 0
def inchashed():
  global fileshashed
  fileshashed += 1
def inccopied():
  global filescopied
  filescopied += 1
def incfailed():
  global filesfailed
  filesfailed += 1
  
try:#Python2
    import Tkinter as tk 
    from Tkinter import filedialog
    import tkMessageBox
    from Tkinter import *
except:#Python3
    import tkinter as tk 
    from tkinter import filedialog
    from tkinter import messagebox
    from tkinter import *

#Ask for Directory
root = Tk()
root.withdraw()
srcdir = filedialog.askdirectory(title='Please select a source directory.')
mrrdir = filedialog.askdirectory(title='Please select a mirror directory.')
result = ""
try:#Python2
    result = tkMessageBox.askyesno("Confirm","Proceed with copy operation?")
except:#Python3
    result = messagebox.askyesno("Confirm","Proceed with copy operation?")


if result == True:
    sources.append(srcdir)
    mirrors.append(mrrdir)
else:
    exit()



#Simple MD5SUM
def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()


# Mirror files operation
def mirror(source, mirror, index):
    for st in source:
        file = os.path.basename(st)
        directory = os.path.split(st)[0]
        newfilepath = st.replace(sources[index], mirrors[index])
        newdirectory = os.path.split(newfilepath)[0]
        if not os.path.exists(newfilepath):
                if not os.path.exists(newdirectory):
                    print("Directory " + "'" + os.path.basename(newdirectory) + "'" + " doesn't exist, creating.")
                    os.makedirs(newdirectory)
                    print("Created directory " + os.path.dirname(newfilepath))    
                    try:
                        copyfile(st, newfilepath)
                        inccopied()
                        print("Copied file " + "'" +file + "'" + " > \\" + os.path.basename(newdirectory) + "\\" + file)
                    except:
                        print("Copy operation failed, unknown error.")
                        incfailed()
                
        else:
            srchash = md5sum(st)
            inchashed()
            mirrorhash = md5sum(newfilepath)
            if srchash == mirrorhash:
                print("File " + "'" + file + "'" + " exists. Matching " + hashtype + "SUM!")
            else:
                print("File " + "'" + file + "'" + " exists, hash didn't match. Overwriting file > " + os.path.dirname(newfilepath))
                try:
                    copyfile(st, newfilepath)
                    inccopied()
                    print("Copied file " + "'" +file + "'" + " > \\" + os.path.basename(newdirectory) + "\\" + file)
                except:
                    print("Copy operation failed, unknown error.")
                    incfailed()
                    


index = 0
size = len(sources) 
while index < size :
    sourcefiles = [os.path.join(r,file) for r,d,f in os.walk(sources[index]) for file in f]
    mirrorfiles = [os.path.join(r,file) for r,d,f in os.walk(mirrors[index]) for file in f]
    mirror(sourcefiles, mirrorfiles, index)
    index += 1


messagebox.showinfo("Operation Completed","Total Files Copied: " + str(filescopied) + ". \nTotal Files Hashed: " + str(fileshashed) + ".\nFailed To Copy: " + str(filesfailed) + ".")
