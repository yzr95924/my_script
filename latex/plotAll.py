#!/usr/bin/python3
# auto plot all R-script under a given dir
import getopt
import os
import sys

exector_path = "Rscript"

def Usage():
    print("auto plot all R-script under a given dir.")
    print("./{file} -i [input_folder] -o [output_folder]")

def GetAllSubDir(input_dir: str):
    subdir_list = []
    directory_content = sorted(os.listdir(input_dir))
    for item in directory_content:
        full_path = os.path.join(input_dir, item)
        if (os.path.isdir(full_path)):
            subdir_list.append(full_path)
    return subdir_list

def PrintPDF(input_dir: str, output_dir: str):
    directory_content = sorted(os.listdir(input_dir))
    for item in directory_content:
        if (item.endswith(".r")):
            full_path = os.path.join(input_dir, item)
            cmd = exector_path + " " + full_path
            print(cmd)
            os.system(cmd)

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "i:o:h")
    input_dir = ""
    output_dir = ""
    for opt_name, opt_value in opts:
        if (opt_name == "-i"):
            input_dir = opt_value
        elif (opt_name == "-o"):
            output_dir = opt_value
        elif (opt_name == "-h"):
            Usage()
            exit()
        else:
            Usage()
            exit()
    subdir_list = []
    subdir_list = GetAllSubDir(input_dir=input_dir) 
    
    for item in subdir_list:
        PrintPDF(input_dir=item, output_dir=output_dir)
            
    