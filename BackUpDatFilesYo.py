# Created by https://github.com/fourminute
# It may look sloppy, but it gets the job done
# Instructions For Use:
# All you need to do is set a source folder(where you'll be backing up your files/folders from).
# And a mirror folder(where to copy the files/folders to).

sources = []
mirrors = []

# List sources and mirrors here!
sources.append("C:\\FolderToBackup") # Root folder?
mirrors.append("B:\\MirrorFolder") # Where to mirror this folder?
# It's that easy.


from shutil import copyfile
import hashlib
import os
hashtype = "MD5"

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
                print("Copied file " + "'" +file + "'" + "...to... \\" + os.path.basename(newdirectory) + "\\" + file)
                
        else:
            srchash = md5sum(st)
            mirrorhash = md5sum(newfilepath)
            if srchash == mirrorhash:
                print("File " + "'" + file + "'" + " exists. Matching " + hashtype + "SUM!")
            else:
                print("File " + "'" + file + "'" + " exists, but hash didn't match. Copying file > " + os.path.dirname(newfilepath))
                copyfile(st, newfilepath)
                    


index = 0
size = len(sources) 
while index < size :
    sourcefiles = [os.path.join(r,file) for r,d,f in os.walk(sources[index]) for file in f]
    mirrorfiles = [os.path.join(r,file) for r,d,f in os.walk(mirrors[index]) for file in f]
    mirror(sourcefiles, mirrorfiles, index)
    index += 1


