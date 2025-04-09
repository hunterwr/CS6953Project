import os
import json
import datetime
import uuid
from typing import Dict, List, Any, Tuple, Optional, Set
import bpy
from functools import partial
from mathutils import Vector
import bpy_extras
import numpy as np


class COCOAnnotator:
    def __init__(self, output_dir: str, config: Dict[str, Any], previous_file: Optional[str] = None):
        """Initialize COCO annotation structure with metadata from config"""
        self.output_dir = output_dir
        self.config = config
        self.image_id = 0
        self.annotation_id = 0
        self.existing_image_names: Set[str] = set()
        
        # Create paths for images and labels
        self.image_dir = os.path.join(output_dir, 'images')
        self.labels_dir = os.path.join(output_dir, 'labels')
        
        # Ensure directories exist
        os.makedirs(self.image_dir, exist_ok=True)
        os.makedirs(self.labels_dir, exist_ok=True)
        
        # Get the sign name from config and create a category name
        sign_file = config.get("sign", "unknown_sign.png")
        self.sign_category = self._extract_sign_name(sign_file)
        
        # Category mapping (id -> name) and reverse mapping (name -> id)
        self.categories = {}
        self.category_names = {}
        
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
            "categories": [],
            "images": [],
            "annotations": []
        }
        
        # Try to load previous annotations if file path is provided
        if previous_file:
            try:
                self._load_previous_file(previous_file)
            except Exception as e:
                raise ValueError(f"Error processing previous annotations file: {str(e)}")
        
        # Initialize categories
        if not self.coco_data["categories"]:
            # Start with ID 1 for the first category if no previous file
            self._add_category(self.sign_category, supercategory="traffic_sign")
        else:
            # Make sure our current sign is in the categories list
            self._ensure_category_exists(self.sign_category, supercategory="traffic_sign")
        
        # Import the dashcam post-processing module
        try:
            from dashcam_postprocessing import process_and_save
            self.process_and_save = process_and_save
            self.post_processing_available = True
            # Get post-processing strength from config or use default
            self.post_processing_strength = float(config.get("post_processing_strength", 0.7))
            print(f"Post-processing initialized with strength: {self.post_processing_strength}")
        except ImportError:
            self.post_processing_available = False
            print("Warning: dashcam_postprocessing module not found. Post-processing will be skipped.")
    
    def _extract_sign_name(self, sign_file: str) -> str:
        """Extract a clean category name from the sign filename"""
        # Remove file extension
        name = os.path.splitext(sign_file)[0]
        
        # Remove any path components
        name = os.path.basename(name)
        
        # Replace special characters with underscore
        import re
        name = re.sub(r'[^\w\s]', '_', name)
        
        # Replace spaces with underscores and make lowercase for consistency
        name = name.replace(' ', '_').lower()
        
        return name
    
    def _add_category(self, name: str, supercategory: str = "sign") -> int:
        """
        Add a new category to the dataset.
        Returns the category ID.
        """
        # Find the next available category ID
        next_id = 1
        if self.coco_data["categories"]:
            next_id = max(cat["id"] for cat in self.coco_data["categories"]) + 1
            
        category = {
            "id": next_id,
            "name": name,
            "supercategory": supercategory
        }
        
        # Add to COCO data
        self.coco_data["categories"].append(category)
        
        # Update our category mappings
        self.categories[next_id] = name
        self.category_names[name] = next_id
        
        print(f"Added new category: {name} (ID: {next_id})")
        return next_id
    
    def _ensure_category_exists(self, name: str, supercategory: str = "sign") -> int:
        """
        Check if a category exists, add it if it doesn't.
        Returns the category ID.
        """
        # Update internal category mappings from the COCO data
        self.categories = {cat["id"]: cat["name"] for cat in self.coco_data["categories"]}
        self.category_names = {cat["name"]: cat["id"] for cat in self.coco_data["categories"]}
        
        # Check if category exists by name
        if name in self.category_names:
            return self.category_names[name]
        
        # Category doesn't exist, add it
        return self._add_category(name, supercategory)
    
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
        
        # Update our category mappings after loading
        self.categories = {cat["id"]: cat["name"] for cat in self.coco_data["categories"]}
        self.category_names = {cat["name"]: cat["id"] for cat in self.coco_data["categories"]}
    
    def generate_unique_filename(self, base_name: str) -> str:
        """
        Generate a unique filename that doesn't collide with existing ones
        by appending a timestamp and random string
        """
        # Get timestamp for uniqueness
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Add a unique identifier (first 6 chars of a UUID)
        unique_id = str(uuid.uuid4())[:6]
        
        # Create a unique filename with timestamp and random ID
        unique_name = f"{base_name}_{timestamp}_{unique_id}"
        
        return unique_name

    # def save_image_and_bbox(self, obj_name: str, cam_name: str, base_filename: str = "image", 
    #                        frame_number: int = 450, samples: int = 128) -> Tuple[str, Tuple[float, float, float, float]]:
    #     """
    #     Renders, saves an image and its bounding box, and returns paths and bbox data
        
    #     Args:
    #         obj_name: Name of the object to track with bounding box
    #         cam_name: Name of the camera to render from
    #         base_filename: Base name for the saved files
    #         samples: Render samples
            
    #     Returns:
    #         Tuple of (image_path, bbox_data)
    #     """
    #     # Check if objects exist
    #     if obj_name not in bpy.data.objects or cam_name not in bpy.data.objects:
    #         raise ValueError(f"Object '{obj_name}' or camera '{cam_name}' not found in scene")
        
    #     # Get a unique filename
    #     filename = self.generate_unique_filename(base_filename)
        
    #     # Set paths
    #     image_path = os.path.join(self.image_dir, f"{filename}.png")
    #     bbox_path = os.path.join(self.labels_dir, f"{filename}_bbox.txt")
        
    #     # Check that we don't have this exact filename already
    #     while os.path.exists(image_path):
    #         filename = self.generate_unique_filename(base_filename)
    #         image_path = os.path.join(self.image_dir, f"{filename}.png")
    #         bbox_path = os.path.join(self.labels_dir, f"{filename}_bbox.txt")
            
    #     # Render and save image
    #     scene = bpy.context.scene
    #     #Continue animation to update particles in scene
    #     #frame_number = 450 set to arbitrary value
        
    #     for i in range(1, frame_number + 1):
    #         scene.frame_set(i)

    #     scene.frame_set(frame_number) #set desired frame for output

    #     scene.render.filepath = image_path
    #     scene.render.engine = 'CYCLES'
    #     scene.cycles.device = 'GPU'
    #     scene.render.image_settings.file_format = 'PNG'
    #     scene.cycles.samples = samples
    #     bpy.ops.render.render(write_still=True)
    #     print(f"Saved image to: {image_path}")
        
    #     # Apply post-processing to make it look like dashcam footage
    #     if hasattr(self, 'post_processing_available') and self.post_processing_available:
    #         try:
    #             print(f"Applying dashcam post-processing effects to {image_path}")
    #             self.process_and_save(image_path, strength=self.post_processing_strength)
    #         except Exception as e:
    #             print(f"Warning: Failed to apply post-processing: {str(e)}")
        
    #     # Calculate bounding box
    #     bbox = self.get_bounding_box(bpy.data.objects[obj_name], bpy.data.objects[cam_name])
        
    #     # Save bounding box as text file
    #     with open(bbox_path, "w") as f:
    #         f.write(f"{bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n")
    #     print(f"Saved bounding box to: {bbox_path}")
        
    #     return image_path, bbox
    
    def save_image_and_bbox(self, obj_name: str, cam_name: str, base_filename: str = "image", 
                        frame_number: int = 450, samples: int = 128) -> Tuple[str, Tuple[float, float, float, float]]:
        if obj_name not in bpy.data.objects or cam_name not in bpy.data.objects:
            raise ValueError(f"Object '{obj_name}' or camera '{cam_name}' not found in scene")

        obj = bpy.data.objects[obj_name]
        cam = bpy.data.objects[cam_name]

        # Check visibility BEFORE rendering
        if not self.is_bbox_fully_in_view(obj, cam, bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y):
            print(f"Skipping image render — '{obj_name}' bounding box not fully in camera view.")
            raise ValueError("Bounding box not fully in frame")

        filename = self.generate_unique_filename(base_filename)
        image_path = os.path.join(self.image_dir, f"{filename}.png")
        bbox_path = os.path.join(self.labels_dir, f"{filename}_bbox.txt")

        while os.path.exists(image_path):
            filename = self.generate_unique_filename(base_filename)
            image_path = os.path.join(self.image_dir, f"{filename}.png")
            bbox_path = os.path.join(self.labels_dir, f"{filename}_bbox.txt")

        scene = bpy.context.scene
        for i in range(1, frame_number + 1):
            scene.frame_set(i)
        scene.frame_set(frame_number)

        scene.render.filepath = image_path
        scene.render.engine = 'CYCLES'
        scene.cycles.device = 'GPU'
        scene.render.image_settings.file_format = 'PNG'
        scene.cycles.samples = samples

        bpy.ops.render.render(write_still=True)
        print(f"Saved image to: {image_path}")

        if hasattr(self, 'post_processing_available') and self.post_processing_available:
            try:
                print(f"Applying dashcam post-processing effects to {image_path}")
                self.process_and_save(image_path, strength=self.post_processing_strength)
            except Exception as e:
                print(f"Warning: Failed to apply post-processing: {str(e)}")

        bbox = self.get_bounding_box(obj, cam)

        with open(bbox_path, "w") as f:
            f.write(f"{bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n")
        print(f"Saved bounding box to: {bbox_path}")

        return image_path, bbox

    
    def get_bounding_box(self, obj, cam):
        """
        Calculate bounding box of object from camera perspective
        Returns (x, y, width, height) in COCO format
        """
        import bpy_extras
        # lattice = bpy.data.objects.get('Road_Lattice')
        scene = bpy.context.scene
        w, h = scene.render.resolution_x, scene.render.resolution_y

        depsgraph = bpy.context.evaluated_depsgraph_get()
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.to_mesh()
        transformed_verts = np.array([eval_obj.matrix_world @ v.co for v in mesh.vertices])
        
        min_x, min_y, max_x, max_y = float("inf"), float("inf"), float("-inf"), float("-inf")
        
        # for vertex in obj.data.vertices:
        #     world_coord = obj.matrix_world @ vertex.co
        #     # world_coord_postwarp = lattice.matrix_world @ world_coord_prewarp 
        #     projected2d = bpy_extras.object_utils.world_to_camera_view(scene, cam, world_coord)
        #     x, y = int(projected2d.x * w), int((1 - projected2d.y) * h)
        #     min_x, min_y = min(min_x, x), min(min_y, y)
        #     max_x, max_y = max(max_x, x), max(max_y, y)

        for vert in transformed_verts:
        # Project the transformed world coordinate to camera space

            if isinstance(vert, np.ndarray):
                vert = Vector(vert)  # Convert numpy array to Blender Vector
            projected2d = bpy_extras.object_utils.world_to_camera_view(scene, cam, vert)
            x, y = int(projected2d.x * w), int((1 - projected2d.y) * h)
            min_x, min_y = min(min_x, x), min(min_y, y)
            max_x, max_y = max(max_x, x), max(max_y, y)

        # Convert to COCO format: [x, y, width, height]
        x = min_x
        y = min_y
        width = max_x - min_x
        height = max_y - min_y
        return x, y, width, height
    
    def is_bbox_fully_in_view(obj, camera_obj, image_width, image_height) -> bool:
        """
        Check if the object's bounding box is fully within the camera frame.
        """
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)

        coords_2d = [
            bpy_extras.object_utils.world_to_camera_view(bpy.context.scene, camera_obj, obj_eval.matrix_world @ Vector(corner))
            for corner in obj_eval.bound_box
        ]

        for coord in coords_2d:
            x, y = coord.x, coord.y
            if coord.z < 0 or x < 0.0 or y < 0.0 or x > 1.0 or y > 1.0:
                return False

        return True
        
    def get_image_dimensions(self):
        """Return the current render resolution as (width, height)"""
        scene = bpy.context.scene
        return scene.render.resolution_x, scene.render.resolution_y
    
    def add_image_with_annotation(self, obj_name: str, cam_name: str, base_filename: str = "image", 
                                  frame_number: int = 400, samples: int = 128) -> int:
        """
        Combined method to render image, save bbox, and add both to COCO annotations.
        Returns the image ID.
        """
        # Save image and get bbox
        image_path, bbox_data = self.save_image_and_bbox(obj_name, cam_name, base_filename, frame_number, samples)
        
        # Get image dimensions
        img_width, img_height = self.get_image_dimensions()
        
        # Add to COCO annotations
        image_id = self.add_image(image_path, img_width, img_height)
        self.add_annotation(image_id, bbox_data)
        
        return image_id

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
        
        # Get the category ID for the current sign
        category_id = self.category_names.get(self.sign_category, 1)
        
        annotation_info = {
            "id": annotation_id,
            "image_id": image_id,
            "category_id": category_id,  # Use the specific sign category
            "segmentation": [],  # No segmentation for now
            "area": area,
            "bbox": list(bbox),  # [x, y, width, height]
            "iscrowd": 0,
            # Include sign-related metadata from config
            "metadata": {
                "sign_width": self.config.get("sign_width", ""),
                "sign_height": self.config.get("sign_height", ""),
                "sign_texture": self.config.get("sign", "").split('/')[-1],
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
        category_literal = [f'{cat["name"]} (ID: {cat["id"]})' for cat in self.coco_data['categories']]
        print(f"Categories: {', '.join(category_literal)}")
