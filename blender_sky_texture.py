import bpy


def create_sky_texture():
    world = bpy.context.scene.world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    nodes.clear()

    sky_texture_node = nodes.new(type='ShaderNodeTexSky')
    sky_texture_node.location = (0, 0)
    sky_texture_node.sun_intensity = 0.45
    sky_texture_node.sun_elevation = 5  * (3.14159 / 180)
    sky_texture_node.sun_rotation = 135 * (3.14159 / 180)
    
    background_node = nodes.new(type='ShaderNodeBackground')
    background_node.location = (100, 0)
    background_node.inputs['Strength'].default_value = 0.250
    links.new(sky_texture_node.outputs['Color'], background_node.inputs['Color'])

    output_node = nodes.new(type='ShaderNodeOutputWorld')
    output_node.location = (200, 0)

    links.new(background_node.outputs['Background'], output_node.inputs['Surface'])