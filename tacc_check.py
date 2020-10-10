import argparse
from datetime import datetime
import os
from pathlib import Path
import json
import re

# File extensions that are scanned
FILE_TYPES = ['.jpg', '.jpeg', '.JPG', '.JPEG']

def show_tree(path=None):
    print('in show_tree:', path)
    for root, dirs, files in os.walk(path):
        print('show_tree_root:', root)

def walk(path=None):
    scan_start_time = datetime.now()
    for root, dirs, files in os.walk(path):

        for file in files:
            file_path = Path(root).joinpath(file)
            file_name = file_path.name
            file_ext = file_path.suffix
            if file_ext in FILE_TYPES:
                print(file_name)
            #file_path = Path(file).resolve()
            #print('file:',file, file_path)

 # set up argument parser
ap = argparse.ArgumentParser()
#ap.add_argument("-d", "--directory", required=True, \
#    help="Path to the directory that contains the images to be analyzed.")
ap.add_argument("-c", "--config", required=True, \
    help="Path to the configuration file to be used for processing images.")

args = vars(ap.parse_args())
config_file = args['config']

# load config file
with open(config_file) as f:
    config = json.load(f)

collection = config.get('collection', None)
collection_prefix = collection.get('prefix', None)
files = config.get('files', None)
#folder_increment = int(files.get('folder_increment', 1000))
#log_directory_path = Path(files.get('log_directory_path', None))
#number_pad = int(files.get('number_pad', 7))
directory_path = Path(files.get('output_base_path', None))

#directory_path = os.path.realpath(args["directory"])


walk(path=directory_path)
