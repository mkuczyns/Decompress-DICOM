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
import shutil

# DICOM Decompression:

# 1. Read in the input DICOM directory
parser = argparse.ArgumentParser()
parser.add_argument("inputDirectory", type=str, help="The input DICOM directory")
args = parser.parse_args()

inputDirectory = args.inputDirectory + "\\"

print ("Starting decompression...\n")

# Decompress the DICOM files and save them to a new folder:

# 2. Create a new folder for the decompressed DICOM files
savePath = inputDirectory + "DECOMPRESSED\\"

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
    #   4. Default (series # 601)
    #   5. Default (series # 602)
    #   6. Dose Report
    #   7. Localizers
    tag = pydicom.read_file(saveFile)
    seriesDescription = tag[0x0008, 0x103e].value
    seriesNumber = tag[0x0020, 0x0011].value

    # Create a new folder for each series description within and move the current DICOM file
    if (seriesDescription == "Bone Plus"):
        seriesFilePath = savePath + "BONE_PLUS\\"
    
        # Possible race-condition with creating directories like this...
        if not os.path.exists(seriesFilePath):
            os.makedirs(seriesFilePath)
        
        shutil.move(saveFile, seriesFilePath + ogFilename + ".dcm")
                
    elif (seriesDescription == "Standard"):
        seriesFilePath = savePath + "STANDARD\\"

        if not os.path.exists(seriesFilePath):
            os.makedirs(seriesFilePath)
                
        shutil.move(saveFile, seriesFilePath + ogFilename + ".dcm")

    elif (seriesDescription == "no calibration phantom (DFOV)"):
        seriesFilePath = savePath + "NO_CALIBRATION_PHANTOM\\"

        if not os.path.exists(seriesFilePath):
            os.makedirs(seriesFilePath)

        shutil.move(saveFile, seriesFilePath + ogFilename + ".dcm")

    elif (seriesDescription == "Default"):
        seriesFilePath = savePath + "DEFAULT\\"

        if not os.path.exists(seriesFilePath):
            os.makedirs(seriesFilePath)

        if (seriesNumber == 601):
            path601 = seriesFilePath + "SERIES_601\\"

            if not os.path.exists(path601):
                os.makedirs(path601)
            
            shutil.move(saveFile, path601 + ogFilename + ".dcm")

        elif (seriesNumber == 602):
            path602 = seriesFilePath + "SERIES_602\\"

            if not os.path.exists(path602):
                os.makedirs(path602)

            shutil.move(saveFile, path602 + ogFilename + ".dcm")

        else:   
            print ("WHAT")
            shutil.move(saveFile, seriesFilePath + ogFilename + ".dcm")

    elif (seriesDescription == "Dose Report"):
        seriesFilePath = savePath + "DOSE_REPORT\\"

        if not os.path.exists(seriesFilePath):
            os.makedirs(seriesFilePath)

        shutil.move(saveFile, seriesFilePath + ogFilename + ".dcm")
        
    elif  (seriesDescription == "Localizers"):
        seriesFilePath = savePath + "LOCALIZERS\\"

        if not os.path.exists(seriesFilePath):
            os.makedirs(seriesFilePath)

        shutil.move(saveFile, seriesFilePath + ogFilename + ".dcm")
        
    else:
        print ("ERROR: Series description unknown for image: " + saveFile)

print ("\nDONE!")