import bpy
import math

def add_sunlight(location=(0.0, 0.0, 0.0), rotation=(0, 0, 0), power=3.0, angle=1.0):
    """
    Adds a Sun light to the scene with adjustable intensity and angle.

    :location: Tuple (x, y, z) - Sun position in meters.
    :rotation: Tuple (x, y, z) - Sun rotation in degrees.
    :power: Float - Sunlight intensity (default is 3.0).
    :angle: Float - Sunlight angle in degrees(default 180).
    """

    # Create a new Sun Light source
    light_data = bpy.data.lights.new(name="SceneSunLight", type='SUN')
    light_data.energy = power  # Adjust intensity
    light_data.angle = math.radians(angle)  # Soft shadow angle (used in Sun light)

    # Create light object
    light_obj = bpy.data.objects.new(name="SceneSunLight", object_data=light_data)
    bpy.context.collection.objects.link(light_obj)  # Link light to the scene

    # Set Sunlight Location
    light_obj.location = location

    return
