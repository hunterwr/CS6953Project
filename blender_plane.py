import bpy
import os

def create_material(size, target_directory, texture_type="snow_03"): # rocky_terrain, snow_03, rocky_trail
    path = f"{target_directory}/textures/Surface/{texture_type}/textures"
    files = os.listdir(path)
    
    diff_file = path +"/" + next((f for f in files if "diff" in f), None)
    rough_file = path +"/" + next((f for f in files if "rough" in f), None)
    disp_file = path +"/" + next((f for f in files if "disp" in f), None)
    nor_gl_file = path +"/" + next((f for f in files if "nor_gl" in f), None)
    
    material = bpy.data.materials.new(name="GroundMaterial")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    for node in nodes:
        nodes.remove(node)
        
    tex_coord = nodes.new(type="ShaderNodeTexCoord")
    voronoi_texture = nodes.new(type="ShaderNodeTexVoronoi")
    mapping = nodes.new(type="ShaderNodeMapping")
    base_color = nodes.new(type="ShaderNodeTexImage")
    roughness = nodes.new(type="ShaderNodeTexImage")
    displacement = nodes.new(type="ShaderNodeTexImage")
    normal_tex = nodes.new(type="ShaderNodeTexImage")
    normal_map = nodes.new(type="ShaderNodeNormalMap")
    displacement_node = nodes.new(type="ShaderNodeDisplacement")
    principled_bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    material_output = nodes.new(type="ShaderNodeOutputMaterial")
    
    
    tex_coord.location = (-800, 300)
    voronoi_texture.location = (-700, 300)
    mapping.location = (-600, 300)
    base_color.location = (-400, 400)
    roughness.location = (-400, 200)
    displacement.location = (-400, 0)
    normal_tex.location = (-400, -200)
    normal_map.location = (-200, -200)
    displacement_node.location = (0, -100)
    principled_bsdf.location = (200, 200)
    material_output.location = (400, 200)

    # Load and assign base color texture
    base_color.image = bpy.data.images.load(diff_file)
    roughness.image = bpy.data.images.load(rough_file)
    displacement.image = bpy.data.images.load(disp_file)
    normal_tex.image = bpy.data.images.load(nor_gl_file)
    
    base_color.image.colorspace_settings.name = 'sRGB'
    roughness.image.colorspace_settings.name = 'Non-Color'
    displacement.image.colorspace_settings.name = 'Non-Color'
    normal_tex.image.colorspace_settings.name = 'Non-Color'

    links.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])
    links.new(tex_coord.outputs["Generated"], voronoi_texture.inputs["Vector"])
    voronoi_texture.inputs["Scale"].default_value = size * 0.05
    links.new(voronoi_texture.outputs["Color"],mapping.inputs["Rotation"])
    mapping.inputs["Scale"].default_value[0] = size * 0.04
    mapping.inputs["Scale"].default_value[1] = size * 0.04
    mapping.inputs["Scale"].default_value[2] = 1
    links.new(mapping.outputs["Vector"], base_color.inputs["Vector"])
    links.new(mapping.outputs["Vector"], roughness.inputs["Vector"])
    links.new(mapping.outputs["Vector"], displacement.inputs["Vector"])
    links.new(mapping.outputs["Vector"], normal_tex.inputs["Vector"])

    links.new(base_color.outputs["Color"], principled_bsdf.inputs["Base Color"])
    links.new(roughness.outputs["Color"], principled_bsdf.inputs["Roughness"])

    links.new(normal_tex.outputs["Color"], normal_map.inputs["Color"])
    links.new(normal_map.outputs["Normal"], principled_bsdf.inputs["Normal"])

    links.new(displacement.outputs["Color"], displacement_node.inputs["Height"])
    links.new(displacement_node.outputs["Displacement"], material_output.inputs["Displacement"])

    links.new(principled_bsdf.outputs["BSDF"], material_output.inputs["Surface"])
    
    material.displacement_method = "BOTH"
    displacement_node.inputs["Scale"].default_value = 4
    
    return material


def create_regular_grass(size):
    # Create Grass Plane
    bpy.ops.mesh.primitive_plane_add(size=size)
    grass_plane = bpy.context.object
    grass_plane.name = 'Grass Plane'
    
    grass_plane.location = (0.0, 0.0, -0.2)
    
    # Hair particles system and settings
    bpy.ops.object.modifier_add(type='PARTICLE_SYSTEM')
    particle_system = grass_plane.particle_systems[-1]
    particle_system.name = 'HairParticles'
    
    particle_settings = particle_system.settings
    
    particle_settings.name = 'HairPlaneSettings'
    particle_settings.type = 'HAIR'
    particle_settings.count = size * 700
    particle_settings.hair_length = 3
    particle_settings.use_advanced_hair = True
    particle_settings.brownian_factor = 0.5
    
    # Material base color to make it green
    mat = bpy.data.materials.new(name="HairPlaneMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (0.05, 0.09, 0.03, 1)  # Light gray color
    grass_plane.data.materials.append(mat)


def create_plane(size, target_directory, material="rocky_trail"): # rocky_terrain, snow_03
    
    # Create Surface Plane
    bpy.ops.mesh.primitive_plane_add(size=size)
    ground_plane = bpy.context.object
    ground_plane.name = 'Ground Plane'
    
    # Subdivide the mesh based on size
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=int(size / 10))
    bpy.ops.object.mode_set(mode='OBJECT')
    
    ground_plane.location = (0.0, 0.0, -1.0)
   
    if material == "regular_grass":
         # Material base color
        mat = bpy.data.materials.new(name="GroundPlaneMaterial")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = (0.05, 0.09, 0.03, 1)
        ground_plane.data.materials.append(mat)
        create_regular_grass(size=size)
    else:
        mat = create_material(size, target_directory=target_directory, texture_type=material)
        ground_plane.data.materials.append(mat)
    
    
    # mod = grass_plane.modifiers.new(name="Subdivision", type='SUBSURF')
    # mod.levels = 2  # Increase subdivision levels
    
    