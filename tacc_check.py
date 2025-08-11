"""Derivative File Checker

This script scans the designated directory to determine if all expected image
files are present and records the presence or absences in a CSV file.
This script has no relevant use outside of the context of a TORCH/BRIT
image processing workflow on TACC due to the very specific directory arrangement
and configuration parameters.

The script requires the path of a configuration file which is a JSON format
file containing parameters for image storage.

The output CSV file can be used as the input for tacc_fix.py which will generate
any missing files and the URL mapping file needed for linking images in Symbiota.

"""

import argparse
import datetime
import os
from pathlib import Path
import json
import re
import csv

def walk(path=None):
    # scan_start_time = datetime.now()

    #TODO add (?i) to start of all regex to make case insensitive
    web_jpg_p = re.compile(web_jpg_regex)
    web_jpg_med_p = re.compile(web_jpg_med_regex)
    web_jpg_thumb_p = re.compile(web_jpg_thumb_regex)

    for root, dirs, files in os.walk(path):

        for file in files:
            file_path = Path(root).joinpath(file)
            file_name = file_path.name
            m_web = web_jpg_p.match(file_name)
            m_thumb = web_jpg_thumb_p.match(file_name)
            m_med = web_jpg_med_p.match(file_name)
            #file_ext = file_path.suffix
            #TODO check to make sure file size > 0
            if m_web:
                # full sized image
                catalog_number = m_web['catNum']
                if catalog_number not in inventory:
                    inventory[catalog_number] = {'catalog_number': catalog_number}
                inventory[catalog_number]['web_jpg'] = file_name
                inventory[catalog_number]['web_jpg_path'] = file_path
                #print('matches web:', file_name)
            if m_thumb:
                #print('matches thumb:', file_name)
                catalog_number = m_thumb['catNum']
                if catalog_number not in inventory:
                    inventory[catalog_number] = {'catalog_number': catalog_number}
                inventory[catalog_number]['web_jpg_thumb'] = file_name
                inventory[catalog_number]['web_jpg_thumb_path'] = file_path
            if m_med:
                catalog_number = m_med['catNum']
                if catalog_number not in inventory:
                    inventory[catalog_number] = {'catalog_number': catalog_number}
                inventory[catalog_number]['web_jpg_med'] = file_name
                inventory[catalog_number]['web_jpg_med_path'] = file_path
            # TODO: log unmatched files

# set up argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", required=True, \
    help="Path to the configuration file to be used for processing images.")
ap.add_argument("-d", "--debug", action="store_true", \
    help="Print debug output.")

args = vars(ap.parse_args())
config_file = args['config']
debug = args['debug']

# load config file
with open(config_file) as f:
    config = json.load(f)

collection = config.get('collection', None)
collection_prefix = collection.get('prefix', None)
catalog_number_regex = collection.get('catalog_number_regex', None)
files = config.get('files', None)
#directory_path = Path(files.get('web_base_path', None))
directory_path = Path(collection.get('web_base', None))
file_types = config.get('file_types', None)

#regex = catalog_number_regex + file_regex
# combine collection number regex with file regex
web_jpg_regex = catalog_number_regex + file_types['web_jpg']['file_regex']
web_jpg_med_regex = catalog_number_regex + file_types['web_jpg_med']['file_regex']
web_jpg_thumb_regex = catalog_number_regex + file_types['web_jpg_thumb']['file_regex']

if debug:
    print('collection:', collection)
    print('collection_prefix:', collection_prefix)
    print('files:', files)
    print('directory_path:', directory_path)
    print('file_types:', file_types)
    print('web_jpg_regex:', web_jpg_regex)
    print('web_jpg_med_regex:', web_jpg_med_regex)
    print('web_jpg_thumb_regex:', web_jpg_thumb_regex)
inventory = {}  # relevant contents of directory path
walk(path=directory_path)

now = datetime.datetime.now()
log_filename = collection['name'] + '_tacc_check_output_' + str(now.strftime('%Y-%m-%dT%H%M%S')) + '.csv'
with open(log_filename, 'w', newline='') as csvfile:
    fieldnames = ['catalog_number', 'web_jpg', 'web_jpg_path', 'web_jpg_med', 'web_jpg_med_path', 'web_jpg_thumb', 'web_jpg_thumb_path']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for catalog_number, value in inventory.items():
        #print(catalog_number, value)
        writer.writerow(value)
print('Check complete, results written to:', log_filename)
