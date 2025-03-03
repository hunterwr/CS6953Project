import bpy


def create_sky_texture(time_of_day="dawn"):
    # time_of_day = dawn | midday | dusk | night
    if time_of_day == "dawn":
        sun_elevation = 5
        sun_intensity = 0.45
        background_strength = 0.25
    elif time_of_day == "midday":
        sun_elevation = 60
        sun_intensity = 0.6
        background_strength = 0.4
    elif time_of_day == "dusk":
        sun_elevation = -5
        sun_intensity = 0.4
        background_strength = 0.2
    elif time_of_day == "night":
        sun_elevation = -45  # Lower elevation for night
        sun_intensity = 0.01  # Much lower intensity
        background_strength = 0.02  # Lower overall brightness
    else:
        # Default to dawn
        sun_elevation = 5
        sun_intensity = 0.45
        background_strength = 0.25
    world = bpy.context.scene.world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    nodes.clear()

    sky_texture_node = nodes.new(type='ShaderNodeTexSky')
    sky_texture_node.location = (0, 0)
    sky_texture_node.sun_intensity = sun_intensity
    sky_texture_node.sun_elevation = sun_elevation * (3.14159 / 180)
    sky_texture_node.sun_rotation = 135 * (3.14159 / 180)
    
    background_node = nodes.new(type='ShaderNodeBackground')
    background_node.location = (100, 0)
    background_node.inputs['Strength'].default_value = background_strength
    links.new(sky_texture_node.outputs['Color'], background_node.inputs['Color'])

    output_node = nodes.new(type='ShaderNodeOutputWorld')
    output_node.location = (200, 0)

    links.new(background_node.outputs['Background'], output_node.inputs['Surface'])