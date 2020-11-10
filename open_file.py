import os
import sys
import tarfile

def open_file(argv):
    if tarfile.is_tarfile(argv):
        print('decompressing tarfile ' + str(argv))
        os.chdir('/tmp')
        tar = tarfile.open(argv)
        tar.extractall()
        tar.close()
        os.chdir('/tmp/tmp/task-export*/')
    else:
        print('This file is not a valid tar file')
        sys.exit(0)