# Created by https://github.com/fourminute
# It may look sloppy, but it gets the job done

from shutil import copyfile
import hashlib
import os
sources = []
mirrors = []
hashtype = "MD5"
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
try: #Python2
    result = tkMessageBox.askyesno("Confirm","Proceed with copy operation?")
except:#Python3
    result = messagebox.askyesno("Confirm","Proceed with copy operation?")


print(result)
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
                copyfile(st, newfilepath)
                print("Copied file " + "'" +file + "'" + " > \\" + os.path.basename(newdirectory) + "\\" + file)
                
        else:
            srchash = md5sum(st)
            mirrorhash = md5sum(newfilepath)
            if srchash == mirrorhash:
                print("File " + "'" + file + "'" + " exists. Matching " + hashtype + "SUM!")
            else:
                print("File " + "'" + file + "'" + " exists, hash didn't match. Overwriting file > " + os.path.dirname(newfilepath))
                copyfile(st, newfilepath)
                    


index = 0
size = len(sources) 
while index < size :
    sourcefiles = [os.path.join(r,file) for r,d,f in os.walk(sources[index]) for file in f]
    mirrorfiles = [os.path.join(r,file) for r,d,f in os.walk(mirrors[index]) for file in f]
    mirror(sourcefiles, mirrorfiles, index)
    index += 1


