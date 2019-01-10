# Created by https://github.com/fourminute
# It may look sloppy, but it gets the job done

from shutil import copyfile
import hashlib
import os

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
source = ""
mirror = ""
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
def changelabel(text):
    labeltxt.set(text)

root = Tk()
root.resizable(0,0)
labeltxt = tk.StringVar()
winlabel = Label(root, textvariable=labeltxt)
winlabel.pack(padx=20,pady=10)
def quit():
    try:#Python2
        result = tkMessageBox.askyesno("Are you sure?","Cancel operation and exit?")
    except:#Python3
        result = messagebox.askyesno("Are you sure?","Cancel operation and exit?")
    if result == True:
        exit()
root.protocol("WM_DELETE_WINDOW",quit)
changelabel("Awaiting File Selection.")
source = filedialog.askdirectory(title='Please select a source directory.')
mirror = filedialog.askdirectory(title='Please select a mirror directory.')
sourcefiles = [os.path.join(r,file) for r,d,f in os.walk(source) for file in f]
mirrorfiles = [os.path.join(r,file) for r,d,f in os.walk(mirror) for file in f]
result = ""
changelabel("Files Selected.")
try:#Python2
    result = tkMessageBox.askyesno("Confirm","Proceed with copy operation?")
except:#Python3
    result = messagebox.askyesno("Confirm","Proceed with copy operation?")


if not result == True:
    exit()


#Simple MD5SUM
def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()


# Mirror files operation
def start():
    for st in sourcefiles:
        file = os.path.basename(st)
        directory = os.path.split(st)[0]
        newfilepath = st.replace(source, mirror)
        newdirectory = os.path.split(newfilepath)[0]
        fncount = sum([len(files) for r, d, files in os.walk(source)])
        #Checking if directory exists
        if not os.path.exists(newdirectory):
            print("Directory " + "'" + os.path.basename(newdirectory) + "'" + " doesn't exist, creating.")
            os.makedirs(newdirectory)
            print("Created directory " + "'" + os.path.dirname(newfilepath) + "'")
                
        #Copy operation
        if not os.path.exists(newfilepath):
            try:
                copyfile(st, newfilepath)
                inccopied()
                print("Copied " + "'" +file + "'" + " to " + "'" + ".../" + os.path.basename(newdirectory) + "/" + file + "'"+ ".")
                changelabel("Copying Files\nProgress: " + str(filescopied + fileshashed) + " of " + str(fncount) + ".")
                root.update()
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
                print("File " + "'" + file + "'" + " exists, hash didn't match. Overwriting to " + "'" + os.path.dirname(newfilepath) + "'"+ ".")
                try:
                    copyfile(st, newfilepath)
                    inccopied()
                    print("Copied " + "'" +file + "'" + " to " + "'" + ".../" + os.path.basename(newdirectory) + "/" + file + "'" + ".")
                    changelabel("Copying Files\nProgress: " + str(filescopied + fileshashed) + " of " + str(fncount) + ".")
                except:
                    print("Failed to copy " + "'" + file + "'" + ".")
                    incfailed()
                    



start()

try:#Python3
    messagebox.showinfo("Operation Completed","Total Files Copied: " + str(filescopied) + ". \nTotal Files Hashed: " + str(fileshashed) + ".\nFailed To Copy: " + str(filesfailed) + ".")
except:
    tkMessageBox.showinfo("Operation Completed","Total Files Copied: " + str(filescopied) + ". \nTotal Files Hashed: " + str(fileshashed) + ".\nFailed To Copy: " + str(filesfailed) + ".")
