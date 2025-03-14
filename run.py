import bpy
import sys
import os
import argparse
import random

def get_script_directory():
    """
    Returns the directory of this Python file if __file__ is defined,
    otherwise returns the directory of the currently open .blend file.
    """
    if "__file__" in globals():
        return os.path.dirname(os.path.abspath(__file__))
    else:
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
import blender_light_source as light
import blender_save as snap
import blender_bbox as bbox
import blender_plane as plane
import blender_car as car
import blender_sky_texture as sky_texture

def main(args):
    # Reset and Clear the Scene
    utils.clear_scene()
    
    # Place a Road
    road.create_road_edges(
        road_width=args.road_width, road_height=1, 
        road_length=args.road_length,
        left_edge_start = (-(args.road_width/2),-50,0),
        name='Road_Edges',
        target_directory=target_directory,
        conditions='Dry'
    )
    
    # Create the pole
    pole_end_points = signs.create_pole(
        args.pole_radius,
        args.pole_height,
        location=((args.road_width/2) + 3, args.sign_distance, args.pole_height / 2),
        texture_path=os.path.join(target_directory, args.pole_texture)
    )
    
    # Create a simple square sign
    signs.create_sign_square(
        args.sign_width,
        args.sign_height,
        text=None,
        start_location=(
            pole_end_points[0]-5/2,
            pole_end_points[1] - 2.5 * 0.2,
            pole_end_points[2] - 0.25
        ),
        name='Simple Sign'
    )
    
    # Add a sign texture
    sign_obj = bpy.data.objects.get('Simple Sign')
    signs.add_sign_color(
        sign_obj,
        target_directory=target_directory,
        texture_path=args.sign_texture
    )
    
    # Add trees 
    # trees.generate_forest(args.road_width, args.road_length, args.min_tree_dist, args.max_tree_dist, args.num_trees)
    trees.generate_preset_forest(target_directory, args.road_width, args.road_length, args.density, args.distance, args.tree_type)
    
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
        "forrest": "forrest_ground_01",
        "mud": "brown_mud_leaves_01"
    }
    
    plane.create_plane(size=args.ground_plane_size, target_directory=target_directory, material=planes[args.plane])

    # Create a car object downloaded as a glTF file
    car.create_car(target_directory)

    # Add sky texture
    sky_texture.create_sky_texture(time_of_day=args.time_of_day)
    
    # Determine output directory
    base_output_dir = os.path.join(target_directory, "output")
    output_image_dir = get_next_output_directory(base_output_dir)
    
    # Ensure the new directory exists
    os.makedirs(output_image_dir, exist_ok=True)
    
    # Update output paths
    output_image = os.path.join(output_image_dir, "sign_step_")
    output_bbox = os.path.join(output_image_dir, "bbox.txt")
    
    # Render images
    for step in range(args.num_steps):
        camera.location.y += args.step_size
        image_path = f"{output_image}{step}.png"
        snap.render_and_save(image_path, samples=args.samples)
        print(f"Saved Image {step} at {image_path}")
    
    # Save bounding box
    bbox.save_bbox_as_text(
        'Simple Sign',
        'Camera',
        output_bbox
    )
    
    # Ensure proper shading mode
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
                    break

if __name__ == '__main__':
    # Strip Blender arguments
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    
    parser = argparse.ArgumentParser(description='Blender Scene Generation Script')
    parser.add_argument('-road_width', type=int, default=50)
    parser.add_argument('-road_length', type=int, default=300)
    parser.add_argument('-sign_width', type=int, default=5)
    parser.add_argument('-sign_height', type=int, default=5)
    parser.add_argument('-pole_radius', type=float, default=0.2)
    parser.add_argument('-pole_height', type=int, default=5)
    parser.add_argument('-sign_distance', type=int, default=100)
    parser.add_argument('-sign_texture', type=str, default='/exit_sign.PNG')
    parser.add_argument('-pole_texture', type=str, default='textures/Signs/sign_pole_al.PNG')
    parser.add_argument('-camera_location', type=str, default='12.5, -58, 6.68')
    parser.add_argument('-camera_rotation', type=str, default='90, 0, 0')
    parser.add_argument('-camera_scale', type=float, default=1.0)
    parser.add_argument('-light_location', type=str, default='-28.398,59.799,19.12')
    parser.add_argument('-light_power', type=float, default=3.0)
    parser.add_argument('-light_angle', type=int, default=180)
    parser.add_argument('-time_of_day', type=str, default="midday")
    parser.add_argument('-ground_plane_size', type=int, default=1000)
    parser.add_argument('-plane', type=str, default="mud") # rock, snow, mud, forrest
    parser.add_argument('-background', type=str, default="sky") # sky, desert, city
    parser.add_argument('-density', type=str, default="some trees") # no trees, some trees, many trees
    parser.add_argument('-distance', type=str, default="close") # close, far
    parser.add_argument('-tree_type', type=str, default="pine")
    parser.add_argument('-samples', type=int, default=128)
    parser.add_argument('-num_steps', type=int, default=1)
    parser.add_argument('-step_size', type=int, default=5)
        
    args = parser.parse_args(argv)  # Use stripped arguments
    main(args)
