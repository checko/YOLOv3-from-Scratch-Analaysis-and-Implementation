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

