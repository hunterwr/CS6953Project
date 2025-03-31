import bpy
import sys
import os
import argparse
import random
import json
import glob
import itertools

# Path to the directory where the addon is located
addon_path = "/home/default/workspace/Add-on/add-on-sapling-tree-gen-fixed.zip"
#addon_path = "/home/default/workspace/Add-on/extra-zip-trees.zip"

# Install the addon
bpy.ops.preferences.addon_install(filepath=addon_path)

# Print all installed addons
addon_paths = bpy.utils.script_paths()
for path in addon_paths:
    print(f"Checking: {path}")
    if os.path.exists(path):
        print("Contents:", os.listdir(path))

#Enable the addon
bpy.ops.preferences.addon_enable(module="sapling_tree_gen")


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
    # Force GPU rendering with Cycles
    bpy.context.scene.render.engine = 'CYCLES'
    prefs = bpy.context.preferences
    cycles_prefs = prefs.addons['cycles'].preferences
    cycles_prefs.compute_device_type = 'CUDA'

    cycles_prefs.get_devices()

    for device in cycles_prefs.devices:
        device.use = True
        print(f" $$$$$$$$$$ Enabled device: {device.name}, Type: {device.type}")
    for scene in bpy.data.scenes:
        scene.cycles.device = 'GPU'
       
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
        lean_forward_angle=args.sign_lean_forward_angle, 
        lean_left_angle=args.sign_lean_left_angle, 
        spin=args.sign_spin,
        sign_size = 7)


    # # Add trees 
    # #trees.generate_forest(args.road_width, args.road_length, args.min_dist, args.max_dist, args.num_trees)
    trees.generate_preset_forest(target_directory, road_boundaries, density=args.tree_density, distance_from_road=args.tree_distance, tree_type=args.tree_type)

    lane_positions = road.warp_scene(x_warp=1,z_warp=0.5,road_preset='Highway')
    
    backgrounds = {
        "city": ["burj_khalifa"],
        "sky" : ["salt_flats", "sky_mountains", "sky1", "sky2"],
        "desert" : ["dunes"]
    }
    # Add a camera
    background = random.choice(backgrounds[args.background])
    camera = cam.add_camera(
        target_directory, background=background,
        location=tuple(map(float, args.camera_location.split(','))),
        rotation=tuple(map(float, args.camera_rotation.split(','))),
        scale=args.camera_scale
    )
    
    # Initialize the camera controller
    camera_controller = cam.CameraController(
        camera, 
        road_boundaries,
        sign_name="Simple Sign",
        height_range=(4, 10)
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
    
    plane.create_plane(size=args.ground_plane_size, target_directory=target_directory, material=planes[args.plane])

    # Create a car object downloaded as a glTF file
    car.create_car(target_directory)

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
        move_success = camera_controller.step()
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

def get_value(param_name, args_dict, random_func):
    """Returns a value based on user input or generates a random one if not provided."""
    if param_name in args_dict:
        if isinstance(args_dict[param_name], list):
            return random.choice(args_dict[param_name])  # Pick one from the list
        return args_dict[param_name]  # Use the provided single value
    return random_func()  # Generate a random value

def generate_random_parameters(args_dict):
    """Handles each parameter based on whether it should be user-defined or randomized."""
    
    scene_params = {
        "sign": args_dict.get("sign", ["Stop"]),  # Handled separately as a list
        "num_scenes": get_value("num_scenes", args_dict, lambda: 1),
        "num_images_per_scene": get_value("num_images_per_scene", args_dict, lambda: 1),
        "light_power": get_value("light_power", args_dict, lambda: random.uniform(3.0, 5.0)),
        "background": get_value("background", args_dict, lambda: random.choice(["sky"])), 
        "road_scene": get_value("road_scene", args_dict, lambda: random.choice(["Highway", "Two Lane"])),
        "road_conditions": get_value("road_conditions", args_dict, lambda: random.choice(["Dry", "Wet"])),
        "sign_scratches": get_value("sign_scratches", args_dict, lambda: random.uniform(0.0, 1)),
        "sign_rust": get_value("sign_rust", args_dict, lambda: random.uniform(0.0, 1)),
        "sign_snow": get_value("sign_snow", args_dict, lambda: random.uniform(0.0, 1)),
        "sign_mud": get_value("sign_mud", args_dict, lambda: random.uniform(0.0, 1)),
        "camera_location": get_value("camera_location", args_dict, lambda: "12.5, -58, 6.68"),
        "camera_rotation": get_value("camera_rotation", args_dict, lambda: "90, 0, 0"),
        "camera_scale": get_value("camera_scale", args_dict, lambda: random.uniform(0.8, 1.2)),
        "light_location": get_value("light_location", args_dict, lambda: "-28.398,59.799,19.12"),
        "light_angle": get_value("light_angle", args_dict, lambda: random.uniform(160, 200)),
        "time_of_day": get_value("time_of_day", args_dict, lambda: random.choice(["dawn", "midday", "dusk", "night"])),
        "ground_plane_size": get_value("ground_plane_size", args_dict, lambda: 1000),
        "plane": get_value("plane", args_dict, lambda: random.choice(["snow", "rock", "forest", "mud"])), 
        "tree_density": get_value("tree_density", args_dict, lambda: random.choice(["no trees", "some trees", "many trees"])),
        "tree_distance": get_value("tree_distance", args_dict, lambda: random.choice(["close", "far"])),
        "tree_type": get_value("tree_type", args_dict, lambda: random.choice(["pine", "birch"])),
        "snow_type": get_value("snow_type", args_dict, lambda: random.choice(["moderate"])),
        "frame_number": get_value("frame_number", args_dict, lambda: 450),
        "samples": get_value("samples", args_dict, lambda: random.choice([64])),
        "step_size": get_value("step_size", args_dict, lambda: random.choice([5])),
        "sign_lean_forward_angle": get_value("sign_lean_forward_angle", args_dict, lambda: random.uniform(0, 10)),
        "sign_lean_left_angle": get_value("sign_lean_left_angle", args_dict, lambda: random.uniform(0,10)),
        "sign_spin": get_value("sign_spin", args_dict, lambda: random.uniform(0, 10)),
        "post_processing_strength": get_value("post_processing_strength", args_dict, lambda: random.uniform(0.3, 0.4)),
    }

    return scene_params

class Args:
        def __init__(self, **entries):
            self.__dict__.update(entries) # Not good because can't see which parameters got errors, but implicit.

def main():
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
            scene_params = generate_random_parameters(user_config)  # Ensures missing values are randomized

            # Merge user-defined values & generated values
            scene_params.update(combo_args)  # Set list-based parameters
            
            scene_params["sign"] = random.choice(signs)  # Set current sign
            
            # Convert dictionary to object-like structure
            args_instance = Args(**scene_params)

            generate_scene_and_annotate(args_instance)


if __name__ == '__main__':

    main()
