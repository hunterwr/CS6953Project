import bpy

def add_snow(density=2000, start_frame=1, end_frame=250):
    """
    Adds snow to the scene.

    :param density: The density of the snow particles.
    :param start_frame: The frame at which the snow starts.
    :param end_frame: The frame at which the snow ends.
    """
    bpy.ops.mesh.primitive_plane_add(size=100, location=(0, 10, 60))
    emitter = bpy.context.object
    emitter.name = "Snow_Emitter"
    
    ps = emitter.modifiers.new(name="Snow_Particles", type='PARTICLE_SYSTEM')
    particle_settings = ps.particle_system.settings

    # Configure particle settings for snow
    particle_settings.particle_size = 1.0
    particle_settings.count = 2000  # Adjust for density
    particle_settings.lifetime = 200
    particle_settings.frame_start = 1
    particle_settings.frame_end = 250
    #particle_settings.use_gravity = True  # Enable gravity
    #particle_settings.effector_weights.gravity = 0.5  # Set lower gravity for a slow snowfall effect    
    particle_settings.render_type = 'OBJECT'
    particle_settings.physics_type = 'NEWTON'
    particle_settings.brownian_factor = 5  # Adds random movement
    particle_settings.damping = 0.05  # Slight resistance to movement
    
    # Create ionosphere for snow particles
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.5, location=(50, 0, 0))
    snowflake = bpy.context.object
    snowflake.name = "Snowflake"
    bpy.ops.object.shade_smooth()
    
    '''
    # Create snowflake object
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=(0, 0, 60))
    snowflake = bpy.context.object
    snowflake.name = "Snowflake"
    '''
    # Assign snowflake as the particle object
    bpy.context.view_layer.objects.active = emitter
    particle_settings.instance_object = snowflake
    
    # Hide snowflake reference object
    snowflake.hide_render = True
    emitter.hide_render = True

def add_rain(density=1000, start_frame=1, end_frame=500):
    """
    Adds rain to the scene.

    :param density: The density of the rain particles.
    :param start_frame: The frame at which the rain starts.
    :param end_frame: The frame at which the rain ends.
    """
    bpy.ops.mesh.primitive_plane_add(size=100, location=(0, 10, 60))
    emitter = bpy.context.object
    emitter.name = "Rain_Emitter"
    
    ps = emitter.modifiers.new(name="Rain_Particles", type='PARTICLE_SYSTEM')
    particle_settings = ps.particle_system.settings

    # Configure particle settings for rain
    particle_settings.particle_size = 0.05
    particle_settings.count = density
    particle_settings.lifetime = 100 
    particle_settings.frame_start = start_frame
    particle_settings.frame_end = end_frame
    particle_settings.use_gravity = True
    particle_settings.effector_weights.gravity = 1.0
    particle_settings.render_type = 'OBJECT'
    particle_settings.physics_type = 'NEWTON'
    particle_settings.brownian_factor = 0.0
    particle_settings.damping = 0.01
    
    # Create cylinder for raindrop particles
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=1.5, location=(50, 0, 0))
    raindrop = bpy.context.object
    raindrop.name = "Raindrop"
    bpy.ops.object.shade_smooth()
    
    # Assign raindrop as the particle object
    bpy.context.view_layer.objects.active = emitter
    particle_settings.instance_object = raindrop
    '''
    # Create material and adjust shading properties for wet reflection
    mat = bpy.data.materials.new(name="RainMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Specular"].default_value = 1.0  # Max specular for shiny water effect
    bsdf.inputs["Roughness"].default_value = 0.1  # Slightly rough for realism
    bsdf.inputs["Transmission"].default_value = 1.0  # Transparency effect
    
    # Assign material to raindrop
    raindrop.data.materials.append(mat)
    '''
    # Hide emitter from rendering
    emitter.hide_render = True
    emitter.hide_viewport = True
    
    print("Rain particle system created successfully!")


def add_clouds(density=0.5, height=10, coverage=0.5):
    """
    Adds clouds to the scene.

    :param density: The density of the clouds.
    :param height: The height at which the clouds appear.
    :param coverage: The amount of cloud coverage in the scene.
    """
    pass

def add_wind(strength=5, direction=(1, 0, 0)):
    """
    Adds wind to the scene.

    :param strength: The strength of the wind.
    :param direction: The direction of the wind as a (x, y, z) vector.
    """
    pass

def add_fog(density=0.1, color=(0.5, 0.5, 0.5), start_distance=5, end_distance=50):
    """
    Adds fog or smog to the scene.

    :param density: The density of the fog.
    :param color: The color of the fog as an (r, g, b) tuple.
    :param start_distance: The distance from the camera where the fog starts.
    :param end_distance: The distance from the camera where the fog ends.
    """
    pass

def create_weather_system():
    """
    Creates a weather system by combining various weather elements.
    """
    pass


