import bpy
import math
import mathutils
import random

def clear_scene():
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

    current_mode = bpy.context.object.mode

    if current_mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.mode_set(mode='OBJECT')

    for obj in bpy.data.objects:
        # Collect all Geometry Nodes modifiers
        geo_modifiers = [mod for mod in obj.modifiers if mod.type == 'NODES']

        # Remove each Geometry Nodes modifier from the object
        for mod in geo_modifiers:
            obj.modifiers.remove(mod)
            
    for node_group in bpy.data.node_groups:
        if node_group.bl_idname == 'GeometryNodeTree':
            bpy.data.node_groups.remove(node_group)
            
    # Delete all objects (mesh and non-mesh)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Clear all materials from the Blender file
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)

    # Clear all mesh data from the Blender file
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)

    # Clear all other data blocks (like textures, images, etc.)
    for texture in bpy.data.textures:
        bpy.data.textures.remove(texture)

    for image in bpy.data.images:
        bpy.data.images.remove(image)


        
    for curves in bpy.data.curves:
        bpy.data.curves.remove(curves)


def wipe_blender():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    

def apply_blenderkit_material(obj_name, asset_base_id, keyword):
    obj = bpy.data.objects.get(obj_name)
    if obj:
        # Download and apply material using asset_base_id
        bpy.ops.view3d.blenderkit_disclaimer_widget(message="Use the 'S' key over the asset bar to search similar assets.", url="https://github.com/BlenderKit/blenderkit/wiki/BlenderKit-add-on-documentation#assetbar", fadeout_time=8, tip=True)
        bpy.data.window_managers["WinMan"].blenderkitUI.asset_type = 'MATERIAL'
        bpy.data.window_managers["WinMan"].blenderkit_mat.search_keywords = keyword
        bpy.ops.scene.blenderkit_download(asset_index=0, target_object=obj_name, material_target_slot=0, model_rotation=(0, 0, 0))
        bpy.ops.view3d.blenderkit_download_gizmo_widget(asset_base_id=asset_base_id)


        print(f"BlenderKit material {asset_base_id} applied to {obj_name}.")
    else:
        print(f"Object '{obj_name}' not found!")
    

def rotate_objects(objects, angle, axis='Z', pivot_point=(0, 0, 0)):
    """
    Rotates multiple objects around a common pivot point.

    Parameters:
    - objects (list): List of objects to rotate.
    - angle (float): Rotation angle in degrees.
    - axis (str): Axis to rotate around ('X', 'Y', or 'Z').
    - pivot_point (tuple): Coordinates of the pivot point (x, y, z).
    """
    # Convert angle to radians
    angle_rad = math.radians(angle)

    # Create rotation matrix
    rotation_matrix = mathutils.Matrix.Rotation(angle_rad, 4, axis.upper())

    # Pivot point as a vector
    pivot_vector = mathutils.Vector(pivot_point)

    # Rotate each object
    for obj in objects:
        obj.matrix_world = (
            mathutils.Matrix.Translation(pivot_vector) @
            rotation_matrix @
            mathutils.Matrix.Translation(-pivot_vector) @
            obj.matrix_world
        )

def get_value(param_name, args_dict, random_func):
    """Returns a value based on user input or generates a random one if not provided."""
    if param_name in args_dict:
        if isinstance(args_dict[param_name], list):
            return random.choice(args_dict[param_name])  # Pick one from the list
        return args_dict[param_name]  # Use the provided single value
    return random_func()  # Generate a random value

def generate_random_parameters(args_dict):
    """Handles each parameter based on whether it should be user-defined or randomized."""
    
    scene_params = {
        "sign": args_dict.get("sign", ["Stop"]),  # Handled separately as a list
        "num_scenes": get_value("num_scenes", args_dict, lambda: 1),
        "num_images_per_scene": get_value("num_images_per_scene", args_dict, lambda: 1),
        "light_power": get_value("light_power", args_dict, lambda: random.uniform(3.0, 5.0)),
        "background": get_value("background", args_dict, lambda: random.choice(["sky"])), 
        "road_scene": get_value("road_scene", args_dict, lambda: random.choice(["Highway", "Two Lane"])),
        "road_conditions": get_value("road_conditions", args_dict, lambda: random.choice(["Dry", "Wet"])),
        "sign_scratches": get_value("sign_scratches", args_dict, lambda: random.uniform(0.0, 1)),
        "sign_rust": get_value("sign_rust", args_dict, lambda: random.uniform(0.0, 1)),
        "sign_snow": get_value("sign_snow", args_dict, lambda: random.uniform(0.0, 1)),
        "sign_mud": get_value("sign_mud", args_dict, lambda: random.uniform(0.0, 1)),
        "camera_lane_number": get_value("camera_lane_number", args_dict, lambda: random.choice([2, 3])),
        "light_location": get_value("light_location", args_dict, lambda: "-28.398,59.799,19.12"),
        "light_angle": get_value("light_angle", args_dict, lambda: random.uniform(160, 200)),
        "time_of_day": get_value("time_of_day", args_dict, lambda: random.choice(["dawn", "midday", "dusk", "night"])),
        "ground_plane_size": get_value("ground_plane_size", args_dict, lambda: 1000),
        "plane": get_value("plane", args_dict, lambda: random.choice(["snow", "rock", "forest", "mud"])), 
        "tree_density": get_value("tree_density", args_dict, lambda: random.choice(["no trees", "some trees", "many trees"])),
        "tree_distance": get_value("tree_distance", args_dict, lambda: random.choice(["close", "far"])),
        "tree_type": get_value("tree_type", args_dict, lambda: random.choice(["pine", "birch"])),
        "snow_type": get_value("snow_type", args_dict, lambda: random.choice(["moderate"])),
        "frame_number": get_value("frame_number", args_dict, lambda: 450),
        "samples": get_value("samples", args_dict, lambda: random.choice([64])),
        "step_size": get_value("step_size", args_dict, lambda: random.choice([5])),
        "sign_lean_forward_strength": get_value("sign_lean_forward_strength", args_dict, lambda: random.uniform(0, 10)),
        "sign_lean_sideways_strength": get_value("sign_lean_sideways_strength", args_dict, lambda: random.uniform(0,10)),
        "sign_spin_strength": get_value("sign_spin_strength", args_dict, lambda: random.uniform(0, 10)),
        "post_processing_strength": get_value("post_processing_strength", args_dict, lambda: random.uniform(0.3, 0.4)),
    }

    return scene_params