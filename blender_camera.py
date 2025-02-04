# Camera position funtions


import bpy
import math

def add_camera(location=(0.0, -19.409, 14.526), rotation=(69.127, 0.000008, 0.569964), scale=1.0):
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

    return
