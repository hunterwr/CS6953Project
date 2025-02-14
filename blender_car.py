import bpy


def create_car(target_directory):
    path = f'{target_directory}/textures/2020_porsche_718_cayman_gt4/scene.gltf'
    bpy.ops.import_scene.gltf(filepath=path)
    car_object = bpy.context.selected_objects[0]
    
    car_object.name = "Porsche"
    car_object.scale = (510.0, 510.0, 510.0)
    car_object.location = (23.5, -10.1, 0.0)
    car_object.rotation_quaternion = (0.053, -0.053, -0.705, 0.705)
    
    wheel_pivot = bpy.data.objects.get("Wheel1A_3D_35")
    wheel_pivot.rotation_quaternion = (1.0, 0.0, 0.0, 0.02)
    
            
