#!/bin/python3
# paprika.py
# https://github.com/R-Rothrock/paprika

from datetime import datetime
from os import chdir, getcwd, mkdir, system
import sys

#%% Getting things ready

DEBUG = True

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

PREINST_PATH  = ""
POSTINST_PATH = ""
DATA_PATH     = ""

if is_debianesque():
    
    class Actions:
        tmp_dir = "/tmp/paprika_" + sys.argv[2]

        def unzip(tmp_dir):
            mkdir(tmp_dir)
            system("dpkg-deb -R %s %s" % (sys.argv[2], tmp_directory))
        
            # setting global variables
            global PREINST_PATH, POSTINST_PATH, DATA_PATH
            PREINST_PATH  = tmp_dir + "/DEBIAN/preinst"
            POSTINST_PATH = tmp_dir + "/DEBIAN/postinst"
            DATA_PATH     = tmp_dir

        def rezip(tmp_directory) -> str:
            """
            returns path to new `.deb` file
            """
            system("dpkg-deb -b %s" % (tmp_directory))

else:

    class Actions:
        wdir = "/tmp/paprika_" + sys.argv[2]

        def unzip(tmp_dir):
            mkdir(tmp_dir)

            # copying
            system("cp %s %s" % (sys.argv[2], wdir))
            deb_file = sys.argv[2].split("/")[-1]
            
            prev_dir = getcwd()
            chdir(tmp_dirf)

            # unzipping .deb
            system("ar -x %s" % (deb_file))
           
            # unzipping `control.tar.gz` & `data.tar.gz`
            system("gzip -d *.gz")
            mkdir("control")
            mkdir("data")
            system("tar -xf control.tar --directory control")
            system("tar -xf data.tar --directory data")
            
            chdir(prev_dir)

            # setting global variables
            global PREINST_PATH, POSTINST_PATH, DATA_PATH
            PREINST_PATH  = tmp_dir + "/control/preinst"
            POSTINST_PATH = tmp_dir + "/control/postinst"
            DATA_PATH     = tmp_dir + "/data"

        def rezip(tmp_directory) -> str:
            """
            returns path to new `.deb` file
            """
            prev_dir = getcwd()
            chdir(tmp_directory)

            # tar
            system("tar -c control -f control.tar")
            system("tar -c data -f data.tar")
            system("rm -rf control data")

            # gzip
            system("gzip control.tar")
            system("gzip data.tar")

            # ar
            system("ar -r new.deb debian_binary control.tar.gz data.tar.gz")

            return getcwd() + "new.deb"

#%% Logging system

class Logger:
    def __init__(self, stream=sys.stdout, debug=True):
        self.stream = stream

        self.debug = debug

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
        if self.debug:
            return
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

l = Logger(debug=DEBUG)

# confirming that files exists
try:
    with open(sys.argv[1], "r") as stream:
        pass
except FileNotFoundError:
    l.error("file %s doesn't exist. Exiting..." % (sys.argv[1]))
try:
    with open(sys.argv[2], "r") as stream:
        pass
except FileNotFoundError:
    l.error("file %s doesn't exist. Exiting..." % (sys.argv[2]))



