import bpy
import sys
import os
import argparse
import random
import json
import glob
import itertools

def ensure_sapling_addon_enabled():
    addon_module = "sapling_tree_gen"
    addon_path = "/home/default/workspace/Add-on/add-on-sapling-tree-gen-fixed.zip"

    # Check if the addon is already installed
    if addon_module in bpy.context.preferences.addons:
        print(f"'{addon_module}' is already installed. Enabling it...")
        bpy.ops.preferences.addon_enable(module=addon_module)
    else:
        print(f"'{addon_module}' is not installed. Installing from ZIP...")
        bpy.ops.preferences.addon_install(filepath=addon_path)
        bpy.ops.preferences.addon_enable(module=addon_module)
        print(f"'{addon_module}' installed and enabled.")

    # Debug: Print all script paths and their contents
    addon_paths = bpy.utils.script_paths()
    for path in addon_paths:
        print(f"Checking: {path}")
        if os.path.exists(path):
            print("Contents:", os.listdir(path))


def get_script_directory():
    """
    Returns the directory of this Python file if __file__ is defined,
    otherwise returns the directory of the currently open .blend file.
    """
    if "__file__" in globals():
        return os.path.dirname(os.path.abspath(__file__))
    
    blend_filepath = bpy.data.filepath
    return os.path.dirname(blend_filepath) if blend_filepath else os.getcwd()

def get_next_output_directory(base_dir):
    """
    Automatically increments the output directory name if it already exists.
    Example: If "samples1" exists, create "samples2".
    """
    i = 1  
    while os.path.exists(os.path.join(base_dir, f"samples{i}")):
        i += 1
    new_dir = os.path.join(base_dir, f"samples{i}")
    os.makedirs(new_dir)
    return new_dir

# Determine target directory
script_directory = get_script_directory()
target_directory = script_directory

os.chdir(target_directory)
sys.path.append(target_directory)
print(target_directory)

import blender_utils as utils
import blender_signs as signs
import blender_road as road
import blender_trees as trees
import blender_camera as cam
import blender_weather as weather
import blender_light_source as light
import blender_save as snap
import blender_bbox as bbox
import blender_plane as plane
import blender_car as car
import blender_sky_texture as sky_texture

# Import our new COCO annotations module
from coco_annotations import COCOAnnotator

def find_previous_annotations(output_dir):
    """
    Look for existing COCO annotations file in the output directory
    """
    annotation_path = os.path.join(output_dir, "coco_annotations.json")
    if os.path.exists(annotation_path):
        return annotation_path
    return None

def generate_scene_and_annotate(args):
    # Reset and Clear the Scene
    utils.clear_scene()


       
    # Place road and sign
    road_boundaries, lane_positions = road.road_presets(scene = args.road_scene, conditions = args.road_conditions, target_directory = target_directory)
    png_path = 'textures/Signs/Signs/PNGs/'
    sign_path = png_path + args.sign + '.png'
    signs.generate_sign(
        road_boundaries,
        sign_path, 
        scratches = args.sign_scratches, 
        rust = args.sign_rust, 
        rivets=False, 
        snow = args.sign_snow, 
        mud = args.sign_mud, 
        target_directory = target_directory, 
        lean_forward_angle=random.gauss(0, args.sign_lean_forward_strength), 
        lean_left_angle=random.gauss(0, args.sign_lean_sideways_strength),   
        spin=random.gauss(0, args.sign_spin_strength),
        sign_size=7)


    # # Add trees 
    # #trees.generate_forest(args.road_width, args.road_length, args.min_dist, args.max_dist, args.num_trees)
    trees.generate_preset_forest(target_directory, road_boundaries, density=args.tree_density, distance_from_road=args.tree_distance, tree_type=args.tree_type)

    plane.create_plane(size=args.ground_plane_size, target_directory=target_directory, material=planes[args.plane])
    
    lane_positions = road.warp_scene(x_warp=1,z_warp=0.5, road_preset=args.road_scene)
    
    # Create a car object downloaded as a glTF file
    #car_obj = car.create_car(target_directory)

    backgrounds = {
        "city": ["burj_khalifa"],
        "sky" : ["salt_flats", "sky_mountains", "sky1", "sky2"],
        "desert" : ["dunes"]
    }
    # Add a camera
    background = random.choice(backgrounds[args.background])
    camera = cam.add_camera(
        target_directory, car=None, lane_positions = lane_positions, camera_lane_number=args.camera_lane_number, background=background
    ) # target_directory, car=None, lane_positions=None, camera_lane_number=2, background="dunes", lane_offset_z=5.0
    
    # Initialize the camera controller
    camera_controller = cam.CameraController(
        camera, 
        road_boundaries,
        sign_name="Simple Sign",
        height_range=(4, 10),
        lane_positions = lane_positions,
        mode="dashcam",
        camera_lane_number=args.camera_lane_number
    )
    
    # Add a light source
    light.add_sunlight(
        location=tuple(map(float, args.light_location.split(','))),
        power=args.light_power,
        angle=args.light_angle
    )
    
    # Create a plane for the ground surface
    planes = {
        "rock": "rocky_trail",
        "snow": "snow_03",
        "forest": "forrest_ground_01",
        "mud": "brown_mud_leaves_01"
    }
    


    # Add sky texture
    sky_texture.create_sky_texture(time_of_day=args.time_of_day)
    
    # Add particles
    weather.add_snow(snow_type=args.snow_type)
    
    # Determine output directory
    base_output_dir = os.path.join(target_directory, "output")
    output_dir = os.path.join(base_output_dir, "samples_multi") #get_next_output_directory(base_output_dir)
    
    previous_annotations = find_previous_annotations(output_dir)
    
    args_dict = vars(args)  # Convert the args object to a dictionary
    try:
        # Initialize COCO annotator with config and previous annotations if found
        coco_annotator = COCOAnnotator(output_dir, args_dict, previous_annotations)
        print("Successfully initialized COCO annotator" + 
              (f" with previous file: {previous_annotations}" if previous_annotations else ""))
    except ValueError as e:
        print(f"ERROR: {str(e)}")
        print("Cannot proceed with invalid previous annotations. Exiting.")
        return
    except FileNotFoundError as e:
        print(f"WARNING: {str(e)}")
        print("Creating new annotations file.")
        coco_annotator = COCOAnnotator(output_dir, args_dict)
    
    for step in range(args.num_images_per_scene):
        # Move camera to next position using the camera controller
        move_success = camera_controller.step(args.step_size)
        print(f"Step {step+1}/{args.num_images_per_scene}: Camera movement {'successful' if move_success else 'adjusted to maintain sign visibility'}")
        
        base_filename = f"image_{step}"
        try:
            # This does everything in one call: renders image, saves bbox, adds to annotations
            image_id = coco_annotator.add_image_with_annotation(
                'Simple Sign', 
                'Camera', 
                base_filename,
                args.frame_number, 
                args.samples
            )
            print(f"Processed image {step} with ID: {image_id}")
        except Exception as e:
            print(f"Error processing image {step}: {str(e)}")
            continue
    
    # Save the COCO annotations file
    coco_annotator.save("coco_annotations.json")
    
    # Ensure proper shading mode
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
                    break


class Args:
        def __init__(self, **entries):
            self.__dict__.update(entries) # Not good because can't see which parameters got errors, but implicit.

def main():
    # Ensure the sapling tree generator addon is enabled
    ensure_sapling_addon_enabled()

    # Force GPU rendering with Cycles
    bpy.context.scene.render.engine = 'CYCLES'
    prefs = bpy.context.preferences
    cycles_prefs = prefs.addons['cycles'].preferences
    cycles_prefs.compute_device_type = 'CUDA'

    cycles_prefs.get_devices()

    for device in cycles_prefs.devices:
        if 'NVIDIA' in device.name:
            device.use = True
            print(f"Enabled GPU device: {device.name}")
        else:
            device.use = False
            print(f"Disabled non-GPU device: {device.name}")

    json_path = os.path.join(target_directory, "config_test.json")  # JSON file path
    with open(json_path, 'r') as f:
        user_config = json.load(f)

    # Get all sign files from the directory
    sign_directory = os.path.join(target_directory, "textures/Signs/Signs/PNGs")
    if os.path.exists(sign_directory):
        all_signs = [os.path.splitext(os.path.basename(file))[0] for file in glob.glob(os.path.join(sign_directory, "*.png"))]
        # Randomly select 5 signs if there are more than 5 available
        if all_signs:
            signs = user_config.get("sign", all_signs)  
        else:
            signs = user_config.get("sign", ["Stop"]) 
    else:
        print(f"Warning: Sign directory not found at {sign_directory}")
        signs = user_config.get("sign", ["Stop"])  # Default to "Stop" if directory not found
    
    num_scenes = user_config.get("num_scenes", 1)
    num_images_per_scene = user_config.get("num_images_per_scene", 1)

    # Identify parameters that are lists (other than "sign" and count-based params)
    list_based_params = {key: value for key, value in user_config.items() 
                         if isinstance(value, list) and key not in ["sign", "num_scenes", "num_images_per_scene"]}
    # Generate all possible combinations of list-based parameters
    param_combinations = list(itertools.product(*list_based_params.values())) if list_based_params else [()]
    
    # Iterate over each sign
    # for sign in signs:
    print(f"Total Number of Images to be generated: {num_scenes * num_images_per_scene * len(param_combinations)}")
    for combo in param_combinations:
        # Assign values from combinations
        combo_args = dict(zip(list_based_params.keys(), combo))

        for scene_index in range(num_scenes):
            print(f"Generating scene {scene_index + 1}/{num_scenes}")
            # Generate new random parameters for the scene
            scene_params = utils.generate_random_parameters(user_config)  # Ensures missing values are randomized

            # Merge user-defined values & generated values
            scene_params.update(combo_args)  # Set list-based parameters
            
            scene_params["sign"] = random.choice(signs)  # Set current sign
            
            # Convert dictionary to object-like structure
            args_instance = Args(**scene_params)

            generate_scene_and_annotate(args_instance)


if __name__ == '__main__':

    main()
