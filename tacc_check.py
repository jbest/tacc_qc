import argparse
from datetime import datetime
import os
from pathlib import Path

def walk(path=None):
    scan_start_time = datetime.now()
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = Path(file).resolve()
            print('file:',file, file_path)



 # set up argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True, \
    help="Path to the directory that contains the images to be analyzed.")
args = vars(ap.parse_args())

directory_path = os.path.realpath(args["directory"])

walk(path=directory_path)
