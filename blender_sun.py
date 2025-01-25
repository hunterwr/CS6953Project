#Functions for the creation of the sun in blender

import bpy

def create_sun(location=(0, 0, 0), radius=1):
    """
    Creates a sphere to represent the sun.

    :param location: Tuple of (x, y, z) coordinates for the sun's position.
    :param radius: Radius of the sun sphere.
    """
    # Add a UV sphere to represent the sun
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radius, 
        location=location
    )
    sun = bpy.context.object
    sun.name = "Sun"

    return sun

def add_glowing_material(obj, color=(1.0, 0.8, 0.0), strength=10):
    """
    Adds an emissive material to the given object to make it glow.

    :param obj: The Blender object to which the material will be applied.
    :param color: The color of the glow as an (R, G, B) tuple.
    :param strength: The emission strength of the material.
    """
    # Create a new material
    material = bpy.data.materials.new(name="SunMaterial")
    material.use_nodes = True

    # Get the material's node tree
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Add emission node
    emission_node = nodes.new(type="ShaderNodeEmission")
    emission_node.inputs[0].default_value = (*color, 1.0)  # RGBA
    emission_node.inputs[1].default_value = strength

    # Add output node
    output_node = nodes.new(type="ShaderNodeOutputMaterial")

    # Connect emission to output
    links.new(emission_node.outputs[0], output_node.inputs[0])

    # Assign the material to the object
    obj.data.materials.append(material)

def setup_sunlight(location=(10, 10, 10), energy=5):
    """
    Sets up a sunlight source in the scene.

    :param location: Tuple of (x, y, z) coordinates for the light's position.
    :param energy: The strength of the sunlight.
    """
    # Add a sunlight object
    bpy.ops.object.light_add(type='SUN', location=location)
    sun_light = bpy.context.object
    sun_light.name = "SunLight"
    
    # Set light energy
    sun_light.data.energy = energy

def create_sun_scene():
    """
    Creates a complete sun setup with a glowing sun sphere and sunlight.
    """
    # Create the sun
    sun = create_sun(location=(0, 0, 0), radius=2)

    # Add glowing material to the sun
    add_glowing_material(sun, color=(1.0, 0.8, 0.0), strength=50)

    # Set up sunlight
    setup_sunlight(location=(10, 10, 10), energy=5)

# Run the function to create the sun scene
if __name__ == "__main__":
    create_sun_scene()
