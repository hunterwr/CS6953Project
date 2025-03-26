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

import importlib
importlib.reload(sky_texture)


#Reset and Clear the Scene
utils.clear_scene()


# road.create_road_edges(
#         road_width=50,road_height=1, 
#         road_length=300,
#         left_edge_start = (-(50/2),-50,0),
#         name='Road_Edges',
#         target_directory=target_directory,
#         conditions='Dry')

road_boundaries, lane_positions = road.road_presets(scene = 'Highway', conditions = 'Dry',target_directory = target_directory)
png_path = 'textures/Signs/Signs/PNGs/Loose Gravel.png'
signs.generate_sign(road_boundaries,png_path,scratches =0.0, rust = 0.0,rivets=False,snow = 0.0,mud = 0.0, target_directory = target_directory, lean_forward_angle=0, lean_left_angle=0, spin=0 )



print(f"Road Boundaries: {road_boundaries}")
# # Create the pole
# pole_end_points = signs.create_pole(
#     0.2,
#     5,
#     location=(road_boundaries[2][0] + 3, 50, 5 / 2),
#     texture_path=os.path.join(target_directory, 'textures/Signs/sign_pole_al.PNG')
# )

# # Create a simple square sign
# signs.create_sign_square(
#     5,
#     5,
#     text=None,
#     start_location=(
#         pole_end_points[0]-5/2,
#         pole_end_points[1] - 2.5 * 0.2,
#         pole_end_points[2] - 0.25
#     ),
#     name='Simple Sign'
# )

# # Add a sign texture
# sign_obj = bpy.data.objects.get('Simple Sign')

# texutils.apply_sign_png_conditions(sign_obj,png_path = os.path.join(target_directory,'textures/Signs/Signs/PNGs/Loose Gravel.png'),
#                                     scratches_on =0.5, rust_minor_on = 0.0, rust_major_on = False,rivets_on=False,snow=0.5,target_directory = target_directory)



road_width = 50
road_length = 300
min_tree_dist = 3
max_tree_dist = 30
num_trees = 10

# Add trees 
trees.generate_preset_forest(target_directory, road_boundaries, density='some trees', distance_from_road='far', tree_type='pine')
# min_dist is the distance from the road to the nearest tree
# max_dist is the distance from the road to the farthest tree

background = "sky1"
camera_location= '12.5, -58, 6.68'
camera_rotation = '90, 0, 0'
camera_scale = 1.0

# Add a camera
cam.add_camera(
    target_directory, background=background,
    location=tuple(map(float, camera_location.split(','))),
    rotation=tuple(map(float, camera_rotation.split(','))),
    scale=camera_scale
)

light_location = '-28.398,59.799,19.12'
light_angle = 180
light_power = 3.0

# Add a light source
light.add_sunlight(
    location=tuple(map(float, light_location.split(','))),
    power=light_power,
    angle=light_angle
)

ground_plane_size = 1000
ground_plane_material = 'forrest_ground_01'

#creates a plane for the ground surfacen
plane.create_plane(size=ground_plane_size, target_directory=target_directory, material=ground_plane_material)

#creates a car object downloaded as gltffile
car.create_car(target_directory)

#adds sky texture
sky_texture.create_sky_texture(time_of_day="dawn")

weather.add_snow(snow_type="heavy")
# output_image = 'output/sign.png'
# samples = 256
# output_bbox = 'output/bbox.txt'
# # Render and save the scene
# snap.render_and_save(os.path.join(target_directory, output_image), samples=samples)

# # Save bounding box
# bbox.save_bbox_as_text(
#     'Simple Sign',
#     'Camera',
#     os.path.join(target_directory, output_bbox)
# )

# Ensure proper shading mode
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'MATERIAL'
                break