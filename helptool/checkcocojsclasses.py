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

