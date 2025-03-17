import bpy
import bpy_extras

def get_bounding_box(obj, cam):
    """
    DEPRECATION WARNING: This function is kept for backward compatibility.
    Please use COCOAnnotator.get_bounding_box() instead.
    """
    scene = bpy.context.scene
    w, h = scene.render.resolution_x, scene.render.resolution_y

    min_x, min_y, max_x, max_y = float("inf"), float("inf"), float("-inf"), float("-inf") 

    for vertex in obj.data.vertices:
        world_coord = obj.matrix_world @ vertex.co
        projected2d = bpy_extras.object_utils.world_to_camera_view(scene, cam, world_coord) 
        x, y = int(projected2d.x * w), int((1 - projected2d.y) * h) 
        min_x, min_y = min(min_x, x), min(min_y, y)
        max_x, max_y = max(max_x, x), max(max_y, y)

    x = min_x
    y = min_y
    width = max_x - min_x
    height = max_y - min_y
    return x, y, width, height

def save_bbox_as_text(obj_name, cam_name, file_path):
    """
    DEPRECATION WARNING: This function is kept for backward compatibility.
    Please use COCOAnnotator.save_image_and_bbox() instead.
    """
    print("WARNING: Using deprecated function save_bbox_as_text(). Please use COCOAnnotator class instead.")
    
    if obj_name not in bpy.data.objects or cam_name not in bpy.data.objects:
        print("Error: Object or Camera not found!")
        return

    bbox = get_bounding_box(bpy.data.objects[obj_name], bpy.data.objects[cam_name])
    
    with open(file_path, "w") as f:
        f.write(f"{bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n")

    print(f"Saved: {file_path}")

    return bbox

def get_image_dimensions():
    """
    DEPRECATION WARNING: This function is kept for backward compatibility.
    Please use COCOAnnotator.get_image_dimensions() instead.
    """
    scene = bpy.context.scene
    return scene.render.resolution_x, scene.render.resolution_y
