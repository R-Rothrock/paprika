#!/bin/python3
# paprika.py
# https://github.com/R-Rothrock/paprika

from datetime import datetime
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

        self.blue   = "\033[34m"
        self.cyan   = "\033[36m"
        self.green  = "\033[32m"
        self.red    = "\033[31m"
        self.yellow = "\033[33m"
        self.reset  = "\033[39m"

    def __get_time(self) -> str:
        now = datetime.now()
        return now.strftime("%H:%M:%S")

    def __get_time_field(self) -> str:
        return "[%s%s%s]" % (self.blue, self.__get_time(), self.reset)

    def debug(self, msg):
        print("%s[%sDEBUG%s]:\t%s" % (
            self.__get_time_field(), self.cyan, self.reset, msg
        ))

    def info(self, msg):
        print("%s[%sINFO%s]:\t%s"% (
            self.__get_time_field(), self.green, self.reset, msg
        ))

    def warning(self, msg):
        print("%s[%sWARNING%s]:\t%s" % (
            self.__get_time_field(), self.yellow, self.reset, msg
        ))
    
    def critical(self, msg):
        print("%s[%sCRITICAL%s]:\t%s" % (
            self.__get_time_field(), self.red, self.reset, msg
        ))

    def error(self, msg):
        print("%s[%sERROR%s]:\t%s" % (
            self.__get_time_field(), self.red, self.reset, msg
        ))

# test
#if __name__ == "__main__":
#    l = Logger()
#    l.debug("Debugging message")
#    l.info("Informational message")
#    l.warning("Warning message")
#    l.critical("Critical message")
#    l.error("Segmentation Fault")

#%% Execution

# TODO

