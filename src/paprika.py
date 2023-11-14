#!/bin/python3
# paprika.py
# https://github.com/R-Rothrock/paprika

from os import chdir, mkdir, system
import sys

#%% Getting things ready

MIN_ARGC = 3
MAX_ARGC = 3

def is_debianesque() -> bool:
    """
    Whether or not the system is Debian-esque and has the required
    programs.
    This is done via searching for `/usr/bin/dpkg-deb`, which is the
    program in question.
    Returns a boolean.
    """

    return True # TODO try

if len(sys.argv) < MIN_ARGC or len(sys.argv) > MAX_ARGC:
    print("USAGE: %s [EXECUTABLE] [.DEB FILE]" % (sys.argv[0]))
    sys.exit()

if is_debianesque():
    
    class FileData:
        tmp_dir = "/tmp/paprika_" + sys.argv[2]

        def unzip(tmp_directory):
            mkdir(tmp_directory)
            system("dpkg-deb -R %s %s" % (sys.argv[2], tmp_directory))
        
        preinst_path = tmp_dir + "/DEBIAN/preinst"

        def rezip(tmp_directory):
            system("dpkg-deb -b ", tmp_directory)

else:

    class FileData:
        tmp_dir = "/tmp/paprika_" + sys.argv[2]

        def unzip(tmp_directory):
            mkdir(tmp_directory)
            system("cp %s %s" % (sys.argv[2], tmp_directory))

    """ old code I'm still referencing
    mkdir(tmp_dir)
    system("mv %s %s" % (sys.argv[2], tmp_dir))
    chdir(tmp_dir)
    system("ar -x %s # I _think_ this is the command..." % (sys.argv[2]))
    # zips should be .gz or .xz
    # no support for anything else
    # lacks error checking
    system("gzip -d *.gz")
    system("xz -d *.gz")

    # extracting tars
    system("tar -xf control.tar -C ./control/")
    system("tar -xf data.tar -C ./data/")

    # remove `md5sum` file if there is one
    system("rm ./control/md5sums")
    """

#%% Logging system

class Logger:
    def __init__(self, stream=sys.stdout):
        self.stream = stream
        
        # TODO (I can't remember these things for the life of me)
        self.blue   = 
        self.green  = 
        self.red    = 
        self.yellow = 
        self.reset  =

    def __get_time(self):
        return # TODO

    def debug(self):
        return # TODO

    def info(self):
        return # TODO

    def warning(self):
        return # TODO
    
    def critical(self):
        return # TODO

#%% Execution

l = Logger()

# TODO

