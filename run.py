import bpy
import sys
import os
import argparse
import random
import json
import glob

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

def main(args):
    # Reset and Clear the Scene
    utils.clear_scene()
    # Force GPU rendering with Cycles
    bpy.context.scene.render.engine = 'CYCLES'
    prefs = bpy.context.preferences
    cycles_prefs = prefs.addons['cycles'].preferences
    cycles_prefs.compute_device_type = 'CUDA' 
    for device in cycles_prefs.devices:
        device.use = True
        print(f" $$$$$$$$$$ Enabled device: {device.name}, Type: {device.type}")
    for scene in bpy.data.scenes:
        scene.cycles.device = 'GPU'
       
    # Place road and sign
    road_boundaries, lane_positions = road.road_presets(scene = args.road_scene, conditions = args.road_conditions, target_directory = target_directory)
    png_path = 'textures/Signs/Signs/PNGs/'
    sign_path = png_path + args.sign + '.png'
    signs.generate_sign(road_boundaries,sign_path, scratches = args.scratches, rust = args.rust, rivets=False, snow = args.snow, mud = args.mud, target_directory = target_directory )

    
    # # Add trees 
    # #trees.generate_forest(args.road_width, args.road_length, args.min_dist, args.max_dist, args.num_trees)
    # trees.generate_preset_forest(target_directory, road_width, road_length, args.density, args.distance, args.tree_type)
    
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
    output_dir = os.path.join(base_output_dir, "samples11") #get_next_output_directory(base_output_dir)
    
    previous_annotations = find_previous_annotations(output_dir)
    
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
    
    for step in range(args.num_steps):
        # Move camera to next position using the camera controller
        move_success = camera_controller.step()
        print(f"Step {step+1}/{args.num_steps}: Camera movement {'successful' if move_success else 'adjusted to maintain sign visibility'}")
        
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

if __name__ == '__main__':
    # # Strip Blender arguments
    # argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    
    # parser = argparse.ArgumentParser(description='Blender Scene Generation Script')
    # parser.add_argument('-road_width', type=int, default=50)
    # parser.add_argument('-road_length', type=int, default=300)
    # parser.add_argument('-sign_width', type=int, default=5)
    # parser.add_argument('-sign_height', type=int, default=5)
    # parser.add_argument('-pole_radius', type=float, default=0.2)
    # parser.add_argument('-pole_height', type=int, default=5)
    # parser.add_argument('-sign_distance', type=int, default=100)
    # parser.add_argument('-sign_texture', type=str, default='/exit_sign.PNG')
    # parser.add_argument('-pole_texture', type=str, default='textures/Signs/sign_pole_al.PNG')
    # parser.add_argument('-camera_location', type=str, default='12.5, -58, 6.68')
    # parser.add_argument('-camera_rotation', type=str, default='90, 0, 0')
    # parser.add_argument('-camera_scale', type=float, default=1.0)
    # parser.add_argument('-light_location', type=str, default='-28.398,59.799,19.12')
    # parser.add_argument('-light_power', type=float, default=3.0)
    # parser.add_argument('-light_angle', type=int, default=180)
    # parser.add_argument('-time_of_day', type=str, default="midday") # day, midday, dusk
    # parser.add_argument('-ground_plane_size', type=int, default=1000)
    # parser.add_argument('-plane', type=str, default="mud") # rock, snow, mud, forest
    # parser.add_argument('-background', type=str, default="sky") # sky, desert, city
    # parser.add_argument('-density', type=str, default="some trees") # no trees, some trees, many trees
    # parser.add_argument('-distance', type=str, default="close") # close, far
    # parser.add_argument('-tree_type', type=str, default="pine")
    # parser.add_argument('-samples', type=int, default=128)
    # parser.add_argument('-num_steps', type=int, default=1)
    # parser.add_argument('-step_size', type=int, default=5)
        
    # args = parser.parse_args(argv)  # Use stripped arguments
    # Load arguments from JSON file
    json_path = os.path.join(target_directory, "config.json") # JSON file path
    with open(json_path, 'r') as f:
        args_dict = json.load(f)

    class Args:
        def __init__(self, **entries):
            self.__dict__.update(entries) # Not good because can't see which parameters got errors, but implicit.

    args = Args(**args_dict)
    
    main(args)
