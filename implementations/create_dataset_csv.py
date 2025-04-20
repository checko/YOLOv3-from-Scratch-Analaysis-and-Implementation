import os
import json
import pandas as pd
from pathlib import Path
from PIL import Image

def convert_coco_to_yolo(img_width, img_height, bbox):
    """
    Convert COCO bbox (x, y, width, height) to YOLO format (x_center, y_center, width, height)
    All values normalized between 0 and 1
    """
    x, y, width, height = bbox
    
    # Convert to center coordinates
    x_center = (x + width/2) / img_width
    y_center = (y + height/2) / img_height
    
    # Normalize width and height
    width = width / img_width
    height = height / img_height
    
    return [x_center, y_center, width, height]

def create_label_files(coco_json, image_dir, label_dir):
    """
    Create YOLO format label files from COCO JSON annotations
    """
    # Load COCO annotations
    with open(coco_json, 'r') as f:
        coco_data = json.load(f)
    
    # Create mapping of image_id to filename
    image_map = {img['id']: img for img in coco_data['images']}
    
    # Create mapping of image_id to annotations
    annotation_map = {}
    for ann in coco_data['annotations']:
        image_id = ann['image_id']
        if image_id not in annotation_map:
            annotation_map[image_id] = []
        annotation_map[image_id].append(ann)
    
    # Process each image
    for img_data in coco_data['images']:
        img_id = img_data['id']
        img_file = img_data['file_name']
        img_width = img_data['width']
        img_height = img_data['height']
        
        # Get annotations for this image
        annotations = annotation_map.get(img_id, [])
        
        # Create label file
        label_file = Path(img_file).stem + '.txt'
        label_path = os.path.join(label_dir, label_file)
        
        with open(label_path, 'w') as f:
            for ann in annotations:
                # Convert bbox to YOLO format
                bbox = convert_coco_to_yolo(img_width, img_height, ann['bbox'])
                category_id = ann['category_id'] - 1  # YOLO uses 0-based indexing
                
                # Write to file: <class> <x_center> <y_center> <width> <height>
                f.write(f"{category_id} {' '.join(map(str, bbox))}\n")

def create_train_csv(image_dir, label_dir, output_csv):
    """
    Create a CSV file mapping image files to their corresponding label files.
    
    Args:
        image_dir (str): Directory containing the images
        label_dir (str): Directory containing the label files
        output_csv (str): Path where to save the CSV file
    """
    # Get all image files
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    # Create data list
    data = []
    for img_file in sorted(image_files):
        # Get corresponding label file (same name, different extension)
        label_file = Path(img_file).stem + '.txt'
        
        # Check if label file exists
        if os.path.exists(os.path.join(label_dir, label_file)):
            data.append({
                'image_name': img_file,
                'label_name': label_file
            })
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"Created {output_csv} with {len(data)} entries")

if __name__ == "__main__":
    # Define paths
    IMAGE_DIR = "../COCO/images/"
    LABEL_DIR = "../COCO/labels/"
    OUTPUT_CSV = "../COCO/train.csv"
    COCO_JSON = "../COCO/annotations/instances_train2017.json"
    
    # Ensure directories exist
    os.makedirs(IMAGE_DIR, exist_ok=True)
    os.makedirs(LABEL_DIR, exist_ok=True)
    
    # Convert COCO annotations to YOLO format
    print("Converting COCO annotations to YOLO format...")
    create_label_files(COCO_JSON, IMAGE_DIR, LABEL_DIR)
    
    # Create the CSV file
    print("Creating CSV file...")
    create_train_csv(IMAGE_DIR, LABEL_DIR, OUTPUT_CSV)
