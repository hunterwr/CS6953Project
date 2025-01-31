import bpy

import bpy_extras

def get_bounding_box(obj, cam):
    scene = bpy.context.scene
    w, h = scene.render.resolution_x, scene.render.resolution_y

    min_x, min_y, max_x, max_y = float("inf"), float("inf"), float("-inf"), float("-inf") #initialize to infinity to update min/max pixel coordinates

    for vertex in obj.data.vertices:
        world_coord = obj.matrix_world @ vertex.co
        projected2d = bpy_extras.object_utils.world_to_camera_view(scene, cam, world_coord) #blender function to transform 3D to 2D
        x, y = int(projected2d.x * w), int((1 - projected2d.y) * h) #normalizing x & y coordiantes to pixel values
        min_x, min_y = min(min_x, x), min(min_y, y)
        max_x, max_y = max(max_x, x), max(max_y, y)

    return min_x, min_y, max_x, max_y

def save_bbox_as_text(obj_name, cam_name, file_path):
    if obj_name not in bpy.data.objects or cam_name not in bpy.data.objects:
        print("Error: Object or Camera not found!")
        return

    bbox = get_bounding_box(bpy.data.objects[obj_name], bpy.data.objects[cam_name])
    
    with open(file_path, "w") as f:
        f.write(f"{bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n")

    print(f"Saved: {file_path}")

object_name = "Sign" #change to actual object name
camera_name = "Camera" #currenrly default, change to actual camera name
# Change the output path 
output_path = "path/bbox.txt"

save_bbox(object_name, camera_name, output_path)
