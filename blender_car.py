import bpy


def create_car(target_directory):
    path = f'{target_directory}/textures/2020_porsche_718_cayman_gt4/scene.gltf'
    bpy.ops.import_scene.gltf(filepath=path)
    obj = bpy.context.selected_objects[0]
    
    obj.name = "Car"
    obj.scale = (250, 250, 250)
    obj.location = (50, 50, 0)