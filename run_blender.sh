#!/bin/bash

# Define Blender executable path
BLENDER_PATH="/Applications/Blender.app/Contents/MacOS/blender"

# Define Python script path
SCRIPT_PATH="/Users/leeyikai/Desktop/CS6953Project/run.py"

#!/bin/bash

$BLENDER_PATH \
    -b \
    --python $SCRIPT_PATH \
    -- \
    -road_width 20 \
    -road_length 5 \
    -spline_start '10,-50,0' \
    -spline_end '20,50,0' \
    -curvature_points 3 \
    -curvature_score 20 \
    -road_texture 'textures/Roads/Seamless-Road-Texture2.jpg' \
    -road_texture_scaling 6 \
    -sign_width 5 \
    -sign_height 5 \
    -pole_radius 0.2 \
    -pole_height 5 \
    -sign_texture 'textures/Signs/exit_sign.PNG' \
    -pole_texture 'textures/Signs/sign_pole_al.PNG' \
    -trees_positions '40,5,0;50,20,0;-10,-10,0;5,10,0' \
    -tree_seeds '0,2,5,10' \
    -camera_location '0.0,-19.409,14.526' \
    -camera_rotation '69.127,0.000008,0.569964' \
    -camera_scale 1.0 \
    -light_location='-28.398,59.799,19.1' \
    -light_power 3.0 \
    -light_angle 180 \
    -output_image 'output/sign.png' \
    -output_bbox 'output/bbox.txt'

