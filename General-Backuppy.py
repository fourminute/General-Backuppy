# Created by https://github.com/fourminute
# Hello There

from shutil import copyfile
import hashlib
import os

try:# Python2
    import Tkinter as tk 
    from Tkinter import filedialog
    import tkMessageBox
    from Tkinter import *
except:# Python3
    import tkinter as tk 
    from tkinter import filedialog
    from tkinter import messagebox
    from tkinter import *

# UI
root = Tk()
labeltxt = tk.StringVar()
root.resizable(0,0)
winlabel = Label(root, textvariable=labeltxt)
winlabel.pack(padx=25,pady=15)
root.protocol("WM_DELETE_WINDOW",quit)
    
# Variables
source_directory = ""
mirror_directory = ""
hashtype = "SHA512" # If you wish to use MD5(faster, but less secure) instead, set this to "MD5".
fileshashed = 0
filescopied = 0
filesfailed = 0
total_file_count = 0
finished = False

# Set file count
def update_file_count(number):
    global total_file_count
    total_file_count = number
    
# Increase file counter 0 = hashed, 1 = copy, 2 = failed.
def inc_file_counter(what):
  if what == 0:
    global fileshashed
    fileshashed += 1
  elif what == 1:
    global filescopied
    filescopied += 1
  elif what == 2:
    global filesfailed
    filesfailed += 1

# Change progress label
def changelabel(text):
    labeltxt.set(text)
    root.update()
    
# Safely exit
def quit():
    quit_result = False
    try:# Python2
        if not finished == True:
            quit_result = tkMessageBox.askyesno("Are you sure?","Cancel operation and exit?")
    except:# Python3
        if not finished == True:
            quit_result = messagebox.askyesno("Are you sure?","Cancel operation and exit?")
    if quit_result == True:
        exit()
    if finished == True:
        exit()



# MD5SUM
def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()

# SHA512SUM
def sha512sum(filename, blocksize=65536):
    hash = hashlib.sha512()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()

# Copy operation
def copy(source, destination):
    copyfile(source, destination)
    inc_file_counter(1)
    file_name = os.path.basename(source)
    print("Copied " + "'" + file_name + "'" + " to " + "'" + ".../" + os.path.basename(destination) + "/" + file_name + "'"+ ".")
    changelabel("Copying Files.\nProgress: " + str(filescopied + fileshashed + filesfailed) + " of " + str(total_file_count) + ".")
    
# Main
def start():
    changelabel("Awaiting File Selection.")
    source_directory = filedialog.askdirectory(title='Please select a source directory.')
    mirror_directory = filedialog.askdirectory(title='Please select a mirror directory.')
    source_files_array = [os.path.join(r,file) for r,d,f in os.walk(source_directory) for file in f]
    mirror_files_array = [os.path.join(r,file) for r,d,f in os.walk(mirror_directory) for file in f]
    update_file_count(sum([len(files) for r, d, files in os.walk(source_directory)]))
    changelabel(str(total_file_count) + " Total Files Selected. Proceed?")
    try:# Python2
        confirm_result = tkMessageBox.askyesno("Confirm","Proceed with copy operation?")
    except:# Python3
        confirm_result = messagebox.askyesno("Confirm","Proceed with copy operation?")
    if not confirm_result == True:
        exit()
        
    for source_file_path in source_files_array:
        file_name = os.path.basename(source_file_path)
        current_source_file_directory = os.path.split(source_file_path)[0]
        mirror_file_path = source_file_path.replace(source_directory, mirror_directory)
        current_mirror_file_directory = os.path.split(mirror_file_path)[0]
        # Checking if directory exists
        if not os.path.exists(current_mirror_file_directory):
            print("Directory " + "'" + os.path.basename(current_mirror_file_directory) + "'" + " doesn't exist, creating.")
            os.makedirs(current_mirror_file_directory)
            print("Created directory ..." + "'" + os.path.dirname(mirror_file_path) + "'")
                
        # Try to copy
        if not os.path.exists(mirror_file_path):
            try:
                copy(source_file_path, mirror_file_path)
            except:
                print("Copy operation failed, unknown error.")
                inc_file_counter(2)
                changelabel("Copying Files.\nProgress: " + str(filescopied + fileshashed + filesfailed) + " of " + str(total_file_count) + ".")
                
        else: # Hash file if already exists
            if hashtype == "MD5":
                srchash = sha512sum(source_file_path)
                mirrorhash = sha512sum(mirror_file_path)
            elif hashtype == "SHA512":
                srchash = sha512sum(source_file_path)
                mirrorhash = sha512sum(mirror_file_path)
            if srchash == mirrorhash:
                print("File " + "'" + file_name + "'" + " exists. Matching " + hashtype + "SUM!")
                inc_file_counter(0)
                changelabel("Copying Files.\nProgress: " + str(filescopied + fileshashed + filesfailed) + " of " + str(total_file_count) + ".")
            else: # Hash different -- proceed with overwrite
                print("File " + "'" + file_name + "'" + " exists, hash didn't match. Overwriting to " + "'" + os.path.dirname(mirror_file_path) + "'"+ ".")
                try:
                    copy(source_file_path, mirror_file_path)
                except:
                    print("Failed to copy " + "'" + file_name + "'" + ".")
                    inc_file_counter(2)
                    changelabel("Copying Files.\nProgress: " + str(filescopied + fileshashed + filesfailed) + " of " + str(total_file_count) + ".")

        
                    

# This is where the fun begins
start()

finished = True
try:#Python3
    messagebox.showinfo("Operation Completed","Total Files Copied: " + str(filescopied) + ". \nTotal Files Hashed: " + str(fileshashed) + ".\nFailed To Copy: " + str(filesfailed) + ".")
except:
    tkMessageBox.showinfo("Operation Completed","Total Files Copied: " + str(filescopied) + ". \nTotal Files Hashed: " + str(fileshashed) + ".\nFailed To Copy: " + str(filesfailed) + ".")
