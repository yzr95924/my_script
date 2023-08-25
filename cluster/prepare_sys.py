import os
import getopt
import sys

old_source_path = "/etc/apt/sources.list"
bak_source_path = "/etc/apt/sources.list.bak"
source_list_lib_path = "./source_list_lib"

def Usage():
    print("{name} -v [the version of the OS]".format(name=__file__))
    print("\t-v: 20 (20.04), 22 (22.04)")
    exit()

def PrepareAPTSource(version: int):
    source_file = ""
    cmd = ""
    if (version == 20):
        source_file = "20_04"
    elif (version == 22):
        source_file = "22_04"
    else:
        Usage()

    print("backup old source list")
    cmd = "sudo cp " + old_source_path + " " + bak_source_path
    print(cmd)
    os.system(cmd)
    new_source_list_path = os.path.join(source_list_lib_path, source_file)
    cmd = "sudo cp " + new_source_list_path + " " + old_source_path
    print(cmd)
    os.system(cmd)
    cmd = "sudo apt-get update"
    print(cmd)
    os.system(cmd)

if __name__ == "__main__":
    options = "-v:-h"
    opts, args = getopt.getopt(sys.argv[1:], options)
    version = 0

    if (len(sys.argv[1:]) == 0):
        Usage()

    for opt_name, opt_value in opts:
        if (opt_name == '-v'):
            version = int(opt_value)
        elif (opt_name == "-h"):
            Usage()
        else:
            print("Invalid option")
            Usage()

    PrepareAPTSource(version)