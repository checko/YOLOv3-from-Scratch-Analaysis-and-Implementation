import os
import pandas as pd
from pathlib import Path

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
    IMAGE_DIR = "../COCO/images/images/"
    LABEL_DIR = "../COCO/labels/labels_new/"
    OUTPUT_CSV = "../COCO/train.csv"
    
    # Ensure COCO directory structure exists
    os.makedirs("../COCO/images/images/", exist_ok=True)
    os.makedirs("../COCO/labels/labels_new/", exist_ok=True)
    
    # Create the CSV file
    create_train_csv(IMAGE_DIR, LABEL_DIR, OUTPUT_CSV)