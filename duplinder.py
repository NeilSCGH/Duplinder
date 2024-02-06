import sys, os
from core import *
import hashlib


class program():
    def __init__(self,args):
        self.core = core(args)
        self.setup(args)#process the arguments
        self.hashes = []
        self.hashesAndFiles = []

    def setup(self,args):
        #Help
        if self.core.argExist("-h") or self.core.argExist("-help"):
          self.help()

        #the folder for source files
        if self.core.argHasValue("-f"):
          val = self.core.argValue("-f")
          self.sourceFolderPath = val.replace("\\","/")
        else:
          self.stop("Error, -f (source folder) is missing !")

        #the folder for output files
        if self.core.argHasValue("-d"):
          val = self.core.argValue("-d")
          self.destinationFolderPath = val.replace("\\","/")
        else:
          self.destinationFolderPath = self.sourceFolderPath + "/_DUPLICATES"
          
          
        #findOnly : Will only find duplicates, and not move them
        self.findOnly = self.core.argExist("-findOnly")

    def md5(self, fname):
        fname = fname.replace("\\","/")
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def process(self, rootPath, file):
        #try:
        filePath = rootPath + "/" + file
        fileHash = self.md5(filePath)
        self.hashesAndFiles.append([filePath, fileHash])     
        
        #print()
        if fileHash in self.hashes:#File already exist
            #print("DUPLICATE", filePath)
            #print(self.getFilesSameHash(fileHash))
            self.getFilesSameHash(fileHash)
            if not self.findOnly:
                self.move(rootPath, file)
        else:
            self.hashes.append(fileHash)
            if not self.findOnly:
                1#print("NO DUPLIC", filePath)
        
        #except: 
        #    print("Error 1 with file", path)
    
    def getFilesSameHash(self, hash):
        files = []
        for f, h in self.hashesAndFiles:
            if hash == h:
                files.append(f)
                #print("     {}  {}".format(h,f))
        
        return files
    
    def printAllGroups(self):
        for hash in self.hashes:
            for file in self.getFilesSameHash(hash):
                print(file)
            
            print("")
            print("")

    def run(self):
        print("Working...")
        for element in os.listdir(self.sourceFolderPath):
            path=os.path.join(self.sourceFolderPath, element)
            
            if os.path.isfile(path): #is a file
                self.process(self.sourceFolderPath, element)
            else:#if folder
                for root, dirs, files in os.walk(path):
                    if not root.endswith("_DUPLICATES"):
                        for filename in files:
                            self.process(root, filename)    

        print("Done")
        
        self.printAllGroups()
        

    def move(self, rootPath, file):
        sourcePath = rootPath + "/" + file
        destinationPath = self.destinationFolderPath

        os.makedirs(destinationPath, 0o777, exist_ok = True)

        destinationFilePath = destinationPath + "/" + file

        try: os.rename(sourcePath, destinationFilePath) #we move the file
        except: 
        	print("Error with file", sourcePath) #cannot move file, or file already exists
        	assert False
            
    def stop(self, msg = ""):
        if msg != "": print(msg)
        self.help()
        exit(0)#stop the program

    def help(self):
        print("")
        print("Usage: python duplinder.py -f folder [-findOnly] [-d destFolder]")
        print("")
        print("Options:")
        print("    -f path         Path to analyse")
        print("    -findOnly       Don't move files, only show duplicates in the console.")
        print("    -d path         Path of the destination folder, where to put duplicates")
        print("                    (Optional, by default it's a subfolder of the source folder)")
        print("")
        print("")
        exit(0)


if __name__ == '__main__':
    prog = program(sys.argv)
    prog.run()