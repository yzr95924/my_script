#!/usr/bin/python3
# auto pdfcrop all pdf figures under a given dir
import argparse
from os import listdir
from os import path
import os 

def GetAllPDF(dir):
    pdfList = []
    for file in listdir(dir):
        if (file.endswith(".pdf")):
            pdfList.append(path.join(dir, file))
    return pdfList

def CropPDF(inputFile):
    cmd = "pdfcrop " + inputFile
    print(cmd)
    os.system(cmd)
    cropFileName = inputFile[:-4] + "-crop.pdf"
    print(cropFileName)
    cmd = "mv " + cropFileName + " " + inputFile
    print(cmd)
    os.system(cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='auto pdfcrop all pdf figures under a given dir')
    # parser.add_argument('-d', metavar='Directory', nargs=1, help='the path of input directory')
    parser.add_argument("directory", help="the path of the input directory")
    args = parser.parse_args()
    inputDir = str(args.directory)
    print(inputDir)
    pdfList = GetAllPDF(inputDir)
    print(pdfList) 
    for pdf in pdfList:
        CropPDF(pdf)
    print("Done")
