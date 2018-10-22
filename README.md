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
- Test on multiple DICOM directories
- Make general for use with any DICOMs
