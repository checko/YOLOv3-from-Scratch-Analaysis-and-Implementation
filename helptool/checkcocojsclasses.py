"""
COCO JSON Class ID Validator

This script validates COCO format JSON annotation files by checking if any annotations
contain category IDs greater than 80 (the maximum number of classes in standard COCO dataset).

Purpose:
    - Helps identify any invalid class IDs in COCO format annotations
    - Useful for debugging annotation files before training YOLO models
    - Prints detailed information about any annotations with invalid category IDs

Usage:
    python checkcocojsclasses.py path/to/annotations.json

Arguments:
    json_file_path: Path to the COCO format JSON annotation file

Example:
    python checkcocojsclasses.py instances_train2017.json

Output:
    - If invalid annotations are found:
        Shows the count of invalid annotations and lists their IDs and category IDs
    - If no invalid annotations:
        Displays a confirmation message
"""

import json
import sys

def check_class_ids(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    annotations = data.get('annotations', [])
    invalid_annotations = [ann for ann in annotations if ann.get('category_id', 0) > 80]
    
    if invalid_annotations:
        print(f"Found {len(invalid_annotations)} annotations with class ID larger than 80.")
        for ann in invalid_annotations:
            print(f"Annotation ID: {ann['id']}, Class ID: {ann['category_id']}")
    else:
        print("No annotations with class ID larger than 80 found.")

# Example usage
json_file_path = sys.argv[1]
check_class_ids(json_file_path)

