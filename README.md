# DICOM Decompression Project
This project aims to create an easier method of decompressing DICOM images compared to using OsiriX.

## Requirements
1. Python 3.6 or greater
2. Python Libraries:
    - pydicom
    - pillow
    - gdcm
    - argparse
    - errno
    - shutil
3. Compressed DICOM files

## How-to
Run the script as follows:
```python
python decompressDICOM.py PATH_TO_DICOM_FOLDER
```

## TO-DO
- Change the main loop's structure:
    - Chnage the loop format. This should reduce the amount of code and make it more general: Make the loop read in each file's series description, convert it to string, then check if such a directory exists. If it doesn't, create a new directory based on that string. If it does exist, just move the file to that directory.
