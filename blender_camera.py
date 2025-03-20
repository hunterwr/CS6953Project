# Camera position funtions


import bpy
import math
import os

def add_camera(target_directory, background="dunes" , location=(0.0, -19.409, 14.526), rotation=(69.127, 0.000008, 0.569964), scale=1.0):
    """
    Adds a camera to the scene at a specified location, rotation, and scale.

    :location: Tuple (x, y, z) - Camera position in meters.
    :rotation: Tuple (x, y, z) - Camera rotation in degrees.
    :scale: Float - Scale of the camera (default 1.0).
    """
    # Create a new camera object
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.name = "Camera"

    # Set Camera Location
    camera.location = location

    # Convert degrees to radians and set rotation, blender uses radians
    camera.rotation_euler = (
        math.radians(rotation[0]),  # X Rotation
        math.radians(rotation[1]),  # Y Rotation
        math.radians(rotation[2])   # Z Rotation
    )

    # Set Camera Scale
    camera.scale = (scale, scale, scale)

    # Set as active camera
    bpy.context.scene.camera = camera
    
    
    # Adding a background and attach it to camera
    bpy.ops.mesh.primitive_plane_add(size=1)
    background_plane = bpy.context.object
    background_plane.name = "Background Plane"
    
    background_plane.scale = (600.0, 400.0, 0.0)
    background_plane.rotation_euler = camera.rotation_euler
    background_plane.location = (0.0, 380.0, 190.0)
    
    # Set the parent of the background plane to the camera
    background_plane.parent = camera
    background_plane.matrix_parent_inverse = camera.matrix_world.inverted()
    
    # Create a new material
    material = bpy.data.materials.new(name="BackgroundMaterial")
    material.use_nodes = True

    nodes = material.node_tree.nodes
    links = material.node_tree.links

    nodes.clear()

    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    texture_node = nodes.new(type='ShaderNodeTexImage')

    # Set node locations
    output_node.location = (400, 0)
    principled_node.location = (200, 0)
    texture_node.location = (0, 0)
    
    path = f"{target_directory}/textures/Background/{background}.jpg"
    
    if os.path.exists(path):
        image = bpy.data.images.load(path)
        texture_node.image = image
    else:
        return

    # Link nodes
    links.new(texture_node.outputs["Color"], principled_node.inputs["Base Color"])
    links.new(texture_node.outputs['Color'], principled_node.inputs['Emission Color'])
    principled_node.inputs['Emission Strength'].default_value = 0.3
    links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])

    # Assign the material to the background plane
    background_plane.data.materials.append(material)
    
    # Enter edit mode on the background plane and perform cube projection UV unwrap
    bpy.context.view_layer.objects.active = background_plane
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.cube_project()
    bpy.ops.object.mode_set(mode='OBJECT')
    
    #define frames for animation
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 500
        
    return camera
