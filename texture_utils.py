    ####Place custom functions to apply textures appropriately here####
import bpy, mathutils

def apply_blenderkit_wetRoad(obj,target_directory):
    tex_path=target_directory+r'/textures/Roads/wet_road_textures_2k/'
    albedo = r'WET ROAD 2_Albedo.jpg'
    ao = r'WET ROAD 2_AO.jpg'
    disp = r'WET ROAD 2_Displacement.exr'
    metal = r'WET ROAD 2_Metalness.jpg'
    normal  = r'WET ROAD 2_Normal.jpg'
    rough = r'WET ROAD 2_Roughness.jpg'


    mat = bpy.data.materials.new(name = "4K Wet road 02")
    mat.use_nodes = True
    #initialize 4K Wet road 02 node group
    def _4k_wet_road_02_node_group():

        _4k_wet_road_02 = mat.node_tree
        #start with a clean node tree
        for node in _4k_wet_road_02.nodes:
            _4k_wet_road_02.nodes.remove(node)
        _4k_wet_road_02.color_tag = 'NONE'
        _4k_wet_road_02.description = ""
        _4k_wet_road_02.default_group_node_width = 140
        

        #_4k_wet_road_02 interface

        #initialize _4k_wet_road_02 nodes
        #node Frame
        frame = _4k_wet_road_02.nodes.new("NodeFrame")
        frame.label = "Mapping"
        frame.name = "Frame"
        frame.label_size = 20
        frame.shrink = True

        #node Frame.001
        frame_001 = _4k_wet_road_02.nodes.new("NodeFrame")
        frame_001.label = "Textures"
        frame_001.name = "Frame.001"
        frame_001.label_size = 20
        frame_001.shrink = True

        #node Principled BSDF
        principled_bsdf = _4k_wet_road_02.nodes.new("ShaderNodeBsdfPrincipled")
        principled_bsdf.name = "Principled BSDF"
        principled_bsdf.distribution = 'MULTI_GGX'
        principled_bsdf.subsurface_method = 'RANDOM_WALK'
        #IOR
        principled_bsdf.inputs[3].default_value = 1.4500000476837158
        #Alpha
        principled_bsdf.inputs[4].default_value = 1.0
        #Diffuse Roughness
        principled_bsdf.inputs[7].default_value = 0.0
        #Subsurface Weight
        principled_bsdf.inputs[8].default_value = 0.0
        #Subsurface Radius
        principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
        #Subsurface Scale
        principled_bsdf.inputs[10].default_value = 0.05000000074505806
        #Subsurface Anisotropy
        principled_bsdf.inputs[12].default_value = 0.0
        #Specular IOR Level
        principled_bsdf.inputs[13].default_value = 0.5
        #Specular Tint
        principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
        #Anisotropic
        principled_bsdf.inputs[15].default_value = 0.0
        #Anisotropic Rotation
        principled_bsdf.inputs[16].default_value = 0.0
        #Tangent
        principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
        #Transmission Weight
        principled_bsdf.inputs[18].default_value = 0.0
        #Coat Weight
        principled_bsdf.inputs[19].default_value = 0.0
        #Coat Roughness
        principled_bsdf.inputs[20].default_value = 0.029999999329447746
        #Coat IOR
        principled_bsdf.inputs[21].default_value = 1.5
        #Coat Tint
        principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
        #Coat Normal
        principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
        #Sheen Weight
        principled_bsdf.inputs[24].default_value = 0.0
        #Sheen Roughness
        principled_bsdf.inputs[25].default_value = 0.5
        #Sheen Tint
        principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
        #Emission Color
        principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
        #Emission Strength
        principled_bsdf.inputs[28].default_value = 0.0
        #Thin Film Thickness
        principled_bsdf.inputs[29].default_value = 0.0
        #Thin Film IOR
        principled_bsdf.inputs[30].default_value = 1.3300000429153442

        #node Image Texture
        image_texture = _4k_wet_road_02.nodes.new("ShaderNodeTexImage")
        image_texture.label = "Displacement"
        image_texture.name = "Image Texture"
        image_texture.extension = 'REPEAT'
        image_texture.image_user.frame_current = 0
        image_texture.image_user.frame_duration = 100
        image_texture.image_user.frame_offset = 0
        image_texture.image_user.frame_start = 1
        image_texture.image_user.tile = 0
        image_texture.image_user.use_auto_refresh = False
        image_texture.image_user.use_cyclic = False
        image_texture.interpolation = 'Linear'
        image_texture.projection = 'FLAT'
        image_texture.projection_blend = 0.0
        image_texture.image = bpy.data.images.load(tex_path+disp)  

        #node Displacement
        displacement = _4k_wet_road_02.nodes.new("ShaderNodeDisplacement")
        displacement.name = "Displacement"
        displacement.space = 'OBJECT'
        #Midlevel
        displacement.inputs[1].default_value = 0.5
        #Scale
        displacement.inputs[2].default_value = 0.7999999523162842
        #Normal
        displacement.inputs[3].default_value = (0.0, 0.0, 0.0)

        #node Image Texture.001
        image_texture_001 = _4k_wet_road_02.nodes.new("ShaderNodeTexImage")
        image_texture_001.label = "Base Color"
        image_texture_001.name = "Image Texture.001"
        image_texture_001.extension = 'REPEAT'
        image_texture_001.image_user.frame_current = 0
        image_texture_001.image_user.frame_duration = 100
        image_texture_001.image_user.frame_offset = 0
        image_texture_001.image_user.frame_start = 1
        image_texture_001.image_user.tile = 0
        image_texture_001.image_user.use_auto_refresh = False
        image_texture_001.image_user.use_cyclic = False
        image_texture_001.interpolation = 'Linear'
        image_texture_001.projection = 'FLAT'
        image_texture_001.projection_blend = 0.0
        image_texture_001.image = bpy.data.images.load(tex_path+albedo)  

        #node Image Texture.002
        image_texture_002 = _4k_wet_road_02.nodes.new("ShaderNodeTexImage")
        image_texture_002.label = "Metallic"
        image_texture_002.name = "Image Texture.002"
        image_texture_002.extension = 'REPEAT'
        image_texture_002.image_user.frame_current = 0
        image_texture_002.image_user.frame_duration = 100
        image_texture_002.image_user.frame_offset = 0
        image_texture_002.image_user.frame_start = 1
        image_texture_002.image_user.tile = 0
        image_texture_002.image_user.use_auto_refresh = False
        image_texture_002.image_user.use_cyclic = False
        image_texture_002.interpolation = 'Linear'
        image_texture_002.projection = 'FLAT'
        image_texture_002.projection_blend = 0.0
        image_texture_002.image = bpy.data.images.load(tex_path+metal)  

        #node Image Texture.003
        image_texture_003 = _4k_wet_road_02.nodes.new("ShaderNodeTexImage")
        image_texture_003.label = "Roughness"
        image_texture_003.name = "Image Texture.003"
        image_texture_003.extension = 'REPEAT'
        image_texture_003.image_user.frame_current = 0
        image_texture_003.image_user.frame_duration = 100
        image_texture_003.image_user.frame_offset = 0
        image_texture_003.image_user.frame_start = 1
        image_texture_003.image_user.tile = 0
        image_texture_003.image_user.use_auto_refresh = False
        image_texture_003.image_user.use_cyclic = False
        image_texture_003.interpolation = 'Linear'
        image_texture_003.projection = 'FLAT'
        image_texture_003.projection_blend = 0.0
        image_texture_003.image = bpy.data.images.load(tex_path+rough)  

        #node Image Texture.004
        image_texture_004 = _4k_wet_road_02.nodes.new("ShaderNodeTexImage")
        image_texture_004.label = "Normal"
        image_texture_004.name = "Image Texture.004"
        image_texture_004.extension = 'REPEAT'
        image_texture_004.image_user.frame_current = 0
        image_texture_004.image_user.frame_duration = 100
        image_texture_004.image_user.frame_offset = 0
        image_texture_004.image_user.frame_start = 1
        image_texture_004.image_user.tile = 0
        image_texture_004.image_user.use_auto_refresh = False
        image_texture_004.image_user.use_cyclic = False
        image_texture_004.interpolation = 'Linear'
        image_texture_004.projection = 'FLAT'
        image_texture_004.projection_blend = 0.0
        image_texture_004.image = bpy.data.images.load(tex_path+normal)  

        #node Normal Map
        normal_map = _4k_wet_road_02.nodes.new("ShaderNodeNormalMap")
        normal_map.name = "Normal Map"
        normal_map.space = 'TANGENT'
        normal_map.uv_map = ""
        #Strength
        normal_map.inputs[0].default_value = 1.0

        #node Mapping
        mapping = _4k_wet_road_02.nodes.new("ShaderNodeMapping")
        mapping.name = "Mapping"
        mapping.vector_type = 'POINT'
        #Location
        mapping.inputs[1].default_value = (1.2999999523162842, -0.05000000074505806, 0.0)
        #Rotation
        mapping.inputs[2].default_value = (0.0, 0.0, 1.5707999467849731)
        #Scale
        mapping.inputs[3].default_value = (-6.575699806213379, 1.5499999523162842, 1.0)

        #node Reroute
        reroute = _4k_wet_road_02.nodes.new("NodeReroute")
        reroute.name = "Reroute"
        reroute.socket_idname = "NodeSocketVector"
        #node Texture Coordinate
        texture_coordinate = _4k_wet_road_02.nodes.new("ShaderNodeTexCoord")
        texture_coordinate.name = "Texture Coordinate"
        texture_coordinate.from_instancer = False

        #node Mix
        mix = _4k_wet_road_02.nodes.new("ShaderNodeMix")
        mix.name = "Mix"
        mix.hide = True
        mix.blend_type = 'MIX'
        mix.clamp_factor = True
        mix.clamp_result = False
        mix.data_type = 'RGBA'
        mix.factor_mode = 'UNIFORM'
        #Factor_Float
        mix.inputs[0].default_value = 0.5
        #B_Color
        mix.inputs[7].default_value = (0.5, 0.5, 0.5, 1.0)

        #node Mix Shader
        mix_shader = _4k_wet_road_02.nodes.new("ShaderNodeMixShader")
        mix_shader.name = "Mix Shader"

        #node Material Output
        material_output = _4k_wet_road_02.nodes.new("ShaderNodeOutputMaterial")
        material_output.name = "Material Output"
        material_output.is_active_output = True
        material_output.target = 'ALL'
        #Thickness
        material_output.inputs[3].default_value = 0.0

        #node Ambient Occlusion
        ambient_occlusion = _4k_wet_road_02.nodes.new("ShaderNodeAmbientOcclusion")
        ambient_occlusion.name = "Ambient Occlusion"
        ambient_occlusion.inside = False
        ambient_occlusion.only_local = False
        ambient_occlusion.samples = 16
        #Distance
        ambient_occlusion.inputs[1].default_value = 1.0
        #Normal
        ambient_occlusion.inputs[2].default_value = (0.0, 0.0, 0.0)
        

        #node Image Texture.005
        image_texture_005 = _4k_wet_road_02.nodes.new("ShaderNodeTexImage")
        image_texture_005.label = "Ambient Occlusion"
        image_texture_005.name = "Image Texture.005"
        image_texture_005.extension = 'REPEAT'
        image_texture_005.image_user.frame_current = 0
        image_texture_005.image_user.frame_duration = 100
        image_texture_005.image_user.frame_offset = 0
        image_texture_005.image_user.frame_start = 1
        image_texture_005.image_user.tile = 0
        image_texture_005.image_user.use_auto_refresh = False
        image_texture_005.image_user.use_cyclic = False
        image_texture_005.interpolation = 'Linear'
        image_texture_005.projection = 'FLAT'
        image_texture_005.projection_blend = 0.0
        image_texture_005.image = bpy.data.images.load(tex_path+ao)  

        #Set parents
        image_texture.parent = frame_001
        image_texture_001.parent = frame_001
        image_texture_002.parent = frame_001
        image_texture_003.parent = frame_001
        image_texture_004.parent = frame_001
        mapping.parent = frame
        reroute.parent = frame_001
        texture_coordinate.parent = frame
        image_texture_005.parent = frame_001

        #Set locations
        frame.location = (0.0, 0.0)
        frame_001.location = (0.0, 0.0)
        principled_bsdf.location = (10.0, 300.0)
        image_texture.location = (-540.0, -900.0)
        displacement.location = (212.29421997070312, -554.315185546875)
        image_texture_001.location = (-540.0, 220.0)
        image_texture_002.location = (-540.0, -60.0)
        image_texture_003.location = (-540.0, -340.0)
        image_texture_004.location = (-540.0, -620.0)
        normal_map.location = (-240.0, -620.0)
        mapping.location = (-1040.0, 300.0)
        reroute.location = (-590.0, -291.4285888671875)
        texture_coordinate.location = (-1240.0, 300.0)
        mix.location = (295.0816345214844, 500.0469970703125)
        mix_shader.location = (440.0, 300.0)
        material_output.location = (694.6681518554688, 300.0)
        ambient_occlusion.location = (15.081624031066895, 550.0469970703125)
        image_texture_005.location = (-540.0, 500.0)

        #Set dimensions
        frame.width, frame.height = 400.0, 421.0
        frame_001.width, frame_001.height = 358.0, 1741.0
        principled_bsdf.width, principled_bsdf.height = 240.0, 100.0
        image_texture.width, image_texture.height = 240.0, 100.0
        displacement.width, displacement.height = 140.0, 100.0
        image_texture_001.width, image_texture_001.height = 240.0, 100.0
        image_texture_002.width, image_texture_002.height = 240.0, 100.0
        image_texture_003.width, image_texture_003.height = 240.0, 100.0
        image_texture_004.width, image_texture_004.height = 240.0, 100.0
        normal_map.width, normal_map.height = 150.0, 100.0
        mapping.width, mapping.height = 140.0, 100.0
        reroute.width, reroute.height = 16.0, 100.0
        texture_coordinate.width, texture_coordinate.height = 140.0, 100.0
        mix.width, mix.height = 140.0, 100.0
        mix_shader.width, mix_shader.height = 140.0, 100.0
        material_output.width, material_output.height = 140.0, 100.0
        ambient_occlusion.width, ambient_occlusion.height = 140.0, 100.0
        image_texture_005.width, image_texture_005.height = 240.0, 100.0

        #initialize _4k_wet_road_02 links
        #image_texture.Color -> displacement.Height
        _4k_wet_road_02.links.new(image_texture.outputs[0], displacement.inputs[0])
        #displacement.Displacement -> material_output.Displacement
        _4k_wet_road_02.links.new(displacement.outputs[0], material_output.inputs[2])
        #image_texture_001.Color -> principled_bsdf.Base Color
        _4k_wet_road_02.links.new(image_texture_001.outputs[0], principled_bsdf.inputs[0])
        #image_texture_002.Color -> principled_bsdf.Metallic
        _4k_wet_road_02.links.new(image_texture_002.outputs[0], principled_bsdf.inputs[1])
        #image_texture_003.Color -> principled_bsdf.Roughness
        _4k_wet_road_02.links.new(image_texture_003.outputs[0], principled_bsdf.inputs[2])
        #image_texture_004.Color -> normal_map.Color
        _4k_wet_road_02.links.new(image_texture_004.outputs[0], normal_map.inputs[1])
        #normal_map.Normal -> principled_bsdf.Normal
        _4k_wet_road_02.links.new(normal_map.outputs[0], principled_bsdf.inputs[5])
        #reroute.Output -> image_texture_005.Vector
        _4k_wet_road_02.links.new(reroute.outputs[0], image_texture_005.inputs[0])
        #reroute.Output -> image_texture_001.Vector
        _4k_wet_road_02.links.new(reroute.outputs[0], image_texture_001.inputs[0])
        #reroute.Output -> image_texture_002.Vector
        _4k_wet_road_02.links.new(reroute.outputs[0], image_texture_002.inputs[0])
        #reroute.Output -> image_texture_003.Vector
        _4k_wet_road_02.links.new(reroute.outputs[0], image_texture_003.inputs[0])
        #reroute.Output -> image_texture_004.Vector
        _4k_wet_road_02.links.new(reroute.outputs[0], image_texture_004.inputs[0])
        #reroute.Output -> image_texture.Vector
        _4k_wet_road_02.links.new(reroute.outputs[0], image_texture.inputs[0])
        #mapping.Vector -> reroute.Input
        _4k_wet_road_02.links.new(mapping.outputs[0], reroute.inputs[0])
        #texture_coordinate.UV -> mapping.Vector
        _4k_wet_road_02.links.new(texture_coordinate.outputs[2], mapping.inputs[0])
        #ambient_occlusion.Color -> mix.A
        _4k_wet_road_02.links.new(ambient_occlusion.outputs[0], mix.inputs[6])
        #mix_shader.Shader -> material_output.Surface
        _4k_wet_road_02.links.new(mix_shader.outputs[0], material_output.inputs[0])
        #ambient_occlusion.Color -> mix_shader.Fac
        _4k_wet_road_02.links.new(ambient_occlusion.outputs[0], mix_shader.inputs[0])
        #principled_bsdf.BSDF -> mix_shader.Shader
        _4k_wet_road_02.links.new(principled_bsdf.outputs[0], mix_shader.inputs[2])
        #image_texture_005.Color -> ambient_occlusion.Color
        _4k_wet_road_02.links.new(image_texture_005.outputs[0], ambient_occlusion.inputs[0])
        return _4k_wet_road_02

    _4k_wet_road_02 = _4k_wet_road_02_node_group()
    obj.data.materials.append(mat)




def apply_blenderkit_dryRoad(obj,target_directory):
    tex_path=target_directory+r'/textures/Roads/dry_road_textures_2k/'
    albedo = r'Patched road 02_Albedo.jpg'
    ao = r'Patched road 02_AO.jpg'
    disp = r'Patched road 02_Displacement.exr'
    metal = r'Patched road 02_Metalness.jpg'
    normal  = r'Patched road 02_Normal.jpg'
    rough = r'Patched road 02_Roughness.jpg'



    mat = bpy.data.materials.new(name = "Patched road 02")
    mat.use_nodes = True
    #initialize Patched road 02 node group
    def patched_road_02_node_group():

        patched_road_02 = mat.node_tree
        #start with a clean node tree
        for node in patched_road_02.nodes:
            patched_road_02.nodes.remove(node)
        patched_road_02.color_tag = 'NONE'
        patched_road_02.description = ""
        patched_road_02.default_group_node_width = 140
        

        #patched_road_02 interface

        #initialize patched_road_02 nodes
        #node Frame
        frame = patched_road_02.nodes.new("NodeFrame")
        frame.label = "Mapping"
        frame.name = "Frame"
        frame.label_size = 20
        frame.shrink = True

        #node Frame.001
        frame_001 = patched_road_02.nodes.new("NodeFrame")
        frame_001.label = "Textures"
        frame_001.name = "Frame.001"
        frame_001.label_size = 20
        frame_001.shrink = True

        #node Material Output
        material_output = patched_road_02.nodes.new("ShaderNodeOutputMaterial")
        material_output.name = "Material Output"
        material_output.is_active_output = True
        material_output.target = 'ALL'
        #Thickness
        material_output.inputs[3].default_value = 0.0

        #node Mix Shader
        mix_shader = patched_road_02.nodes.new("ShaderNodeMixShader")
        mix_shader.name = "Mix Shader"

        #node Ambient Occlusion
        ambient_occlusion = patched_road_02.nodes.new("ShaderNodeAmbientOcclusion")
        ambient_occlusion.name = "Ambient Occlusion"
        ambient_occlusion.inside = False
        ambient_occlusion.only_local = False
        ambient_occlusion.samples = 16
        #Distance
        ambient_occlusion.inputs[1].default_value = 1.0
        #Normal
        ambient_occlusion.inputs[2].default_value = (0.0, 0.0, 0.0)

        #node Mapping
        mapping = patched_road_02.nodes.new("ShaderNodeMapping")
        mapping.name = "Mapping"
        mapping.vector_type = 'POINT'
        #Location
        mapping.inputs[1].default_value = (0.0, -0.6999999284744263, 0.0)
        #Rotation
        mapping.inputs[2].default_value = (0.0, 0.0, 1.5707963705062866)
        #Scale
        mapping.inputs[3].default_value = (0.30000001192092896, 0.10000000149011612, 1.0)

        #node Texture Coordinate
        texture_coordinate = patched_road_02.nodes.new("ShaderNodeTexCoord")
        texture_coordinate.name = "Texture Coordinate"
        texture_coordinate.from_instancer = False

        #node Image Texture
        image_texture = patched_road_02.nodes.new("ShaderNodeTexImage")
        image_texture.label = "Displacement"
        image_texture.name = "Image Texture"
        image_texture.extension = 'REPEAT'
        image_texture.image_user.frame_current = 0
        image_texture.image_user.frame_duration = 100
        image_texture.image_user.frame_offset = 0
        image_texture.image_user.frame_start = 1
        image_texture.image_user.tile = 0
        image_texture.image_user.use_auto_refresh = False
        image_texture.image_user.use_cyclic = False
        image_texture.interpolation = 'Linear'
        image_texture.projection = 'FLAT'
        image_texture.projection_blend = 0.0
        image_texture.image = bpy.data.images.load(tex_path+disp)  

        #node Image Texture.001
        image_texture_001 = patched_road_02.nodes.new("ShaderNodeTexImage")
        image_texture_001.label = "Base Color"
        image_texture_001.name = "Image Texture.001"
        image_texture_001.extension = 'REPEAT'
        image_texture_001.image_user.frame_current = 0
        image_texture_001.image_user.frame_duration = 100
        image_texture_001.image_user.frame_offset = 0
        image_texture_001.image_user.frame_start = 1
        image_texture_001.image_user.tile = 0
        image_texture_001.image_user.use_auto_refresh = False
        image_texture_001.image_user.use_cyclic = False
        image_texture_001.interpolation = 'Linear'
        image_texture_001.projection = 'FLAT'
        image_texture_001.projection_blend = 0.0
        image_texture_001.image = bpy.data.images.load(tex_path+albedo)  

        #node Image Texture.002
        image_texture_002 = patched_road_02.nodes.new("ShaderNodeTexImage")
        image_texture_002.label = "Metallic"
        image_texture_002.name = "Image Texture.002"
        image_texture_002.extension = 'REPEAT'
        image_texture_002.image_user.frame_current = 0
        image_texture_002.image_user.frame_duration = 100
        image_texture_002.image_user.frame_offset = 0
        image_texture_002.image_user.frame_start = 1
        image_texture_002.image_user.tile = 0
        image_texture_002.image_user.use_auto_refresh = False
        image_texture_002.image_user.use_cyclic = False
        image_texture_002.interpolation = 'Linear'
        image_texture_002.projection = 'FLAT'
        image_texture_002.projection_blend = 0.0
        image_texture_002.image = bpy.data.images.load(tex_path+metal)  

        #node Image Texture.003
        image_texture_003 = patched_road_02.nodes.new("ShaderNodeTexImage")
        image_texture_003.label = "Roughness"
        image_texture_003.name = "Image Texture.003"
        image_texture_003.extension = 'REPEAT'
        image_texture_003.image_user.frame_current = 0
        image_texture_003.image_user.frame_duration = 100
        image_texture_003.image_user.frame_offset = 0
        image_texture_003.image_user.frame_start = 1
        image_texture_003.image_user.tile = 0
        image_texture_003.image_user.use_auto_refresh = False
        image_texture_003.image_user.use_cyclic = False
        image_texture_003.interpolation = 'Linear'
        image_texture_003.projection = 'FLAT'
        image_texture_003.projection_blend = 0.0
        image_texture_003.image = bpy.data.images.load(tex_path+rough)  
        #node Image Texture.004
        image_texture_004 = patched_road_02.nodes.new("ShaderNodeTexImage")
        image_texture_004.label = "Normal"
        image_texture_004.name = "Image Texture.004"
        image_texture_004.extension = 'REPEAT'
        image_texture_004.image_user.frame_current = 0
        image_texture_004.image_user.frame_duration = 100
        image_texture_004.image_user.frame_offset = 0
        image_texture_004.image_user.frame_start = 1
        image_texture_004.image_user.tile = 0
        image_texture_004.image_user.use_auto_refresh = False
        image_texture_004.image_user.use_cyclic = False
        image_texture_004.interpolation = 'Linear'
        image_texture_004.projection = 'FLAT'
        image_texture_004.projection_blend = 0.0
        image_texture_004.image = bpy.data.images.load(tex_path+normal)  

        #node Reroute
        reroute = patched_road_02.nodes.new("NodeReroute")
        reroute.name = "Reroute"
        reroute.socket_idname = "NodeSocketVector"
        #node Image Texture.005
        image_texture_005 = patched_road_02.nodes.new("ShaderNodeTexImage")
        image_texture_005.label = "Ambient Occlusion"
        image_texture_005.name = "Image Texture.005"
        image_texture_005.extension = 'REPEAT'
        image_texture_005.image_user.frame_current = 0
        image_texture_005.image_user.frame_duration = 100
        image_texture_005.image_user.frame_offset = 0
        image_texture_005.image_user.frame_start = 1
        image_texture_005.image_user.tile = 0
        image_texture_005.image_user.use_auto_refresh = False
        image_texture_005.image_user.use_cyclic = False
        image_texture_005.interpolation = 'Linear'
        image_texture_005.projection = 'FLAT'
        image_texture_005.projection_blend = 0.0
        image_texture_005.image = bpy.data.images.load(tex_path+ao)  

        #node Principled BSDF
        principled_bsdf = patched_road_02.nodes.new("ShaderNodeBsdfPrincipled")
        principled_bsdf.name = "Principled BSDF"
        principled_bsdf.distribution = 'MULTI_GGX'
        principled_bsdf.subsurface_method = 'RANDOM_WALK'
        #IOR
        principled_bsdf.inputs[3].default_value = 1.4500000476837158
        #Alpha
        principled_bsdf.inputs[4].default_value = 1.0
        #Diffuse Roughness
        principled_bsdf.inputs[7].default_value = 0.0
        #Subsurface Weight
        principled_bsdf.inputs[8].default_value = 0.0
        #Subsurface Radius
        principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
        #Subsurface Scale
        principled_bsdf.inputs[10].default_value = 0.05000000074505806
        #Subsurface Anisotropy
        principled_bsdf.inputs[12].default_value = 0.0
        #Specular IOR Level
        principled_bsdf.inputs[13].default_value = 0.5
        #Specular Tint
        principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
        #Anisotropic
        principled_bsdf.inputs[15].default_value = 0.0
        #Anisotropic Rotation
        principled_bsdf.inputs[16].default_value = 0.0
        #Tangent
        principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
        #Transmission Weight
        principled_bsdf.inputs[18].default_value = 0.0
        #Coat Weight
        principled_bsdf.inputs[19].default_value = 0.0
        #Coat Roughness
        principled_bsdf.inputs[20].default_value = 0.029999999329447746
        #Coat IOR
        principled_bsdf.inputs[21].default_value = 1.5
        #Coat Tint
        principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
        #Coat Normal
        principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
        #Sheen Weight
        principled_bsdf.inputs[24].default_value = 0.0
        #Sheen Roughness
        principled_bsdf.inputs[25].default_value = 0.5
        #Sheen Tint
        principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
        #Emission Color
        principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
        #Emission Strength
        principled_bsdf.inputs[28].default_value = 0.0
        #Thin Film Thickness
        principled_bsdf.inputs[29].default_value = 0.0
        #Thin Film IOR
        principled_bsdf.inputs[30].default_value = 1.3300000429153442

        #node Color Ramp
        color_ramp = patched_road_02.nodes.new("ShaderNodeValToRGB")
        color_ramp.name = "Color Ramp"
        color_ramp.color_ramp.color_mode = 'RGB'
        color_ramp.color_ramp.hue_interpolation = 'NEAR'
        color_ramp.color_ramp.interpolation = 'LINEAR'

        #initialize color ramp elements
        color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[0])
        color_ramp_cre_0 = color_ramp.color_ramp.elements[0]
        color_ramp_cre_0.position = 0.0
        color_ramp_cre_0.alpha = 1.0
        color_ramp_cre_0.color = (0.0, 0.0, 0.0, 1.0)

        color_ramp_cre_1 = color_ramp.color_ramp.elements.new(0.8942598104476929)
        color_ramp_cre_1.alpha = 1.0
        color_ramp_cre_1.color = (1.0, 1.0, 1.0, 1.0)


        #node Displacement
        displacement = patched_road_02.nodes.new("ShaderNodeDisplacement")
        displacement.name = "Displacement"
        displacement.space = 'OBJECT'
        #Midlevel
        displacement.inputs[1].default_value = 0.5
        #Scale
        displacement.inputs[2].default_value = 0.20000000298023224
        #Normal
        displacement.inputs[3].default_value = (0.0, 0.0, 0.0)

        #node Normal Map
        normal_map = patched_road_02.nodes.new("ShaderNodeNormalMap")
        normal_map.name = "Normal Map"
        normal_map.space = 'TANGENT'
        normal_map.uv_map = ""
        #Strength
        normal_map.inputs[0].default_value = 1.0

        #Set parents
        mapping.parent = frame
        texture_coordinate.parent = frame
        image_texture.parent = frame_001
        image_texture_001.parent = frame_001
        image_texture_002.parent = frame_001
        image_texture_003.parent = frame_001
        image_texture_004.parent = frame_001
        reroute.parent = frame_001
        image_texture_005.parent = frame_001

        #Set locations
        frame.location = (0.0, 0.0)
        frame_001.location = (0.0, 0.0)
        material_output.location = (817.8197021484375, 306.3113708496094)
        mix_shader.location = (530.0, 300.0)
        ambient_occlusion.location = (48.98478317260742, 558.7246704101562)
        mapping.location = (-1040.0, 300.0)
        texture_coordinate.location = (-1240.0, 300.0)
        image_texture.location = (-540.0, -900.0)
        image_texture_001.location = (-540.0, 220.0)
        image_texture_002.location = (-540.0, -60.0)
        image_texture_003.location = (-540.0, -340.0)
        image_texture_004.location = (-540.0, -620.0)
        reroute.location = (-590.0, -291.4285888671875)
        image_texture_005.location = (-540.0, 500.0)
        principled_bsdf.location = (99.99999237060547, 300.0)
        color_ramp.location = (-220.00001525878906, -103.8960952758789)
        displacement.location = (110.0, -400.0)
        normal_map.location = (-222.4766082763672, -455.0442810058594)

        #Set dimensions
        frame.width, frame.height = 400.0, 421.0
        frame_001.width, frame_001.height = 358.0, 1741.0
        material_output.width, material_output.height = 140.0, 100.0
        mix_shader.width, mix_shader.height = 140.0, 100.0
        ambient_occlusion.width, ambient_occlusion.height = 140.0, 100.0
        mapping.width, mapping.height = 140.0, 100.0
        texture_coordinate.width, texture_coordinate.height = 140.0, 100.0
        image_texture.width, image_texture.height = 240.0, 100.0
        image_texture_001.width, image_texture_001.height = 240.0, 100.0
        image_texture_002.width, image_texture_002.height = 240.0, 100.0
        image_texture_003.width, image_texture_003.height = 240.0, 100.0
        image_texture_004.width, image_texture_004.height = 240.0, 100.0
        reroute.width, reroute.height = 16.0, 100.0
        image_texture_005.width, image_texture_005.height = 240.0, 100.0
        principled_bsdf.width, principled_bsdf.height = 240.0, 100.0
        color_ramp.width, color_ramp.height = 240.0, 100.0
        displacement.width, displacement.height = 140.0, 100.0
        normal_map.width, normal_map.height = 150.0, 100.0

        #initialize patched_road_02 links
        #mix_shader.Shader -> material_output.Surface
        patched_road_02.links.new(mix_shader.outputs[0], material_output.inputs[0])
        #ambient_occlusion.Color -> mix_shader.Fac
        patched_road_02.links.new(ambient_occlusion.outputs[0], mix_shader.inputs[0])
        #principled_bsdf.BSDF -> mix_shader.Shader
        patched_road_02.links.new(principled_bsdf.outputs[0], mix_shader.inputs[2])
        #image_texture.Color -> displacement.Height
        patched_road_02.links.new(image_texture.outputs[0], displacement.inputs[0])
        #displacement.Displacement -> material_output.Displacement
        patched_road_02.links.new(displacement.outputs[0], material_output.inputs[2])
        #image_texture_001.Color -> principled_bsdf.Base Color
        patched_road_02.links.new(image_texture_001.outputs[0], principled_bsdf.inputs[0])
        #image_texture_002.Color -> principled_bsdf.Metallic
        patched_road_02.links.new(image_texture_002.outputs[0], principled_bsdf.inputs[1])
        #color_ramp.Color -> principled_bsdf.Roughness
        patched_road_02.links.new(color_ramp.outputs[0], principled_bsdf.inputs[2])
        #image_texture_004.Color -> normal_map.Color
        patched_road_02.links.new(image_texture_004.outputs[0], normal_map.inputs[1])
        #normal_map.Normal -> principled_bsdf.Normal
        patched_road_02.links.new(normal_map.outputs[0], principled_bsdf.inputs[5])
        #reroute.Output -> image_texture_005.Vector
        patched_road_02.links.new(reroute.outputs[0], image_texture_005.inputs[0])
        #reroute.Output -> image_texture_001.Vector
        patched_road_02.links.new(reroute.outputs[0], image_texture_001.inputs[0])
        #reroute.Output -> image_texture_002.Vector
        patched_road_02.links.new(reroute.outputs[0], image_texture_002.inputs[0])
        #reroute.Output -> image_texture_003.Vector
        patched_road_02.links.new(reroute.outputs[0], image_texture_003.inputs[0])
        #reroute.Output -> image_texture_004.Vector
        patched_road_02.links.new(reroute.outputs[0], image_texture_004.inputs[0])
        #reroute.Output -> image_texture.Vector
        patched_road_02.links.new(reroute.outputs[0], image_texture.inputs[0])
        #mapping.Vector -> reroute.Input
        patched_road_02.links.new(mapping.outputs[0], reroute.inputs[0])
        #texture_coordinate.UV -> mapping.Vector
        patched_road_02.links.new(texture_coordinate.outputs[2], mapping.inputs[0])
        #image_texture_005.Color -> ambient_occlusion.Color
        patched_road_02.links.new(image_texture_005.outputs[0], ambient_occlusion.inputs[0])
        #image_texture_003.Color -> color_ramp.Fac
        patched_road_02.links.new(image_texture_003.outputs[0], color_ramp.inputs[0])
        return patched_road_02

    patched_road_02 = patched_road_02_node_group()
    obj.data.materials.append(mat)








def apply_blenderkit_sign_jpg(obj,target_directory,base_color_path = None,scratches_on =True, rust_minor_on = True, rust_major_on = False,rivets_on=True):
    tex_path=target_directory+r'/textures/Signs/'
    base_color = base_color_path
    rust_major = r'/rust.png'
    rust_minor = r'/rust.jpg'
    scratches = r'/scratches.jpg'
    rivets = r'/metal_rivets_textures_2k/metal-23_normal.jpg'
    rivets_rough = r'/metal_rivets_textures_2k/metal-23_roughness.jpg'


   

    mat = bpy.data.materials.new(name = "SignMaterial")
    mat.use_nodes = True
    #initialize SignMaterial node group
    def signmaterial_node_group():

        signmaterial = mat.node_tree
        #start with a clean node tree
        for node in signmaterial.nodes:
            signmaterial.nodes.remove(node)
        signmaterial.color_tag = 'NONE'
        signmaterial.description = ""
        signmaterial.default_group_node_width = 140
        

        #signmaterial interface

        #initialize signmaterial nodes
        #node Principled BSDF
        principled_bsdf = signmaterial.nodes.new("ShaderNodeBsdfPrincipled")
        principled_bsdf.name = "Principled BSDF"
        principled_bsdf.distribution = 'MULTI_GGX'
        principled_bsdf.subsurface_method = 'RANDOM_WALK'
        #Metallic
        principled_bsdf.inputs[1].default_value = 0.7363636493682861
        #Roughness
        principled_bsdf.inputs[2].default_value = 1.0
        #IOR
        principled_bsdf.inputs[3].default_value = 1.5
        #Alpha
        principled_bsdf.inputs[4].default_value = 1.0
        #Subsurface Weight
        principled_bsdf.inputs[8].default_value = 0.0
        #Subsurface Radius
        principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
        #Subsurface Scale
        principled_bsdf.inputs[10].default_value = 0.05000000074505806
        #Subsurface Anisotropy
        principled_bsdf.inputs[12].default_value = 0.0
        #Specular IOR Level
        principled_bsdf.inputs[13].default_value = 0.5
        #Specular Tint
        principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
        #Anisotropic
        principled_bsdf.inputs[15].default_value = 0.0
        #Anisotropic Rotation
        principled_bsdf.inputs[16].default_value = 0.0
        #Tangent
        principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
        #Transmission Weight
        principled_bsdf.inputs[18].default_value = 0.0
        #Coat Weight
        principled_bsdf.inputs[19].default_value = 0.0
        #Coat Roughness
        principled_bsdf.inputs[20].default_value = 0.029999999329447746
        #Coat IOR
        principled_bsdf.inputs[21].default_value = 1.5
        #Coat Tint
        principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
        #Coat Normal
        principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
        #Sheen Weight
        principled_bsdf.inputs[24].default_value = 0.0
        #Sheen Roughness
        principled_bsdf.inputs[25].default_value = 0.5
        #Sheen Tint
        principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
        #Emission Color
        principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
        #Emission Strength
        principled_bsdf.inputs[28].default_value = 0.0
        #Thin Film Thickness
        principled_bsdf.inputs[29].default_value = 0.0
        #Thin Film IOR
        principled_bsdf.inputs[30].default_value = 1.3300000429153442

        #node Image Texture
        image_texture = signmaterial.nodes.new("ShaderNodeTexImage")
        image_texture.name = "Image Texture"
        image_texture.extension = 'REPEAT'
        image_texture.image_user.frame_current = 0
        image_texture.image_user.frame_duration = 100
        image_texture.image_user.frame_offset = 0
        image_texture.image_user.frame_start = 1
        image_texture.image_user.tile = 0
        image_texture.image_user.use_auto_refresh = False
        image_texture.image_user.use_cyclic = False
        image_texture.interpolation = 'Linear'
        image_texture.projection = 'FLAT'
        image_texture.projection_blend = 0.0
        image_texture.image = bpy.data.images.load(tex_path+base_color) 

        #node Material Output
        material_output = signmaterial.nodes.new("ShaderNodeOutputMaterial")
        material_output.name = "Material Output"
        material_output.is_active_output = True
        material_output.target = 'ALL'
        #Displacement
        material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
        #Thickness
        material_output.inputs[3].default_value = 0.0

        #node Image Texture.001
        image_texture_001 = signmaterial.nodes.new("ShaderNodeTexImage")
        image_texture_001.label = "Scratches"
        image_texture_001.name = "Image Texture.001"
        image_texture_001.extension = 'REPEAT'
        image_texture_001.image_user.frame_current = 1
        image_texture_001.image_user.frame_duration = 1
        image_texture_001.image_user.frame_offset = -1
        image_texture_001.image_user.frame_start = 1
        image_texture_001.image_user.tile = 0
        image_texture_001.image_user.use_auto_refresh = False
        image_texture_001.image_user.use_cyclic = False
        image_texture_001.interpolation = 'Linear'
        image_texture_001.projection = 'FLAT'
        image_texture_001.projection_blend = 0.0
        image_texture_001.image = bpy.data.images.load(tex_path+scratches)  

        #node Mix
        mix = signmaterial.nodes.new("ShaderNodeMix")
        mix.name = "Mix"
        mix.blend_type = 'MIX'
        mix.clamp_factor = True
        mix.clamp_result = False
        mix.data_type = 'RGBA'
        mix.factor_mode = 'UNIFORM'
        #Factor_Float
        #### THIS IS BASE IMAGE + SCRATCHES 
        if scratches_on == True:
            mix.inputs[0].default_value = 0.24166667461395264
        else:
            mix.inputs[0].default_value = 0.0
        #node Mix.001
        mix_001 = signmaterial.nodes.new("ShaderNodeMix")
        mix_001.name = "Mix.001"
        mix_001.blend_type = 'MIX'
        mix_001.clamp_factor = True
        mix_001.clamp_result = False
        mix_001.data_type = 'RGBA'
        mix_001.factor_mode = 'UNIFORM'
        #Factor_Float
        #combines output with RUST MINOR
        if rust_minor_on == True:
            mix_001.inputs[0].default_value = 0.32500001788139343
        else:
            mix_001.inputs[0].default_value = 0.0

        #node Image Texture.002
        image_texture_002 = signmaterial.nodes.new("ShaderNodeTexImage")
        image_texture_002.label = "Rust Minor"
        image_texture_002.name = "Image Texture.002"
        image_texture_002.extension = 'REPEAT'
        image_texture_002.image_user.frame_current = 1
        image_texture_002.image_user.frame_duration = 1
        image_texture_002.image_user.frame_offset = -1
        image_texture_002.image_user.frame_start = 1
        image_texture_002.image_user.tile = 0
        image_texture_002.image_user.use_auto_refresh = False
        image_texture_002.image_user.use_cyclic = False
        image_texture_002.interpolation = 'Linear'
        image_texture_002.projection = 'FLAT'
        image_texture_002.projection_blend = 0.0
        image_texture_002.image = bpy.data.images.load(tex_path+rust_minor) 
        #Vector
        image_texture_002.inputs[0].default_value = (0.0, 0.0, 0.0)

        #node Texture Coordinate
        texture_coordinate = signmaterial.nodes.new("ShaderNodeTexCoord")
        texture_coordinate.name = "Texture Coordinate"
        texture_coordinate.from_instancer = False

        #node Mapping
        mapping = signmaterial.nodes.new("ShaderNodeMapping")
        mapping.name = "Mapping"
        mapping.vector_type = 'POINT'
        #Location
        mapping.inputs[1].default_value = (0.9999999403953552, 0.5, 0.0)
        #Rotation
        mapping.inputs[2].default_value = (0.9267697930335999, 0.1745329350233078, 3.1415927410125732)
        #Scale
        mapping.inputs[3].default_value = (1.0, 1.0, 1.0)

        #node Mapping.001
        mapping_001 = signmaterial.nodes.new("ShaderNodeMapping")
        mapping_001.name = "Mapping.001"
        mapping_001.vector_type = 'POINT'
        #Location
        mapping_001.inputs[1].default_value = (0.0, 0.0, 0.0)
        #Rotation
        mapping_001.inputs[2].default_value = (0.0, 0.0, -1.5708)
        #Scale
        mapping_001.inputs[3].default_value = (2, 2, 1.0)

        #node Image Texture.003
        image_texture_003 = signmaterial.nodes.new("ShaderNodeTexImage")
        image_texture_003.label = "Rust Major"
        image_texture_003.name = "Image Texture.003"
        image_texture_003.extension = 'REPEAT'
        image_texture_003.image_user.frame_current = 1
        image_texture_003.image_user.frame_duration = 1
        image_texture_003.image_user.frame_offset = -1
        image_texture_003.image_user.frame_start = 1
        image_texture_003.image_user.tile = 0
        image_texture_003.image_user.use_auto_refresh = False
        image_texture_003.image_user.use_cyclic = False
        image_texture_003.interpolation = 'Linear'
        image_texture_003.projection = 'FLAT'
        image_texture_003.projection_blend = 0.0
        image_texture_003.image = bpy.data.images.load(tex_path+rust_major) 
        #Vector
        image_texture_003.inputs[0].default_value = (0.0, 0.0, 0.0)


        ### THIS NODE CONTROLS MAJOR RUST. COME BACK LATER ### 
        #node Mix.002
        mix_002 = signmaterial.nodes.new("ShaderNodeMix")
        mix_002.name = "Mix.002"
        mix_002.blend_type = 'MIX'
        mix_002.clamp_factor = True
        mix_002.clamp_result = False
        mix_002.data_type = 'RGBA'
        mix_002.factor_mode = 'UNIFORM'
        #A_Color
        mix_002.inputs[6].default_value = (0.5, 0.5, 0.5, 1.0)

        #node Image Texture.004
        image_texture_004 = signmaterial.nodes.new("ShaderNodeTexImage")
        image_texture_004.label = "Rivets Normal"
        image_texture_004.name = "Image Texture.004"
        image_texture_004.extension = 'REPEAT'
        image_texture_004.image_user.frame_current = 1
        image_texture_004.image_user.frame_duration = 1
        image_texture_004.image_user.frame_offset = 22
        image_texture_004.image_user.frame_start = 1
        image_texture_004.image_user.tile = 0
        image_texture_004.image_user.use_auto_refresh = False
        image_texture_004.image_user.use_cyclic = False
        image_texture_004.interpolation = 'Linear'
        image_texture_004.projection = 'FLAT'
        image_texture_004.projection_blend = 0.0
        image_texture_004.image = bpy.data.images.load(tex_path+rivets) 
        #Vector
        image_texture_004.inputs[0].default_value = (0.0, 0.0, 0.0)

        #node Image Texture.005
        image_texture_005 = signmaterial.nodes.new("ShaderNodeTexImage")
        image_texture_005.label = "Rivets Roughness"
        image_texture_005.name = "Image Texture.005"
        image_texture_005.extension = 'REPEAT'
        image_texture_005.image_user.frame_current = 1
        image_texture_005.image_user.frame_duration = 1
        image_texture_005.image_user.frame_offset = 22
        image_texture_005.image_user.frame_start = 1
        image_texture_005.image_user.tile = 0
        image_texture_005.image_user.use_auto_refresh = False
        image_texture_005.image_user.use_cyclic = False
        image_texture_005.interpolation = 'Linear'
        image_texture_005.projection = 'FLAT'
        image_texture_005.projection_blend = 0.0
        image_texture_005.image = bpy.data.images.load(tex_path+rivets_rough) 
        #Vector
        image_texture_005.inputs[0].default_value = (0.0, 0.0, 0.0)


        #Set locations
        principled_bsdf.location = (510.5553283691406, -59.9542236328125)
        image_texture.location = (-658.6177978515625, 66.822265625)
        material_output.location = (808.970458984375, -26.89124870300293)
        image_texture_001.location = (-663.31103515625, -260.9002380371094)
        mix.location = (-373.9364929199219, 18.197063446044922)
        mix_001.location = (-103.21905517578125, 15.489540100097656)
        image_texture_002.location = (-738.0819091796875, -667.8732299804688)
        texture_coordinate.location = (-1274.4552001953125, -27.621980667114258)
        mapping.location = (-1028.459228515625, -457.97308349609375)
        mapping_001.location = (-968.6342163085938, 63.104949951171875)
        image_texture_003.location = (-283.27056884765625, -568.5834350585938)
        mix_002.location = (74.1423568725586, -326.18988037109375)
        image_texture_004.location = (102.3629150390625, -633.4000854492188)
        image_texture_005.location = (419.182861328125, -666.4660034179688)

        #Set dimensions
        principled_bsdf.width, principled_bsdf.height = 240.0, 100.0
        image_texture.width, image_texture.height = 240.0, 100.0
        material_output.width, material_output.height = 140.0, 100.0
        image_texture_001.width, image_texture_001.height = 240.0, 100.0
        mix.width, mix.height = 140.0, 100.0
        mix_001.width, mix_001.height = 140.0, 100.0
        image_texture_002.width, image_texture_002.height = 240.0, 100.0
        texture_coordinate.width, texture_coordinate.height = 140.0, 100.0
        mapping.width, mapping.height = 140.0, 100.0
        mapping_001.width, mapping_001.height = 140.0, 100.0
        image_texture_003.width, image_texture_003.height = 240.0, 100.0
        mix_002.width, mix_002.height = 140.0, 100.0
        image_texture_004.width, image_texture_004.height = 240.0, 100.0
        image_texture_005.width, image_texture_005.height = 240.0, 100.0

        #initialize signmaterial links
        #image_texture.Color -> mix.A
        signmaterial.links.new(image_texture.outputs[0], mix.inputs[2])
        #image_texture.Color -> mix.A
        signmaterial.links.new(image_texture.outputs[0], mix.inputs[6])
        #image_texture_001.Color -> mix.B
        signmaterial.links.new(image_texture_001.outputs[0], mix.inputs[7])
        #mix.Result -> mix_001.A
        signmaterial.links.new(mix.outputs[2], mix_001.inputs[6])
        #image_texture_002.Color -> mix_001.B
        signmaterial.links.new(image_texture_002.outputs[0], mix_001.inputs[7])
        #texture_coordinate.UV -> mapping.Vector
        signmaterial.links.new(texture_coordinate.outputs[2], mapping.inputs[0])
        #mapping.Vector -> image_texture_001.Vector
        signmaterial.links.new(mapping.outputs[0], image_texture_001.inputs[0])
        #texture_coordinate.UV -> mapping_001.Vector
        signmaterial.links.new(texture_coordinate.outputs[2], mapping_001.inputs[0])
        #mapping_001.Vector -> image_texture.Vector
        signmaterial.links.new(mapping_001.outputs[0], image_texture.inputs[0])
        #principled_bsdf.BSDF -> material_output.Surface
        signmaterial.links.new(principled_bsdf.outputs[0], material_output.inputs[0])
        #image_texture_003.Color -> mix_002.B
        signmaterial.links.new(image_texture_003.outputs[0], mix_002.inputs[7])
        #image_texture_003.Alpha -> mix_002.Factor
        signmaterial.links.new(image_texture_003.outputs[1], mix_002.inputs[0])
        #mix_001.Result -> principled_bsdf.Base Color
        signmaterial.links.new(mix_001.outputs[2], principled_bsdf.inputs[0])
        #image_texture_004.Color -> principled_bsdf.Normal
        signmaterial.links.new(image_texture_004.outputs[0], principled_bsdf.inputs[5])
        #image_texture_005.Color -> principled_bsdf.Diffuse Roughness
        signmaterial.links.new(image_texture_005.outputs[0], principled_bsdf.inputs[7])
        return signmaterial

    signmaterial = signmaterial_node_group()
    obj.data.materials.append(mat)

