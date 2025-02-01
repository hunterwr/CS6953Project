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


#Reset and Clear the Scene
utils.clear_scene()


#Place a Road
road.create_spline_road(width = 15,length = 3,spline_start=(-15,-50,0),spline_end=(20,50,0),curvature_points = 3, 
curvature_score = 20,texture_path = target_directory + r'./textures/Roads/Seamless-Road-Texture2.jpg',texture_scaling=6)   



#Place a basic sign 
sign_width = 5
sign_height = 5
pole_radius = 0.20
pole_height= 5


# Note that cylinder forms from center of 'Location', so we start at the halfway point of the desired pole. 
pole_end_points = signs.create_pole(pole_radius,pole_height,location =(0,0,pole_height/2),texture_path = target_directory + r'./textures/Signs/sign_pole_al.PNG') 

#create a simple square sign 
signs.create_sign_square(sign_width,sign_height,text=None,start_location = (-sign_width/2,
pole_end_points[1]-2.5*pole_radius,pole_end_points[2]-0.25), name='Simple Sign')

#Add a sign texture. Optionally, add text. 
sign_obj = bpy.data.objects.get('Simple Sign')
signs.add_sign_color(sign_obj,texture_path=target_directory+ r'./textures/Signs/exit_sign.PNG' )




# Ensure an area with type 'VIEW_3D' exists
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'MATERIAL'
                break