import sys, os
from core import *
import hashlib


class program():
    def __init__(self,args):
        self.core = core(args)
        self.setup(args)#process the arguments
        self.hashes = []

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
        os.makedirs(self.destinationFolderPath, 0o777, exist_ok = True)

    def md5(self, fname):
        fname = fname.replace("\\","/")
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def process(self, path):
        #try:
        
        fileHash = self.md5(path)
        if fileHash in self.hashes:#File already exist
            print("DUPLICATE", path)
        else:
            self.hashes.append(fileHash)
            print("NO DUPLI", path)
        #self.move(self.sourceFolderPath, element)
        
        #except: 
        #    print("Error 1 with file", path)
    

    def run(self):
        valid=0
        invalid=0

        print("Working...")
        for element in os.listdir(self.sourceFolderPath):
            path=os.path.join(self.sourceFolderPath,element)
            
            if os.path.isfile(path): #is a file
                process(path)
            else:#if folder
                for root, dirs, files in os.walk(path):
                    if not root.endswith("_DUPLICATES"):
                        for filename in files:
                            process(root + "/" + filename)      

        print("{} file.s moved ({} error.s)".format(valid,invalid))
        if invalid !=0 : print("There was an error, please retry the same command")

    def move(self,rootPath,file):#TO DO
        
        sourcePath = rootPath + "/" + file
        destinationPath = self.destinationFolderPath

        if self.validDate(year,month,day):
            if self.printFileNames: print("OK", file)

            if self.flat:
                destinationPath += "/" + year + "-" + month + "-" + day + "/"
            else:
                destinationPath += "/" + year + "/" + month + "/"
                if self.day: destinationPath += day + "/"

        else:#invalid filename
            if self.printFileNames: print("NO",file)
            destinationPath += "/invalid/"

        os.makedirs(destinationPath, 0o777, exist_ok = True)

        destinationFilePath = destinationPath + file

        try: os.rename(sourcePath, destinationFilePath) #we move the file
        except: 
        	print("Error with file",sourcePath) #cannot move file, or file already exists
        	assert False
            
    def stop(self, msg = ""):
        if msg != "": print(msg)
        self.help()
        exit(0)#stop the program

    def help(self):
        print("")
        print("Usage: python duplinder.py -f folder [-d destFolder]")
        print("")
        print("Options:")
        print("    -f path         Path to analyse")
        print("    -d path         Path of the destination folder, where to put duplicates")
        print("                    (Optional, by default it's a subfolder of the source folder)")
        print("")
        print("")
        exit(0)


if __name__ == '__main__':
    prog = program(sys.argv)
    prog.run()