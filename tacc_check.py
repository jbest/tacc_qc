import argparse
from datetime import datetime
import os
from pathlib import Path
import json
import re

# File extensions that are scanned
#FILE_TYPES = ['.jpg', '.jpeg', '.JPG', '.JPEG']

def show_tree(path=None):
    print('in show_tree:', path)
    for root, dirs, files in os.walk(path):
        print('show_tree_root:', root)

def walk(path=None):
    scan_start_time = datetime.now()
    web_jpg_p = re.compile(web_jpg_regex)
    web_jpg_med_p = re.compile(web_jpg_med_regex)
    web_jpg_thumb_p = re.compile(web_jpg_thumb_regex)
    print(web_jpg_thumb_regex)

    for root, dirs, files in os.walk(path):

        for file in files:
            file_path = Path(root).joinpath(file)
            file_name = file_path.name
            m_web = web_jpg_p.match(file_name)
            m_thumb = web_jpg_thumb_p.match(file_name)
            m_med = web_jpg_med_p.match(file_name)
            #file_ext = file_path.suffix
            if m_web:
                # full sized image
                catalog_number = m_web['catalog_number']
                if catalog_number not in inventory:
                    inventory[catalog_number] = {'catalog_number': catalog_number}
                inventory[catalog_number]['web_jpg'] = file_name
                print('matches web:', file_name)
            if m_thumb:
                print('matches thumb:', file_name)
                catalog_number = m_thumb['catalog_number']
                if catalog_number not in inventory:
                    inventory[catalog_number] = {'catalog_number': catalog_number}
                inventory[catalog_number]['web_jpg_thumb'] = file_name
            if m_med:
                catalog_number = m_med['catalog_number']
                if catalog_number not in inventory:
                    inventory[catalog_number] = {'catalog_number': catalog_number}
                inventory[catalog_number]['web_jpg_med'] = file_name
                print('matches med:', file_name)
            """
            if file_ext in FILE_TYPES:
                print(file_name)
            """
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
directory_path = Path(files.get('output_base_path', None))
file_types = config.get('file_types', None)
#directory_path = os.path.realpath(args["directory"])

web_jpg_regex = file_types['web_jpg']['regex']
web_jpg_med_regex = file_types['web_jpg_med']['regex']
web_jpg_thumb_regex = file_types['web_jpg_thumb']['regex']

inventory = {} # relevant contents of directory path
walk(path=directory_path)
#print(inventory)
for catalog_number, value in inventory.items():
    print(catalog_number, value)


