# Really Basic Main script. Copy and paste into scripting window?
# 
#  
import bpy
import math

import sys
import os

script_name = bpy.context.space_data.text.name

# Get the absolute path of the script
script_filepath = bpy.data.texts[script_name].filepath

script_directory = os.path.dirname(script_filepath)


#### CHANGE TARGET DIRECTORY TO SHARED FOLDER LOCATION######
target_directory = script_directory



os.chdir(target_directory)

sys.path.append(os.getcwd())

import blender_utils as utils
import blender_signs as signs
import blender_road as road 
import blender_trees as trees
import blender_camera as cam
import blender_light_source as light
import blender_save as snap
import blender_bbox as bbox
import blender_plane as plane
import blender_car as car
import blender_sky_texture as sky_texture
import texture_utils as texutils
import blender_weather as weather
import random
import json

import importlib
importlib.reload(sky_texture)

json_path = os.path.join(target_directory, "config_test.json")  # JSON file path
with open(json_path, 'r') as f:
    user_config = json.load(f)

scene_params = utils.generate_random_parameters(user_config)  # Ensures missing values are randomized

class Args:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def simplify_args(args_obj):
    simplified = {}
    for key, value in args_obj.__dict__.items():
        if isinstance(value, list) and value:
            simplified[key] = value[0]
        else:
            simplified[key] = value
    return Args(**simplified)  # Return a new Args object

# Create and simplify the args
args = Args(**scene_params)
args = simplify_args(args)  # Now back to Args class with simplified values

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
    sign_width=args.sign_width)


# # Add trees 
# #trees.generate_forest(args.road_width, args.road_length, args.min_dist, args.max_dist, args.num_trees)
trees.generate_preset_forest(target_directory, road_boundaries, density=args.tree_density, distance_from_road=args.tree_distance, tree_type=args.tree_type)

# Create a plane for the ground surface
planes = {
    "rock": "rocky_trail",
    "snow": "snow_03",
    "forest": "forrest_ground_01",
    "mud": "brown_mud_leaves_01"
}

plane.create_plane(size=args.ground_plane_size, target_directory=target_directory, material=planes[args.plane])
lane_positions = road.warp_scene(x_warp=1,z_warp=0.5,road_preset=args.road_scene)

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





# Add sky texture
sky_texture.create_sky_texture(time_of_day=args.time_of_day)

# Add particles
#weather.add_snow(snow_type=args.snow_type)