"""
This script extracts class names from a COCO format annotation JSON file.

Description:
------------
The script reads a COCO format JSON annotation file and extracts all class names 
(category names) defined in the dataset. It's particularly useful when you need 
to get a list of all object categories in a COCO dataset.

Usage:
------
python getcococlassnames.py /path/to/coco/annotations.json

Arguments:
    annotations.json : Path to the COCO format annotation JSON file

Output:
    - Total number of classes
    - List of all class names

Example:
    $ python getcococlassnames.py instances_train2017.json
    total: 80 classes
    ['person', 'bicycle', 'car', ...]
"""

import json
import sys

def list_class_names(coco_annotation_file):
    with open(coco_annotation_file, 'r') as file:
        data = json.load(file)
    
    class_names = [category['name'] for category in data['categories']]
    return class_names

# Example usage
coco_annotation_file = sys.argv[1]
class_names = list_class_names(coco_annotation_file)
print(f"total: {len(class_names)} classes")
print(class_names)

