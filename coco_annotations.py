import os
import json
import datetime
from typing import Dict, List, Any, Tuple, Optional, Set

class COCOAnnotator:
    def __init__(self, output_dir: str, config: Dict[str, Any], previous_file: Optional[str] = None):
        """Initialize COCO annotation structure with metadata from config"""
        self.output_dir = output_dir
        self.config = config
        self.image_id = 0
        self.annotation_id = 0
        self.existing_image_names: Set[str] = set()
        
        # Initialize default COCO format structure
        self.coco_data = {
            "info": {
                "description": "Synthetic traffic sign dataset",
                "url": "",
                "version": "1.0",
                "year": datetime.datetime.now().year,
                "contributor": "Blender Synthetic Data Generator",
                "date_created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "licenses": [
                {
                    "id": 1,
                    "name": "Synthetic Data License",
                    "url": ""
                }
            ],
            "categories": [
                {
                    "id": 1,
                    "name": "traffic_sign",
                    "supercategory": "sign"
                }
            ],
            "images": [],
            "annotations": []
        }
        
        # Try to load previous annotations if file path is provided
        
        if previous_file:
            try:
                self._load_previous_file(previous_file)
            except Exception as e:
                raise ValueError(f"Error processing previous annotations file: {str(e)}")
    
    def _validate_coco_format(self, data: Dict[str, Any]) -> bool:
        """
        Validate that the loaded data conforms to COCO format
        Returns True if valid, raises ValueError with details if invalid
        """
        required_keys = ["info", "images", "annotations", "categories"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required key '{key}' in COCO annotations")
        
        # Validate images format
        if not isinstance(data["images"], list):
            raise ValueError("'images' must be a list")
        
        for img in data["images"]:
            required_img_keys = ["id", "file_name", "width", "height"]
            for key in required_img_keys:
                if key not in img:
                    raise ValueError(f"Image missing required key: {key}")
        
        # Validate annotations format
        if not isinstance(data["annotations"], list):
            raise ValueError("'annotations' must be a list")
            
        for ann in data["annotations"]:
            required_ann_keys = ["id", "image_id", "category_id", "bbox"]
            for key in required_ann_keys:
                if key not in ann:
                    raise ValueError(f"Annotation missing required key: {key}")
            
            # Ensure bbox is proper format [x, y, width, height]
            if not isinstance(ann["bbox"], list) or len(ann["bbox"]) != 4:
                raise ValueError(f"Invalid bbox format in annotation {ann['id']}")
        
        # Validate categories format
        if not isinstance(data["categories"], list):
            raise ValueError("'categories' must be a list")
            
        for cat in data["categories"]:
            if "id" not in cat or "name" not in cat:
                raise ValueError("Category missing required id or name")
                
        return True
    
    def _load_previous_file(self, file_path: str) -> None:
        """
        Load and validate a previous COCO annotations file
        Updates image_id and annotation_id to continue from previous file
        """
        print(f"Loading previous annotations from: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Previous annotations file not found: {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                previous_data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse JSON in {file_path}")
        
        # Validate format
        self._validate_coco_format(previous_data)
        print("Previous annotations file format is valid")
        
        # Update our current data with previous data
        self.coco_data = previous_data
        
        # Track existing image filenames to avoid duplicates
        self.existing_image_names = {img["file_name"] for img in previous_data["images"]}
        
        # Set starting IDs to be one more than the highest existing IDs
        if previous_data["images"]:
            self.image_id = max(img["id"] for img in previous_data["images"]) + 1
        
        if previous_data["annotations"]:
            self.annotation_id = max(ann["id"] for ann in previous_data["annotations"]) + 1
            
        print(f"Continuing with image_id: {self.image_id}, annotation_id: {self.annotation_id}")
        print(f"Found {len(self.existing_image_names)} existing images in annotations")
        
    def add_image(self, file_path: str, width: int, height: int) -> int:
        """
        Add an image to the COCO dataset and return its ID
        Checks for duplicate filenames to avoid adding the same image twice
        """
        # Extract filename from the full path
        filename = os.path.basename(file_path)
        
        # Check if this image already exists in the dataset
        if filename in self.existing_image_names:
            print(f"Warning: Image {filename} already exists in annotations, skipping")
            # Return the existing image ID
            for img in self.coco_data["images"]:
                if img["file_name"] == filename:
                    return img["id"]
        
        image_id = self.image_id
        self.image_id += 1
        self.existing_image_names.add(filename)
        
        image_info = {
            "id": image_id,
            "file_name": filename,
            "width": width,
            "height": height,
            "date_captured": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "license": 1,
            # Include relevant config parameters as image metadata
            "metadata": {
                "time_of_day": self.config.get("time_of_day", ""),
                "plane": self.config.get("plane", ""),
                "background": self.config.get("background", ""),
                "density": self.config.get("density", ""),
                "distance": self.config.get("distance", ""),
                "tree_type": self.config.get("tree_type", "")
            }
        }
        
        self.coco_data["images"].append(image_info)
        return image_id

    def add_annotation(self, image_id: int, bbox: Tuple[float, float, float, float]) -> int:
        """
        Add an annotation to the COCO dataset and return its ID
        bbox should be in COCO format: [x, y, width, height]
        """
        annotation_id = self.annotation_id
        self.annotation_id += 1
        
        # Calculate area as width * height
        area = bbox[2] * bbox[3]
        
        annotation_info = {
            "id": annotation_id,
            "image_id": image_id,
            "category_id": 1,  # traffic_sign category
            "segmentation": [],  # No segmentation for now
            "area": area,
            "bbox": list(bbox),  # [x, y, width, height]
            "iscrowd": 0,
            # Include sign-related metadata from config
            "metadata": {
                "sign_width": self.config.get("sign_width", ""),
                "sign_height": self.config.get("sign_height", ""),
                "sign_texture": self.config.get("sign_texture", "").split('/')[-1],
            }
        }
        
        self.coco_data["annotations"].append(annotation_info)
        return annotation_id
    
    def save(self, output_file: str = "coco_annotations.json") -> None:
        """Save the COCO dataset to a JSON file"""
        output_path = os.path.join(self.output_dir, output_file)
        
        # Final validation before saving
        try:
            self._validate_coco_format(self.coco_data)
        except ValueError as e:
            print(f"Warning: Invalid COCO data before saving: {e}")
            print("Attempting to fix issues...")
            # Basic fixes could be implemented here
        
        with open(output_path, 'w') as f:
            json.dump(self.coco_data, f, indent=2)
        
        print(f"COCO annotations saved to {output_path}")
        print(f"Total images: {len(self.coco_data['images'])}")
        print(f"Total annotations: {len(self.coco_data['annotations'])}")
