# Really Basic Main script. Copy and paste into scripting window?
# 
#  
import bpy

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

import importlib
importlib.reload(cam)


#Reset and Clear the Scene
utils.clear_scene()


#Place a Road
# road.create_spline_road(width = 15,length = 3,spline_start=(-15,-50,0),spline_end=(20,50,0),curvature_points = 3, 
# curvature_score = 20,texture_path = target_directory + r'/textures/Roads/Seamless-Road-Texture2.jpg',texture_scaling=6)   
road.create_road_edges(road_width=5,road_height=0.25, road_length=20,left_edge_start = (0,0,0),name='Road_Edges',target_directory=target_directory,conditions='Dry')


#Place a basic sign 
sign_width = 5
sign_height = 5
pole_radius = 0.20
pole_height= 5


# Note that cylinder forms from center of 'Location', so we start at the halfway point of the desired pole. 
pole_end_points = signs.create_pole(pole_radius,pole_height,location =(0,0,pole_height/2),texture_path = target_directory + r'/textures/Signs/sign_pole_al.PNG') 

#create a simple square sign 
signs.create_sign_square(sign_width,sign_height,text=None,start_location = (-sign_width/2,
pole_end_points[1]-2.5*pole_radius,pole_end_points[2]-0.25), name='Simple Sign')

#Add a sign texture. Optionally, add text. 
sign_obj = bpy.data.objects.get('Simple Sign')
signs.add_sign_color(sign_obj,target_directory=target_directory,texture_path= r'/textures/Signs/exit_sign.PNG' )


#Add some trees to the area
trees.create_pine_tree("tree1", target_directory, position=(40,5,0), seed=0, ) #
trees.create_pine_tree("tree2", target_directory, position=(50,20,0), seed=2) #
trees.create_pine_tree("tree3", target_directory, position=(-10,-10,0), seed=5) # we will need to fix the file path
trees.create_pine_tree("tree4", target_directory, position=(5,10,0), seed=10) #

#adds a camera in front of the sign object
cam.add_camera(target_directory, location=(0.3, -61.367, 6.6872), rotation=(91.527, 0.0000048, -13.83), scale=1.0)

#adds a light source
light.add_sunlight(location = (-28.398, 59.799, 19.12), power = 3.0, angle = 180)

#creates a plane for the ground surfacen
plane.create_plane(size=1000, target_directory=target_directory, material="forrest_ground_01")

#creates a car object downloaded as gltffile
car.create_car(target_directory)

#adds sky texture
sky_texture.create_sky_texture()
#renders the scene and saves a snap as png
#snap.render_and_save(target_directory + r'/output/sign.png')

#draws a bounding box around the sign object and returns the coordinates in txt file
#bbox.save_bbox_as_text('Simple Sign', 'Camera', target_directory + r'/output/bbox.txt')

bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'



# Ensure an area with type 'VIEW_3D' exists
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'MATERIAL'
                break
