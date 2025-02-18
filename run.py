import bpy
import sys
import os
import argparse

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

# Determine target directory
script_directory = get_script_directory()
target_directory = script_directory

os.chdir(target_directory)
sys.path.append(target_directory)

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
    road.create_spline_road(
        width=args.road_width,
        length=args.road_length,
        spline_start=tuple(map(float, args.spline_start.split(','))),
        spline_end=tuple(map(float, args.spline_end.split(','))),
        curvature_points=args.curvature_points,
        curvature_score=args.curvature_score,
        texture_path=os.path.join(target_directory, args.road_texture),
        texture_scaling=args.road_texture_scaling
    )
    
    # Create the pole
    pole_end_points = signs.create_pole(
        args.pole_radius,
        args.pole_height,
        location=(0, 0, args.pole_height / 2),
        texture_path=os.path.join(target_directory, args.pole_texture)
    )
    
    # Create a simple square sign
    signs.create_sign_square(
        args.sign_width,
        args.sign_height,
        text=None,
        start_location=(
            -args.sign_width / 2,
            pole_end_points[1] - 2.5 * args.pole_radius,
            pole_end_points[2] - 0.25
        ),
        name='Simple Sign'
    )
    
    # Add a sign texture
    sign_obj = bpy.data.objects.get('Simple Sign')
    signs.add_sign_color(
        sign_obj,
        texture_path=os.path.join(target_directory, args.sign_texture)
    )
    
    # Add trees 
    trees.generate_forest(args.road_width, args.road_length, args.min_tree_dist, args.max_tree_dist, args.num_trees)
    # min_dist is the distance from the road to the nearest tree
    # max_dist is the distance from the road to the farthest tree

    
    # Add a camera
    cam.add_camera(
        target_directory, background=args.background,
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
    
    #creates a plane for the ground surfacen
    plane.create_plane(size=args.ground_plane_size, target_directory=target_directory, material=args.ground_plane_material)

    #creates a car object downloaded as gltffile
    car.create_car(target_directory)

    #adds sky texture
    sky_texture.create_sky_texture()
    
    # Render and save the scene
    snap.render_and_save(os.path.join(target_directory, args.output_image))
    
    # Save bounding box
    bbox.save_bbox_as_text(
        'Simple Sign',
        'Camera',
        os.path.join(target_directory, args.output_bbox)
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
    parser.add_argument('-road_width', type=int, default=15)
    parser.add_argument('-road_length', type=int, default=3)
    parser.add_argument('-spline_start', type=str, default='-15,-50,0')
    parser.add_argument('-spline_end', type=str, default='20,50,0')
    parser.add_argument('-curvature_points', type=int, default=3)
    parser.add_argument('-curvature_score', type=int, default=20)
    parser.add_argument('-road_texture', type=str, default='textures/Roads/Seamless-Road-Texture2.jpg')
    parser.add_argument('-road_texture_scaling', type=int, default=6)
    parser.add_argument('-sign_width', type=int, default=5)
    parser.add_argument('-sign_height', type=int, default=5)
    parser.add_argument('-pole_radius', type=float, default=0.2)
    parser.add_argument('-pole_height', type=int, default=5)
    parser.add_argument('-sign_texture', type=str, default='textures/Signs/exit_sign.PNG')
    parser.add_argument('-pole_texture', type=str, default='textures/Signs/sign_pole_al.PNG')
    parser.add_argument('-trees_positions', type=str, default='40,5,0;50,20,0;-10,-10,0;5,10,0')
    parser.add_argument('-tree_seeds', type=str, default='0,2,5,10')
    parser.add_argument('-camera_location', type=str, default='0.0,-19.409,14.526')
    parser.add_argument('-camera_rotation', type=str, default='69.127,0.000008,0.569964')
    parser.add_argument('-camera_scale', type=float, default=1.0)
    parser.add_argument('-light_location', type=str, default='-28.398,59.799,19.12')
    parser.add_argument('-light_power', type=float, default=3.0)
    parser.add_argument('-light_angle', type=int, default=180)
    parser.add_argument('-ground_plane_size', type=int, default=1000)
    parser.add_argument('-ground_plane_material', type=str, default="forrest_ground_01")
    parser.add_argument('-background', type=str, default="sky_mountains")
    parser.add_argument('-output_image', type=str, default='output/sign.png')
    parser.add_argument('-output_bbox', type=str, default='output/bbox.txt')
    parser.add_argument('-min_tree_dist', type=int, default=3)
    parser.add_argument('-max_tree_dist', type=int, default=30)
    parser.add_argument('-num_trees', type=int, default=10)
    
    args = parser.parse_args(argv)  # Use stripped arguments
    main(args)
