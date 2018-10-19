# coding=utf-8
#----------------------------------------------------- 
# decompressDICOM.py
#
# Created by:   Michael Kuczynski
# Created on:   2018.10.19
#
# Modified by:
# Modified on:
#
# Description: Decompresses compressed DICOM images using pydicom.
#----------------------------------------------------- 
#
# Requirements:
#   -Python 2.7, 3.4 or later
#   -pydicom, GDCM, Pillow, argparse
#
# Usage:
#   decompressDICOM.py DICOM_FOLDER
#----------------------------------------------------- 

import pydicom
import os
import argparse
import errno

# Switcher for series description:
def switch(arg):
    switcher = {
        1: "Bone Plus",
        2: "Standard",
        3: "No Calibration Phantom (DFOV)",
        4: "Default",
        5: "Dose Report",
        6: "Localizers",
    }
    return switcher.get(arg, "Invaild series description.")

# DICOM Decompression:

# 1. Read in the input DICOM directory
parser = argparse.ArgumentParser()
parser.add_argument("inputDirectory", type=str, help="The input DICOM directory")
args = parser.parse_args()

inputDirectory = args.inputDirectory + "\\"

print ("Starting decompression...\n")
print (inputDirectory)

# Decompress the DICOM files and save them to a new folder:

# 2. Create a new folder for the decompressed DICOM files
savePath = inputDirectory + "\\decompressed\\"

try:
    os.mkdir(savePath)
except OSError as e:
    if e.errno != errno.EEXIST:     # File already exists error
        raise

# 3. Loop through the entire input folder
#       First decompress the file
#       Next, get the tag of each DICOM image to analyze the series description
#       Finally, place the decompressed image into the correct series folder
for DICOMfile in os.listdir(inputDirectory):
    # Get the next file
    ogFilename = os.fsdecode(DICOMfile)

    # Decompress the file
    ds = pydicom.dcmread(inputDirectory + ogFilename)
    ds.decompress()

    # Save the file to the correct series folder
    saveFile = savePath + ogFilename + ".dcm"

    try:
        ds.save_as(saveFile)
    except OSError as e:
        if e.errno != errno.ENOENT:     # No such file or directory error
            raise
    
    # Get the file's tag and parse out the series description
    # Series description is located at [0x0008, 0x103e] in the tag and can be one of the following:
    #   1. Bone Plus
    #   2. Standard
    #   3. No Calibration Phantom (DFOV)
    #   4. Default (x2)
    #   5. Dose Report
    #   6. Localizers
    tag = pydicom.read_file(saveFile)
    seriesDescription = tag[0x0008, 0x103e].value

    switch(seriesDescription)



''' DEBUGGING:

filename = "00001190" 
print ("FILE: " + inputDirectory + filename)
ds = pydicom.dcmread(inputDirectory + filename)
ds.decompress()
ds.save_as(savePath + filename + ".dcm")

d = pydicom.read_file(savePath + filename + ".dcm")
print (d)
'''

print ("DONE!")