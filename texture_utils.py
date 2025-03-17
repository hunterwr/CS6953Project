    ####Place custom functions to apply textures appropriately here####
import bpy, mathutils
import random
import bmesh
from mathutils import Vector 

def square_unwrap(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    mesh = bmesh.from_edit_mesh(obj.data)
    front_normal = Vector((0, -1, 0))
    front_face = max(mesh.faces, key=lambda f: f.normal.dot(front_normal))
    for face in mesh.faces:
        face.select = (face == front_face)
    bmesh.update_edit_mesh(obj.data)
    

    if not obj.data.uv_layers:
            obj.data.uv_layers.new(name="UVMap")

  
    uv_layer = obj.data.uv_layers.active.data

    
    min_x = min(vert.co.x for vert in front_face.verts)
    max_x = max(vert.co.x for vert in front_face.verts)
    min_y = min(vert.co.z for vert in front_face.verts)  

    
    for loop in front_face.loops:
        vert = loop.vert
        loop_index = loop.index  
        if loop_index >= len(uv_layer):  
            print(f"Error: UV index {loop_index} out of range!")
            continue
        loop_uv = uv_layer[loop_index]
        loop_uv.uv.x = (vert.co.x - min_x) / (max_x - min_x)
        loop_uv.uv.y = (vert.co.z - min_y) / (max_x - min_x)  

    bmesh.update_edit_mesh(obj.data)

   
    bpy.ops.object.mode_set(mode='OBJECT')


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








def apply_blenderkit_sign_jpg(obj,target_directory,base_color_path = None,scratches_on =0.25, rust_minor_on = 0.25, rust_major_on = False,rivets_on=True):
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



def apply_sign_png(obj,png_path,scratches_on =0.25, rust_minor_on = 0.25, rust_major_on = False,rivets_on=True,target_directory =None):
    tex_path=r'/textures/Signs/'
    if target_directory != None:
        tex_path = target_directory+tex_path
    rust_major = r'/rust.png'
    rust_minor = r'/rust.jpg'
    scratches = r'/scratches.jpg'
    rivets = r'/metal_rivets_textures_2k/metal-23_normal.jpg'
    rivets_rough = r'/metal_rivets_textures_2k/metal-23_roughness.jpg'

    square_unwrap(obj=obj)
    

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
        image_texture.image = bpy.data.images.load(png_path) 

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
        if scratches_on > 0:
            mix.inputs[0].default_value = scratches_on
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
        if rust_minor_on > 0:
            mix_001.inputs[0].default_value = rust_minor_on
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
        rand_z_rotate = 6.28319*random.random()
        mapping.inputs[2].default_value = (0.9267697930335999, 0.1745329350233078, rand_z_rotate)
        #Scale
        mapping.inputs[3].default_value = (1.0, 1.0, 1.0)

        #node Mapping.001
        mapping_001 = signmaterial.nodes.new("ShaderNodeMapping")
        mapping_001.name = "Mapping.001"
        mapping_001.vector_type = 'POINT'
        #Location
        mapping_001.inputs[1].default_value = (0.0, 0.0, 0.0)
        #Rotation
        mapping_001.inputs[2].default_value = (0.0, 0.0, 1.5708)
        #Scale
        mapping_001.inputs[3].default_value = (1, 1, 1.0)

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
        if rivets_on == True:
            signmaterial.links.new(image_texture_004.outputs[0], principled_bsdf.inputs[5])
        #image_texture_005.Color -> principled_bsdf.Diffuse Roughness
            signmaterial.links.new(image_texture_005.outputs[0], principled_bsdf.inputs[7])
        signmaterial.links.new(image_texture.outputs[1], principled_bsdf.inputs[4])
        return signmaterial

    signmaterial = signmaterial_node_group()
    obj.data.materials.append(mat)


def apply_sign_png_conditions(obj,png_path,scratches_on =0.25, rust_minor_on = 0.25, rust_major_on = False,rivets_on=False,snow = 0.0, mud = 0.0, target_directory =None):
    tex_path=r'/textures/Signs/'
    if target_directory != None:
        tex_path = target_directory+tex_path
    rust_major = r'/rust.png'
    rust_minor = r'/rust.jpg'
    scratches = r'/scratches.jpg'
    rivets = r'/metal_rivets_textures_2k/metal-23_normal.jpg'
    rivets_rough = r'/metal_rivets_textures_2k/metal-23_roughness.jpg'



    square_unwrap(obj=obj)
        
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
        #Normal
        principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
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
        image_texture.image = bpy.data.images.load(png_path) 

        #node Image Texture.001
        image_texture_001 = signmaterial.nodes.new("ShaderNodeTexImage")
        image_texture_001.label = "Scratches"
        image_texture_001.name = "Image Texture.001"
        image_texture_001.extension = 'REPEAT'
        image_texture_001.image_user.frame_current = 0
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
        if scratches_on > 0:
            mix.inputs[0].default_value = scratches_on
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
        if rust_minor_on > 0:
            mix_001.inputs[0].default_value = rust_minor_on
        else:
            mix_001.inputs[0].default_value = 0.0

        #node Image Texture.002
        image_texture_002 = signmaterial.nodes.new("ShaderNodeTexImage")
        image_texture_002.label = "Rust Minor"
        image_texture_002.name = "Image Texture.002"
        image_texture_002.extension = 'REPEAT'
        image_texture_002.image_user.frame_current = 0
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
        rand_z_rotate = 6.28319*random.random()
        mapping.inputs[2].default_value = (0.9267697930335999, 0.1745329350233078, rand_z_rotate)
        #Scale
        mapping.inputs[3].default_value = (1.0, 1.0, 1.0)

        #node Mapping.001
        mapping_001 = signmaterial.nodes.new("ShaderNodeMapping")
        mapping_001.name = "Mapping.001"
        mapping_001.vector_type = 'POINT'
        #Location
        mapping_001.inputs[1].default_value = (0.0, 0.0, 0.0)
        #Rotation
        mapping_001.inputs[2].default_value = (0.0, 0.0, 1.5707999467849731)
        #Scale
        mapping_001.inputs[3].default_value = (1.0, 1.0, 1.0)

        #node Image Texture.003
        image_texture_003 = signmaterial.nodes.new("ShaderNodeTexImage")
        image_texture_003.label = "Rust Major"
        image_texture_003.name = "Image Texture.003"
        image_texture_003.extension = 'REPEAT'
        image_texture_003.image_user.frame_current = 0
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
        image_texture_004.image_user.frame_current = 0
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
        image_texture_005.image_user.frame_current = 0
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

        #node Material Output.001
        material_output_001 = signmaterial.nodes.new("ShaderNodeOutputMaterial")
        material_output_001.name = "Material Output.001"
        material_output_001.is_active_output = True
        material_output_001.target = 'ALL'
        #Thickness
        material_output_001.inputs[3].default_value = 0.0

        #node Voronoi Texture
        voronoi_texture = signmaterial.nodes.new("ShaderNodeTexVoronoi")
        voronoi_texture.name = "Voronoi Texture"
        voronoi_texture.distance = 'EUCLIDEAN'
        voronoi_texture.feature = 'F1'
        voronoi_texture.normalize = False
        voronoi_texture.voronoi_dimensions = '3D'
        #Scale
        voronoi_texture.inputs[2].default_value = 5.0
        #Detail
        voronoi_texture.inputs[3].default_value = 0.0
        #Roughness
        voronoi_texture.inputs[4].default_value = 0.5
        #Lacunarity
        voronoi_texture.inputs[5].default_value = 2.0
        #Randomness
        voronoi_texture.inputs[8].default_value = 1.0

        #node Displacement
        displacement = signmaterial.nodes.new("ShaderNodeDisplacement")
        displacement.name = "Displacement"
        displacement.space = 'OBJECT'
        #Height
        displacement.inputs[0].default_value = 0.5999999046325684
        #Midlevel
        displacement.inputs[1].default_value = 0.5
        #Normal
        displacement.inputs[3].default_value = (0.0, 0.0, 0.0)

        #node ColorRamp.001
        colorramp_001 = signmaterial.nodes.new("ShaderNodeValToRGB")
        colorramp_001.name = "ColorRamp.001"
        colorramp_001.color_ramp.color_mode = 'RGB'
        colorramp_001.color_ramp.hue_interpolation = 'NEAR'
        colorramp_001.color_ramp.interpolation = 'LINEAR'

        #initialize color ramp elements
        colorramp_001.color_ramp.elements.remove(colorramp_001.color_ramp.elements[0])
        colorramp_001_cre_0 = colorramp_001.color_ramp.elements[0]
        colorramp_001_cre_0.position = 0.0
        colorramp_001_cre_0.alpha = 1.0
        colorramp_001_cre_0.color = (0.07733254134654999, 0.059307511895895004, 0.1461154669523239, 1.0)

        colorramp_001_cre_1 = colorramp_001.color_ramp.elements.new(0.8181818127632141)
        colorramp_001_cre_1.alpha = 1.0
        colorramp_001_cre_1.color = (0.9220297932624817, 1.0, 1.0, 1.0)


        #node Principled BSDF.001
        principled_bsdf_001 = signmaterial.nodes.new("ShaderNodeBsdfPrincipled")
        principled_bsdf_001.name = "Principled BSDF.001"
        principled_bsdf_001.distribution = 'GGX'
        principled_bsdf_001.subsurface_method = 'RANDOM_WALK_SKIN'
        #Metallic
        principled_bsdf_001.inputs[1].default_value = 0.0
        #IOR
        principled_bsdf_001.inputs[3].default_value = 1.4500000476837158
        #Alpha
        principled_bsdf_001.inputs[4].default_value = 1.0
        #Normal
        principled_bsdf_001.inputs[5].default_value = (0.0, 0.0, 0.0)
        #Diffuse Roughness
        principled_bsdf_001.inputs[7].default_value = 0.0
        #Subsurface Weight
        principled_bsdf_001.inputs[8].default_value = 1.0
        #Subsurface Radius
        principled_bsdf_001.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
        #Subsurface Scale
        principled_bsdf_001.inputs[10].default_value = 0.10909092426300049
        #Subsurface IOR
        principled_bsdf_001.inputs[11].default_value = 1.399999976158142
        #Subsurface Anisotropy
        principled_bsdf_001.inputs[12].default_value = 0.0
        #Specular IOR Level
        principled_bsdf_001.inputs[13].default_value = 0.5
        #Specular Tint
        principled_bsdf_001.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
        #Anisotropic
        principled_bsdf_001.inputs[15].default_value = 0.0
        #Anisotropic Rotation
        principled_bsdf_001.inputs[16].default_value = 0.0
        #Tangent
        principled_bsdf_001.inputs[17].default_value = (0.0, 0.0, 0.0)
        #Transmission Weight
        principled_bsdf_001.inputs[18].default_value = 0.0
        #Coat Weight
        principled_bsdf_001.inputs[19].default_value = 0.0
        #Coat Roughness
        principled_bsdf_001.inputs[20].default_value = 0.029999999329447746
        #Coat IOR
        principled_bsdf_001.inputs[21].default_value = 1.5
        #Coat Tint
        principled_bsdf_001.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
        #Coat Normal
        principled_bsdf_001.inputs[23].default_value = (0.0, 0.0, 0.0)
        #Sheen Weight
        principled_bsdf_001.inputs[24].default_value = 0.0
        #Sheen Roughness
        principled_bsdf_001.inputs[25].default_value = 0.5
        #Sheen Tint
        principled_bsdf_001.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
        #Emission Color
        principled_bsdf_001.inputs[27].default_value = (0.0, 0.0, 0.0, 1.0)
        #Emission Strength
        principled_bsdf_001.inputs[28].default_value = 0.19999992847442627
        #Thin Film Thickness
        principled_bsdf_001.inputs[29].default_value = 0.0
        #Thin Film IOR
        principled_bsdf_001.inputs[30].default_value = 1.3300000429153442

        #node Mix.003
        mix_003 = signmaterial.nodes.new("ShaderNodeMix")
        mix_003.name = "Mix.003"
        mix_003.blend_type = 'OVERLAY'
        mix_003.clamp_factor = True
        mix_003.clamp_result = False
        mix_003.data_type = 'RGBA'
        mix_003.factor_mode = 'UNIFORM'
        #Factor_Float
        mix_003.inputs[0].default_value = 1.0

        #node ColorRamp.002
        colorramp_002 = signmaterial.nodes.new("ShaderNodeValToRGB")
        colorramp_002.name = "ColorRamp.002"
        colorramp_002.color_ramp.color_mode = 'RGB'
        colorramp_002.color_ramp.hue_interpolation = 'NEAR'
        colorramp_002.color_ramp.interpolation = 'LINEAR'

        #initialize color ramp elements
        colorramp_002.color_ramp.elements.remove(colorramp_002.color_ramp.elements[0])
        colorramp_002_cre_0 = colorramp_002.color_ramp.elements[0]
        colorramp_002_cre_0.position = 0.472727507352829
        colorramp_002_cre_0.alpha = 1.0
        colorramp_002_cre_0.color = (0.0, 0.0, 0.0, 1.0)

        colorramp_002_cre_1 = colorramp_002.color_ramp.elements.new(0.9863636493682861)
        colorramp_002_cre_1.alpha = 1.0
        colorramp_002_cre_1.color = (1.0, 1.0, 1.0, 1.0)


        #node ColorRamp
        colorramp = signmaterial.nodes.new("ShaderNodeValToRGB")
        colorramp.name = "ColorRamp"
        colorramp.color_ramp.color_mode = 'RGB'
        colorramp.color_ramp.hue_interpolation = 'NEAR'
        colorramp.color_ramp.interpolation = 'LINEAR'

        #initialize color ramp elements
        colorramp.color_ramp.elements.remove(colorramp.color_ramp.elements[0])
        colorramp_cre_0 = colorramp.color_ramp.elements[0]
        colorramp_cre_0.position = 0.48181840777397156
        colorramp_cre_0.alpha = 1.0
        colorramp_cre_0.color = (1.0, 0.9665863513946533, 0.940509021282196, 1.0)

        colorramp_cre_1 = colorramp.color_ramp.elements.new(0.9863636493682861)
        colorramp_cre_1.alpha = 1.0
        colorramp_cre_1.color = (1.0, 1.0, 1.0, 1.0)


        #node Mapping.002
        mapping_002 = signmaterial.nodes.new("ShaderNodeMapping")
        mapping_002.name = "Mapping.002"
        mapping_002.vector_type = 'POINT'
        #Location
        mapping_002.inputs[1].default_value = (0.0, 0.0, 0.0)
        #Rotation
        mapping_002.inputs[2].default_value = (0.0, 0.0, 0.0)
        #Scale
        mapping_002.inputs[3].default_value = (1.0, 1.0, 1.0)

        #node Texture Coordinate.001
        texture_coordinate_001 = signmaterial.nodes.new("ShaderNodeTexCoord")
        texture_coordinate_001.name = "Texture Coordinate.001"
        texture_coordinate_001.from_instancer = False

        #node Noise Texture
        noise_texture = signmaterial.nodes.new("ShaderNodeTexNoise")
        noise_texture.name = "Noise Texture"
        noise_texture.noise_dimensions = '3D'
        noise_texture.noise_type = 'FBM'
        noise_texture.normalize = True
        #Scale
        noise_texture.inputs[2].default_value = 10.5
        #Detail
        noise_texture.inputs[3].default_value = 9.899999618530273
        #Roughness
        noise_texture.inputs[4].default_value = 0.5833332538604736
        #Lacunarity
        noise_texture.inputs[5].default_value = 2.0
        #Distortion
        noise_texture.inputs[8].default_value = 0.0

        #node Mix.004
        mix_004 = signmaterial.nodes.new("ShaderNodeMix")
        mix_004.name = "Mix.004"
        mix_004.blend_type = 'MIX'
        mix_004.clamp_factor = True
        mix_004.clamp_result = False
        mix_004.data_type = 'RGBA'
        mix_004.factor_mode = 'UNIFORM'
        #Factor_Float
        mix_004.inputs[0].default_value = 0.10909092426300049
        #B_Color
        mix_004.inputs[7].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)

        #node Mix Shader
        mix_shader = signmaterial.nodes.new("ShaderNodeMixShader")
        mix_shader.name = "Mix Shader"

        #node Noise Texture.001
        noise_texture_001 = signmaterial.nodes.new("ShaderNodeTexNoise")
        noise_texture_001.name = "Noise Texture.001"
        noise_texture_001.noise_dimensions = '3D'
        noise_texture_001.noise_type = 'FBM'
        noise_texture_001.normalize = True
        #Scale
        noise_texture_001.inputs[2].default_value = 5.0
        #Detail
        noise_texture_001.inputs[3].default_value = 2.0
        #Roughness
        noise_texture_001.inputs[4].default_value = 0.5
        #Lacunarity
        noise_texture_001.inputs[5].default_value = 2.0
        #Distortion
        noise_texture_001.inputs[8].default_value = 0.0

        #node Color Ramp
        color_ramp = signmaterial.nodes.new("ShaderNodeValToRGB")
        color_ramp.name = "Color Ramp"
        color_ramp.color_ramp.color_mode = 'RGB'
        color_ramp.color_ramp.hue_interpolation = 'NEAR'
        color_ramp.color_ramp.interpolation = 'LINEAR'

        #initialize color ramp elements

        if mud> 0.0:
            black_value = mud
        elif snow>0.0:
            black_value = snow
        elif snow == 0.0 and mud ==0.0:
            black_value =0.5


        color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[0])
        color_ramp_cre_0 = color_ramp.color_ramp.elements[0]
        color_ramp_cre_0.position = black_value
        color_ramp_cre_0.alpha = 1.0
        color_ramp_cre_0.color = (0.0, 0.0, 0.0, 1.0)

        color_ramp_cre_1 = color_ramp.color_ramp.elements.new(black_value-0.08)
        color_ramp_cre_1.alpha = 1.0
        color_ramp_cre_1.color = (1.0, 1.0, 1.0, 1.0)


        #node Frame
        frame = signmaterial.nodes.new("NodeFrame")
        frame.name = "Frame"
        frame.label_size = 20
        frame.shrink = True

        #node Principled BSDF.002
        principled_bsdf_002 = signmaterial.nodes.new("ShaderNodeBsdfPrincipled")
        principled_bsdf_002.name = "Principled BSDF.002"
        principled_bsdf_002.distribution = 'MULTI_GGX'
        principled_bsdf_002.subsurface_method = 'RANDOM_WALK'
        #Metallic
        principled_bsdf_002.inputs[1].default_value = 0.0
        #IOR
        principled_bsdf_002.inputs[3].default_value = 1.5
        #Diffuse Roughness
        principled_bsdf_002.inputs[7].default_value = 0.0
        #Subsurface Weight
        principled_bsdf_002.inputs[8].default_value = 0.0
        #Subsurface Radius
        principled_bsdf_002.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
        #Subsurface Scale
        principled_bsdf_002.inputs[10].default_value = 0.05000000074505806
        #Subsurface Anisotropy
        principled_bsdf_002.inputs[12].default_value = 0.0
        #Specular IOR Level
        principled_bsdf_002.inputs[13].default_value = 0.5
        #Specular Tint
        principled_bsdf_002.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
        #Anisotropic
        principled_bsdf_002.inputs[15].default_value = 0.0
        #Anisotropic Rotation
        principled_bsdf_002.inputs[16].default_value = 0.0
        #Tangent
        principled_bsdf_002.inputs[17].default_value = (0.0, 0.0, 0.0)
        #Transmission Weight
        principled_bsdf_002.inputs[18].default_value = 0.0
        #Coat Weight
        principled_bsdf_002.inputs[19].default_value = 0.0
        #Coat Roughness
        principled_bsdf_002.inputs[20].default_value = 0.029999999329447746
        #Coat IOR
        principled_bsdf_002.inputs[21].default_value = 1.5
        #Coat Tint
        principled_bsdf_002.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
        #Coat Normal
        principled_bsdf_002.inputs[23].default_value = (0.0, 0.0, 0.0)
        #Sheen Weight
        principled_bsdf_002.inputs[24].default_value = 0.0
        #Sheen Roughness
        principled_bsdf_002.inputs[25].default_value = 0.5
        #Sheen Tint
        principled_bsdf_002.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
        #Emission Color
        principled_bsdf_002.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
        #Emission Strength
        principled_bsdf_002.inputs[28].default_value = 0.0
        #Thin Film Thickness
        principled_bsdf_002.inputs[29].default_value = 0.0
        #Thin Film IOR
        principled_bsdf_002.inputs[30].default_value = 1.3300000429153442

        #node Noise Texture.002
        noise_texture_002 = signmaterial.nodes.new("ShaderNodeTexNoise")
        noise_texture_002.name = "Noise Texture.002"
        noise_texture_002.noise_dimensions = '3D'
        noise_texture_002.noise_type = 'FBM'
        noise_texture_002.normalize = True
        #Scale
        noise_texture_002.inputs[2].default_value = 13.0
        #Detail
        noise_texture_002.inputs[3].default_value = 15.0
        #Roughness
        noise_texture_002.inputs[4].default_value = 0.6000000238418579
        #Lacunarity
        noise_texture_002.inputs[5].default_value = 2.0
        #Distortion
        noise_texture_002.inputs[8].default_value = 0.0

        #node Mapping.003
        mapping_003 = signmaterial.nodes.new("ShaderNodeMapping")
        mapping_003.name = "Mapping.003"
        mapping_003.vector_type = 'POINT'
        #Location
        mapping_003.inputs[1].default_value = (0.0, 0.0, 0.0)
        #Rotation
        mapping_003.inputs[2].default_value = (0.0, 0.0, 0.0)
        #Scale
        mapping_003.inputs[3].default_value = (1.0, 1.0, 1.0)

        #node Texture Coordinate.002
        texture_coordinate_002 = signmaterial.nodes.new("ShaderNodeTexCoord")
        texture_coordinate_002.name = "Texture Coordinate.002"
        texture_coordinate_002.from_instancer = False

        #node Color Ramp.001
        color_ramp_001 = signmaterial.nodes.new("ShaderNodeValToRGB")
        color_ramp_001.name = "Color Ramp.001"
        color_ramp_001.color_ramp.color_mode = 'RGB'
        color_ramp_001.color_ramp.hue_interpolation = 'NEAR'
        color_ramp_001.color_ramp.interpolation = 'LINEAR'

        #initialize color ramp elements
        color_ramp_001.color_ramp.elements.remove(color_ramp_001.color_ramp.elements[0])
        color_ramp_001_cre_0 = color_ramp_001.color_ramp.elements[0]
        color_ramp_001_cre_0.position = 0.0
        color_ramp_001_cre_0.alpha = 1.0
        color_ramp_001_cre_0.color = (0.03189585357904434, 0.02217390388250351, 0.01161225326359272, 1.0)

        color_ramp_001_cre_1 = color_ramp_001.color_ramp.elements.new(1.0)
        color_ramp_001_cre_1.alpha = 1.0
        color_ramp_001_cre_1.color = (0.08021937310695648, 0.05126950517296791, 0.03560134768486023, 1.0)


        #node Color Ramp.002
        color_ramp_002 = signmaterial.nodes.new("ShaderNodeValToRGB")
        color_ramp_002.name = "Color Ramp.002"
        color_ramp_002.color_ramp.color_mode = 'RGB'
        color_ramp_002.color_ramp.hue_interpolation = 'NEAR'
        color_ramp_002.color_ramp.interpolation = 'LINEAR'

        #initialize color ramp elements
        color_ramp_002.color_ramp.elements.remove(color_ramp_002.color_ramp.elements[0])
        color_ramp_002_cre_0 = color_ramp_002.color_ramp.elements[0]
        color_ramp_002_cre_0.position = 0.0
        color_ramp_002_cre_0.alpha = 1.0
        color_ramp_002_cre_0.color = (0.0, 0.0, 0.0, 1.0)

        color_ramp_002_cre_1 = color_ramp_002.color_ramp.elements.new(1.0)
        color_ramp_002_cre_1.alpha = 1.0
        color_ramp_002_cre_1.color = (0.5647079944610596, 0.5647121667861938, 0.5647119283676147, 1.0)


        #node Bump
        bump = signmaterial.nodes.new("ShaderNodeBump")
        bump.name = "Bump"
        bump.invert = False
        #Strength
        bump.inputs[0].default_value = 0.20000000298023224
        #Distance
        bump.inputs[1].default_value = 1.0
        #Normal
        bump.inputs[3].default_value = (0.0, 0.0, 0.0)

        #node Principled BSDF.003
        principled_bsdf_003 = signmaterial.nodes.new("ShaderNodeBsdfPrincipled")
        principled_bsdf_003.name = "Principled BSDF.003"
        principled_bsdf_003.distribution = 'MULTI_GGX'
        principled_bsdf_003.subsurface_method = 'RANDOM_WALK'
        #Metallic
        principled_bsdf_003.inputs[1].default_value = 0.0
        #Roughness
        principled_bsdf_003.inputs[2].default_value = 0.10000000149011612
        #IOR
        principled_bsdf_003.inputs[3].default_value = 1.5
        #Diffuse Roughness
        principled_bsdf_003.inputs[7].default_value = 0.0
        #Subsurface Weight
        principled_bsdf_003.inputs[8].default_value = 0.0
        #Subsurface Radius
        principled_bsdf_003.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
        #Subsurface Scale
        principled_bsdf_003.inputs[10].default_value = 0.05000000074505806
        #Subsurface Anisotropy
        principled_bsdf_003.inputs[12].default_value = 0.0
        #Specular IOR Level
        principled_bsdf_003.inputs[13].default_value = 0.5
        #Specular Tint
        principled_bsdf_003.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
        #Anisotropic
        principled_bsdf_003.inputs[15].default_value = 0.0
        #Anisotropic Rotation
        principled_bsdf_003.inputs[16].default_value = 0.0
        #Tangent
        principled_bsdf_003.inputs[17].default_value = (0.0, 0.0, 0.0)
        #Transmission Weight
        principled_bsdf_003.inputs[18].default_value = 0.0
        #Coat Weight
        principled_bsdf_003.inputs[19].default_value = 0.0
        #Coat Roughness
        principled_bsdf_003.inputs[20].default_value = 0.029999999329447746
        #Coat IOR
        principled_bsdf_003.inputs[21].default_value = 1.5
        #Coat Tint
        principled_bsdf_003.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
        #Coat Normal
        principled_bsdf_003.inputs[23].default_value = (0.0, 0.0, 0.0)
        #Sheen Weight
        principled_bsdf_003.inputs[24].default_value = 0.0
        #Sheen Roughness
        principled_bsdf_003.inputs[25].default_value = 0.5
        #Sheen Tint
        principled_bsdf_003.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
        #Emission Color
        principled_bsdf_003.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
        #Emission Strength
        principled_bsdf_003.inputs[28].default_value = 0.0
        #Thin Film Thickness
        principled_bsdf_003.inputs[29].default_value = 0.0
        #Thin Film IOR
        principled_bsdf_003.inputs[30].default_value = 1.3300000429153442

        #node Noise Texture.003
        noise_texture_003 = signmaterial.nodes.new("ShaderNodeTexNoise")
        noise_texture_003.name = "Noise Texture.003"
        noise_texture_003.noise_dimensions = '3D'
        noise_texture_003.noise_type = 'FBM'
        noise_texture_003.normalize = True
        #Scale
        noise_texture_003.inputs[2].default_value = 13.0
        #Detail
        noise_texture_003.inputs[3].default_value = 15.0
        #Roughness
        noise_texture_003.inputs[4].default_value = 0.699999988079071
        #Lacunarity
        noise_texture_003.inputs[5].default_value = 2.0
        #Distortion
        noise_texture_003.inputs[8].default_value = 1.0

        #node Color Ramp.003
        color_ramp_003 = signmaterial.nodes.new("ShaderNodeValToRGB")
        color_ramp_003.name = "Color Ramp.003"
        color_ramp_003.color_ramp.color_mode = 'RGB'
        color_ramp_003.color_ramp.hue_interpolation = 'NEAR'
        color_ramp_003.color_ramp.interpolation = 'LINEAR'

        #initialize color ramp elements
        color_ramp_003.color_ramp.elements.remove(color_ramp_003.color_ramp.elements[0])
        color_ramp_003_cre_0 = color_ramp_003.color_ramp.elements[0]
        color_ramp_003_cre_0.position = 0.0
        color_ramp_003_cre_0.alpha = 1.0
        color_ramp_003_cre_0.color = (0.03189585357904434, 0.02217390388250351, 0.01161225326359272, 1.0)

        color_ramp_003_cre_1 = color_ramp_003.color_ramp.elements.new(1.0)
        color_ramp_003_cre_1.alpha = 1.0
        color_ramp_003_cre_1.color = (0.21222949028015137, 0.1412634402513504, 0.09084176272153854, 1.0)


        #node Bump.001
        bump_001 = signmaterial.nodes.new("ShaderNodeBump")
        bump_001.name = "Bump.001"
        bump_001.invert = False
        #Strength
        bump_001.inputs[0].default_value = 0.029999999329447746
        #Distance
        bump_001.inputs[1].default_value = 1.0
        #Normal
        bump_001.inputs[3].default_value = (0.0, 0.0, 0.0)

        #node Mix Shader.001
        mix_shader_001 = signmaterial.nodes.new("ShaderNodeMixShader")
        mix_shader_001.name = "Mix Shader.001"

        #node Noise Texture.004
        noise_texture_004 = signmaterial.nodes.new("ShaderNodeTexNoise")
        noise_texture_004.name = "Noise Texture.004"
        noise_texture_004.noise_dimensions = '3D'
        noise_texture_004.noise_type = 'FBM'
        noise_texture_004.normalize = True
        #Scale
        noise_texture_004.inputs[2].default_value = 3.0
        #Detail
        noise_texture_004.inputs[3].default_value = 15.0
        #Roughness
        noise_texture_004.inputs[4].default_value = 0.5
        #Lacunarity
        noise_texture_004.inputs[5].default_value = 2.0
        #Distortion
        noise_texture_004.inputs[8].default_value = 0.0

        #node Color Ramp.004
        color_ramp_004 = signmaterial.nodes.new("ShaderNodeValToRGB")
        color_ramp_004.name = "Color Ramp.004"
        color_ramp_004.color_ramp.color_mode = 'RGB'
        color_ramp_004.color_ramp.hue_interpolation = 'NEAR'
        color_ramp_004.color_ramp.interpolation = 'LINEAR'

        #initialize color ramp elements
        color_ramp_004.color_ramp.elements.remove(color_ramp_004.color_ramp.elements[0])
        color_ramp_004_cre_0 = color_ramp_004.color_ramp.elements[0]
        color_ramp_004_cre_0.position = 0.39999985694885254
        color_ramp_004_cre_0.alpha = 1.0
        color_ramp_004_cre_0.color = (0.0, 0.0, 0.0, 1.0)

        color_ramp_004_cre_1 = color_ramp_004.color_ramp.elements.new(0.4909094572067261)
        color_ramp_004_cre_1.alpha = 1.0
        color_ramp_004_cre_1.color = (1.0, 1.0, 1.0, 1.0)


        #node Displacement.001
        displacement_001 = signmaterial.nodes.new("ShaderNodeDisplacement")
        displacement_001.name = "Displacement.001"
        displacement_001.space = 'OBJECT'
        #Midlevel
        displacement_001.inputs[1].default_value = 0.0
        #Scale
        displacement_001.inputs[2].default_value = 0.03999999910593033
        #Normal
        displacement_001.inputs[3].default_value = (0.0, 0.0, 0.0)

        #node Mix.005
        mix_005 = signmaterial.nodes.new("ShaderNodeMix")
        mix_005.name = "Mix.005"
        mix_005.blend_type = 'MIX'
        mix_005.clamp_factor = True
        mix_005.clamp_result = False
        mix_005.data_type = 'RGBA'
        mix_005.factor_mode = 'UNIFORM'
        #B_Color
        mix_005.inputs[7].default_value = (0.0, 0.0, 0.0, 1.0)

        #node Invert Color
        invert_color = signmaterial.nodes.new("ShaderNodeInvert")
        invert_color.name = "Invert Color"
        #Fac
        invert_color.inputs[0].default_value = 1.0

        #node Frame.001
        frame_001 = signmaterial.nodes.new("NodeFrame")
        frame_001.name = "Frame.001"
        frame_001.label_size = 20
        frame_001.shrink = True

                #node Displacement.002
        displacement_002 = signmaterial.nodes.new("ShaderNodeDisplacement")
        displacement_002.label = "DISPLACEMENT FOR PNG"
        displacement_002.name = "Displacement.002"
        displacement_002.space = 'OBJECT'
        #Midlevel
        displacement_002.inputs[1].default_value = 0.5
        #Scale
        displacement_002.inputs[2].default_value = 1.0

        #Set locations
        principled_bsdf.location = (510.5553283691406, -59.9542236328125)
        image_texture.location = (-658.6177978515625, 66.822265625)
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
        material_output_001.location = (1959.68359375, -975.3723754882812)
        voronoi_texture.location = (-940.3441162109375, -1402.0634765625)
        displacement.location = (789.5448608398438, -1730.8603515625)
        colorramp_001.location = (-493.6947937011719, -1812.22265625)
        principled_bsdf_001.location = (418.7927551269531, -1422.31787109375)
        mix_003.location = (-708.8441162109375, -1151.271240234375)
        colorramp_002.location = (-111.66281127929688, -1571.203857421875)
        colorramp.location = (-368.0056457519531, -1261.1865234375)
        mapping_002.location = (-1550.2725830078125, -1137.20263671875)
        texture_coordinate_001.location = (-1730.2723388671875, -1137.20263671875)
        noise_texture.location = (-952.6441650390625, -1056.30810546875)
        mix_004.location = (248.79275512695312, -1542.31787109375)
        mix_shader.location = (1569.85791015625, -764.6122436523438)
        noise_texture_001.location = (1133.0177001953125, 103.29817199707031)
        color_ramp.location = (1475.7100830078125, 1.5466625690460205)
        frame.location = (-299.72802734375, -1494.472900390625)
        principled_bsdf_002.location = (605.614013671875, 953.3546752929688)
        noise_texture_002.location = (-160.20770263671875, 1132.1702880859375)
        mapping_003.location = (-472.304443359375, 1658.639404296875)
        texture_coordinate_002.location = (-658.140380859375, 1688.0921630859375)
        color_ramp_001.location = (63.09385681152344, 1117.67724609375)
        color_ramp_002.location = (62.693206787109375, 892.7188720703125)
        bump.location = (81.29820251464844, 656.4393310546875)
        principled_bsdf_003.location = (598.4451904296875, 1623.074951171875)
        noise_texture_003.location = (-111.94149780273438, 1853.592529296875)
        color_ramp_003.location = (108.19537353515625, 1845.7601318359375)
        bump_001.location = (357.6639404296875, 1581.8834228515625)
        mix_shader_001.location = (982.8507080078125, 1381.4736328125)
        noise_texture_004.location = (-134.80438232421875, 1480.1810302734375)
        color_ramp_004.location = (256.40106201171875, 1366.7816162109375)
        displacement_001.location = (1015.9722900390625, 616.9949951171875)
        mix_005.location = (661.4043579101562, 532.2132568359375)
        invert_color.location = (491.7807922363281, 637.0462036132812)
        frame_001.location = (440.9736328125, 1237.7647705078125)

        #Set dimensions
        principled_bsdf.width, principled_bsdf.height = 240.0, 100.0
        image_texture.width, image_texture.height = 240.0, 100.0
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
        material_output_001.width, material_output_001.height = 140.0, 100.0
        voronoi_texture.width, voronoi_texture.height = 140.0, 100.0
        displacement.width, displacement.height = 140.0, 100.0
        colorramp_001.width, colorramp_001.height = 240.0, 100.0
        principled_bsdf_001.width, principled_bsdf_001.height = 240.0, 100.0
        mix_003.width, mix_003.height = 140.0, 100.0
        colorramp_002.width, colorramp_002.height = 240.0, 100.0
        colorramp.width, colorramp.height = 240.0, 100.0
        mapping_002.width, mapping_002.height = 140.0, 100.0
        texture_coordinate_001.width, texture_coordinate_001.height = 140.0, 100.0
        noise_texture.width, noise_texture.height = 140.0, 100.0
        mix_004.width, mix_004.height = 140.0, 100.0
        mix_shader.width, mix_shader.height = 140.0, 100.0
        noise_texture_001.width, noise_texture_001.height = 140.0, 100.0
        color_ramp.width, color_ramp.height = 240.0, 100.0
        frame.width, frame.height = 3310.129638671875, 1106.0250244140625
        principled_bsdf_002.width, principled_bsdf_002.height = 240.0, 100.0
        noise_texture_002.width, noise_texture_002.height = 164.716796875, 100.0
        mapping_003.width, mapping_003.height = 140.0, 100.0
        texture_coordinate_002.width, texture_coordinate_002.height = 140.0, 100.0
        color_ramp_001.width, color_ramp_001.height = 240.0, 100.0
        color_ramp_002.width, color_ramp_002.height = 240.0, 100.0
        bump.width, bump.height = 140.0, 100.0
        principled_bsdf_003.width, principled_bsdf_003.height = 240.0, 100.0
        noise_texture_003.width, noise_texture_003.height = 140.0, 100.0
        color_ramp_003.width, color_ramp_003.height = 240.0, 100.0
        bump_001.width, bump_001.height = 140.0, 100.0
        mix_shader_001.width, mix_shader_001.height = 140.0, 100.0
        noise_texture_004.width, noise_texture_004.height = 140.0, 100.0
        color_ramp_004.width, color_ramp_004.height = 240.0, 100.0
        displacement_001.width, displacement_001.height = 140.0, 100.0
        mix_005.width, mix_005.height = 140.0, 100.0
        invert_color.width, invert_color.height = 140.0, 100.0
        frame_001.width, frame_001.height = 3044.44970703125, 1855.811767578125

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
        #image_texture_003.Color -> mix_002.B
        signmaterial.links.new(image_texture_003.outputs[0], mix_002.inputs[7])
        #image_texture_003.Alpha -> mix_002.Factor
        signmaterial.links.new(image_texture_003.outputs[1], mix_002.inputs[0])
        #mix_001.Result -> principled_bsdf.Base Color
        signmaterial.links.new(mix_001.outputs[2], principled_bsdf.inputs[0])
        #image_texture.Alpha -> principled_bsdf.Alpha
        signmaterial.links.new(image_texture.outputs[1], principled_bsdf.inputs[4])
        #noise_texture.Fac -> mix_003.A
        signmaterial.links.new(noise_texture.outputs[0], mix_003.inputs[6])
        #voronoi_texture.Distance -> mix_003.B
        signmaterial.links.new(voronoi_texture.outputs[0], mix_003.inputs[7])
        #mix_003.Result -> colorramp.Fac
        signmaterial.links.new(mix_003.outputs[2], colorramp.inputs[0])
        #colorramp_001.Color -> displacement.Scale
        signmaterial.links.new(colorramp_001.outputs[0], displacement.inputs[2])
        #mix_003.Result -> colorramp_001.Fac
        signmaterial.links.new(mix_003.outputs[2], colorramp_001.inputs[0])
        #mix_003.Result -> colorramp_002.Fac
        signmaterial.links.new(mix_003.outputs[2], colorramp_002.inputs[0])
        #colorramp_002.Color -> principled_bsdf_001.Roughness
        signmaterial.links.new(colorramp_002.outputs[0], principled_bsdf_001.inputs[2])
        #mapping_002.Vector -> noise_texture.Vector
        signmaterial.links.new(mapping_002.outputs[0], noise_texture.inputs[0])
        #texture_coordinate_001.Generated -> mapping_002.Vector
        signmaterial.links.new(texture_coordinate_001.outputs[0], mapping_002.inputs[0])
        #mapping_002.Vector -> voronoi_texture.Vector
        signmaterial.links.new(mapping_002.outputs[0], voronoi_texture.inputs[0])
        #colorramp.Color -> mix_004.A
        signmaterial.links.new(colorramp.outputs[0], mix_004.inputs[6])
        #mix_004.Result -> principled_bsdf_001.Base Color
        signmaterial.links.new(mix_004.outputs[2], principled_bsdf_001.inputs[0])
        #principled_bsdf.BSDF -> mix_shader.Shader
        signmaterial.links.new(principled_bsdf.outputs[0], mix_shader.inputs[1])
        #mix_shader.Shader -> material_output_001.Surface
        signmaterial.links.new(mix_shader.outputs[0], material_output_001.inputs[0])
        #noise_texture_001.Color -> color_ramp.Fac
        signmaterial.links.new(noise_texture_001.outputs[1], color_ramp.inputs[0])

        #mapping.Vector -> noise_texture_001.Vector
        signmaterial.links.new(mapping.outputs[0], noise_texture_001.inputs[0])
        #mapping_003.Vector -> noise_texture_002.Vector
        signmaterial.links.new(mapping_003.outputs[0], noise_texture_002.inputs[0])
        #texture_coordinate_002.Object -> mapping_003.Vector
        signmaterial.links.new(texture_coordinate_002.outputs[3], mapping_003.inputs[0])
        #color_ramp_001.Color -> principled_bsdf_002.Base Color
        signmaterial.links.new(color_ramp_001.outputs[0], principled_bsdf_002.inputs[0])
        #noise_texture_002.Fac -> color_ramp_001.Fac
        signmaterial.links.new(noise_texture_002.outputs[0], color_ramp_001.inputs[0])
        #color_ramp_002.Color -> principled_bsdf_002.Roughness
        signmaterial.links.new(color_ramp_002.outputs[0], principled_bsdf_002.inputs[2])
        #noise_texture_002.Fac -> color_ramp_002.Fac
        signmaterial.links.new(noise_texture_002.outputs[0], color_ramp_002.inputs[0])
        #bump.Normal -> principled_bsdf_002.Normal
        signmaterial.links.new(bump.outputs[0], principled_bsdf_002.inputs[5])
        #noise_texture_002.Fac -> bump.Height
        signmaterial.links.new(noise_texture_002.outputs[0], bump.inputs[2])
        #mapping_003.Vector -> noise_texture_003.Vector
        signmaterial.links.new(mapping_003.outputs[0], noise_texture_003.inputs[0])
        #color_ramp_003.Color -> principled_bsdf_003.Base Color
        signmaterial.links.new(color_ramp_003.outputs[0], principled_bsdf_003.inputs[0])
        #noise_texture_003.Fac -> color_ramp_003.Fac
        signmaterial.links.new(noise_texture_003.outputs[0], color_ramp_003.inputs[0])
        #bump_001.Normal -> principled_bsdf_003.Normal
        signmaterial.links.new(bump_001.outputs[0], principled_bsdf_003.inputs[5])
        #color_ramp_003.Color -> bump_001.Height
        signmaterial.links.new(color_ramp_003.outputs[0], bump_001.inputs[2])
        #principled_bsdf_003.BSDF -> mix_shader_001.Shader
        signmaterial.links.new(principled_bsdf_003.outputs[0], mix_shader_001.inputs[1])
        #principled_bsdf_002.BSDF -> mix_shader_001.Shader
        signmaterial.links.new(principled_bsdf_002.outputs[0], mix_shader_001.inputs[2])
        #mapping_003.Vector -> noise_texture_004.Vector
        signmaterial.links.new(mapping_003.outputs[0], noise_texture_004.inputs[0])
        #noise_texture_004.Fac -> color_ramp_004.Fac
        signmaterial.links.new(noise_texture_004.outputs[0], color_ramp_004.inputs[0])
        #color_ramp_004.Color -> mix_shader_001.Fac
        signmaterial.links.new(color_ramp_004.outputs[0], mix_shader_001.inputs[0])
        #mix_005.Result -> displacement_001.Height
        signmaterial.links.new(mix_005.outputs[2], displacement_001.inputs[0])
        #noise_texture_002.Fac -> mix_005.A
        signmaterial.links.new(noise_texture_002.outputs[0], mix_005.inputs[6])
        #invert_color.Color -> mix_005.Factor
        signmaterial.links.new(invert_color.outputs[0], mix_005.inputs[0])
        #color_ramp_004.Color -> invert_color.Color
        signmaterial.links.new(color_ramp_004.outputs[0], invert_color.inputs[1])


        #image_texture.Alpha -> principled_bsdf_002.Alpha

        

        ### Conditional Linkages 
        if rivets_on == True:
            signmaterial.links.new(image_texture_004.outputs[0], principled_bsdf.inputs[5])
        #image_texture_005.Color -> principled_bsdf.Diffuse Roughness
            signmaterial.links.new(image_texture_005.outputs[0], principled_bsdf.inputs[7])
        
        if mud>0.0:
                    #color_ramp.Color -> mix_shader.Fac
            signmaterial.links.new(color_ramp.outputs[0], mix_shader.inputs[0])
            signmaterial.links.new(image_texture.outputs[1], principled_bsdf_002.inputs[4])
            #image_texture.Alpha -> principled_bsdf_003.Alpha
            signmaterial.links.new(image_texture.outputs[1], principled_bsdf_003.inputs[4])

                    #mix_shader_001.Shader -> mix_shader.Shader
            signmaterial.links.new(mix_shader_001.outputs[0], mix_shader.inputs[2])

            #displacement_001.Displacement -> material_output_001.Displacement
            signmaterial.links.new(displacement_001.outputs[0], material_output_001.inputs[2])

        if snow >0.0:
                    #color_ramp.Color -> mix_shader.Fac
            signmaterial.links.new(color_ramp.outputs[0], mix_shader.inputs[0])
             #principled_bsdf_001.BSDF -> mix_shader.Shader
            signmaterial.links.new(principled_bsdf_001.outputs[0], mix_shader.inputs[2])
            #displacement.Displacement -> material_output_001.Displacement
            signmaterial.links.new(displacement.outputs[0], material_output_001.inputs[2])
            #image_texture.Alpha -> principled_bsdf_001.Alpha
            signmaterial.links.new(image_texture.outputs[1], principled_bsdf_001.inputs[4])
        
        if snow == 0.0 and mud ==0.0:
            mix_shader.inputs[0].default_value = 0.0
        return signmaterial

    signmaterial = signmaterial_node_group()


    obj.data.materials.append(mat)


















def apply_birch_tree_bark(obj):

    mat = bpy.data.materials.new(name = "Birch Tree bark")
    mat.use_nodes = True
    #initialize Birch Tree bark node group

    birch_tree_bark = mat.node_tree
    #start with a clean node tree
    for node in birch_tree_bark.nodes:
        birch_tree_bark.nodes.remove(node)
    birch_tree_bark.color_tag = 'NONE'
    birch_tree_bark.description = ""
    birch_tree_bark.default_group_node_width = 140
    

    #birch_tree_bark interface

    #initialize birch_tree_bark nodes
    #node Noise Texture.003
    noise_texture_003 = birch_tree_bark.nodes.new("ShaderNodeTexNoise")
    noise_texture_003.name = "Noise Texture.003"
    noise_texture_003.noise_dimensions = '3D'
    noise_texture_003.noise_type = 'FBM'
    noise_texture_003.normalize = True
    #Scale
    noise_texture_003.inputs[2].default_value = 4.0
    #Detail
    noise_texture_003.inputs[3].default_value = 15.0
    #Roughness
    noise_texture_003.inputs[4].default_value = 0.625
    #Lacunarity
    noise_texture_003.inputs[5].default_value = 2.0
    #Distortion
    noise_texture_003.inputs[8].default_value = 0.0

    #node Bump
    bump = birch_tree_bark.nodes.new("ShaderNodeBump")
    bump.name = "Bump"
    bump.invert = False
    #Strength
    bump.inputs[0].default_value = 0.5666666626930237
    #Distance
    bump.inputs[1].default_value = 1.0
    #Normal
    bump.inputs[3].default_value = (0.0, 0.0, 0.0)

    #node Bump.001
    bump_001 = birch_tree_bark.nodes.new("ShaderNodeBump")
    bump_001.name = "Bump.001"
    bump_001.invert = False
    #Strength
    bump_001.inputs[0].default_value = 0.38333332538604736
    #Distance
    bump_001.inputs[1].default_value = 1.0

    #node Noise Texture.002
    noise_texture_002 = birch_tree_bark.nodes.new("ShaderNodeTexNoise")
    noise_texture_002.name = "Noise Texture.002"
    noise_texture_002.noise_dimensions = '3D'
    noise_texture_002.noise_type = 'FBM'
    noise_texture_002.normalize = True
    #Scale
    noise_texture_002.inputs[2].default_value = 40.0
    #Detail
    noise_texture_002.inputs[3].default_value = 15.0
    #Roughness
    noise_texture_002.inputs[4].default_value = 0.6499999761581421
    #Lacunarity
    noise_texture_002.inputs[5].default_value = 2.0
    #Distortion
    noise_texture_002.inputs[8].default_value = 0.30000001192092896

    #node ColorRamp.003
    colorramp_003 = birch_tree_bark.nodes.new("ShaderNodeValToRGB")
    colorramp_003.name = "ColorRamp.003"
    colorramp_003.color_ramp.color_mode = 'RGB'
    colorramp_003.color_ramp.hue_interpolation = 'NEAR'
    colorramp_003.color_ramp.interpolation = 'LINEAR'

    #initialize color ramp elements
    colorramp_003.color_ramp.elements.remove(colorramp_003.color_ramp.elements[0])
    colorramp_003_cre_0 = colorramp_003.color_ramp.elements[0]
    colorramp_003_cre_0.position = 0.5772725343704224
    colorramp_003_cre_0.alpha = 1.0
    colorramp_003_cre_0.color = (0.0, 0.0, 0.0, 1.0)

    colorramp_003_cre_1 = colorramp_003.color_ramp.elements.new(0.650000274181366)
    colorramp_003_cre_1.alpha = 1.0
    colorramp_003_cre_1.color = (1.0, 1.0, 1.0, 1.0)


    #node Bump.002
    bump_002 = birch_tree_bark.nodes.new("ShaderNodeBump")
    bump_002.name = "Bump.002"
    bump_002.invert = False
    #Strength
    bump_002.inputs[0].default_value = 0.5666666626930237
    #Distance
    bump_002.inputs[1].default_value = 1.0

    #node Material Output
    material_output = birch_tree_bark.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    #Thickness
    material_output.inputs[3].default_value = 0.0

    #node Displacement
    displacement = birch_tree_bark.nodes.new("ShaderNodeDisplacement")
    displacement.name = "Displacement"
    displacement.space = 'OBJECT'
    #Midlevel
    displacement.inputs[1].default_value = 0.5
    #Scale
    displacement.inputs[2].default_value = 0.20000000298023224
    #Normal
    displacement.inputs[3].default_value = (0.0, 0.0, 0.0)

    #node Principled BSDF
    principled_bsdf = birch_tree_bark.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK_SKIN'
    #Metallic
    principled_bsdf.inputs[1].default_value = 0.0
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
    #Subsurface IOR
    principled_bsdf.inputs[11].default_value = 1.399999976158142
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
    principled_bsdf.inputs[27].default_value = (0.0, 0.0, 0.0, 1.0)
    #Emission Strength
    principled_bsdf.inputs[28].default_value = 1.0
    #Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    #Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    #node Mapping
    mapping = birch_tree_bark.nodes.new("ShaderNodeMapping")
    mapping.name = "Mapping"
    mapping.vector_type = 'POINT'
    #Location
    mapping.inputs[1].default_value = (0.0, 0.0, 0.0)
    #Rotation
    mapping.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    mapping.inputs[3].default_value = (1.0, 1.0, 0.20000000298023224)

    #node ColorRamp.002
    colorramp_002 = birch_tree_bark.nodes.new("ShaderNodeValToRGB")
    colorramp_002.name = "ColorRamp.002"
    colorramp_002.color_ramp.color_mode = 'RGB'
    colorramp_002.color_ramp.hue_interpolation = 'NEAR'
    colorramp_002.color_ramp.interpolation = 'LINEAR'

    #initialize color ramp elements
    colorramp_002.color_ramp.elements.remove(colorramp_002.color_ramp.elements[0])
    colorramp_002_cre_0 = colorramp_002.color_ramp.elements[0]
    colorramp_002_cre_0.position = 0.0
    colorramp_002_cre_0.alpha = 1.0
    colorramp_002_cre_0.color = (0.4780173897743225, 0.4780173897743225, 0.4780173897743225, 1.0)

    colorramp_002_cre_1 = colorramp_002.color_ramp.elements.new(1.0)
    colorramp_002_cre_1.alpha = 1.0
    colorramp_002_cre_1.color = (0.8509905338287354, 0.8509905338287354, 0.8509905338287354, 1.0)


    #node Noise Texture.004
    noise_texture_004 = birch_tree_bark.nodes.new("ShaderNodeTexNoise")
    noise_texture_004.name = "Noise Texture.004"
    noise_texture_004.noise_dimensions = '3D'
    noise_texture_004.noise_type = 'FBM'
    noise_texture_004.normalize = True
    #Scale
    noise_texture_004.inputs[2].default_value = 5.0
    #Detail
    noise_texture_004.inputs[3].default_value = 2.0
    #Roughness
    noise_texture_004.inputs[4].default_value = 0.5
    #Lacunarity
    noise_texture_004.inputs[5].default_value = 2.0
    #Distortion
    noise_texture_004.inputs[8].default_value = 0.0

    #node ColorRamp.004
    colorramp_004 = birch_tree_bark.nodes.new("ShaderNodeValToRGB")
    colorramp_004.name = "ColorRamp.004"
    colorramp_004.color_ramp.color_mode = 'RGB'
    colorramp_004.color_ramp.hue_interpolation = 'NEAR'
    colorramp_004.color_ramp.interpolation = 'LINEAR'

    #initialize color ramp elements
    colorramp_004.color_ramp.elements.remove(colorramp_004.color_ramp.elements[0])
    colorramp_004_cre_0 = colorramp_004.color_ramp.elements[0]
    colorramp_004_cre_0.position = 0.5409091114997864
    colorramp_004_cre_0.alpha = 1.0
    colorramp_004_cre_0.color = (0.0, 0.0, 0.0, 1.0)

    colorramp_004_cre_1 = colorramp_004.color_ramp.elements.new(1.0)
    colorramp_004_cre_1.alpha = 1.0
    colorramp_004_cre_1.color = (1.0, 1.0, 1.0, 1.0)


    #node Mix.001
    mix_001 = birch_tree_bark.nodes.new("ShaderNodeMix")
    mix_001.name = "Mix.001"
    mix_001.blend_type = 'MIX'
    mix_001.clamp_factor = True
    mix_001.clamp_result = False
    mix_001.data_type = 'RGBA'
    mix_001.factor_mode = 'UNIFORM'
    #B_Color
    mix_001.inputs[7].default_value = (0.0012143913190811872, 0.0019650054164230824, 0.0007245307206176221, 1.0)

    #node Texture Coordinate
    texture_coordinate = birch_tree_bark.nodes.new("ShaderNodeTexCoord")
    texture_coordinate.name = "Texture Coordinate"
    texture_coordinate.from_instancer = False

    #node Noise Texture
    noise_texture = birch_tree_bark.nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.noise_dimensions = '3D'
    noise_texture.noise_type = 'FBM'
    noise_texture.normalize = True
    #Scale
    noise_texture.inputs[2].default_value = 2.0
    #Detail
    noise_texture.inputs[3].default_value = 15.0
    #Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    #Distortion
    noise_texture.inputs[8].default_value = 0.20000000298023224

    #node Mapping.002
    mapping_002 = birch_tree_bark.nodes.new("ShaderNodeMapping")
    mapping_002.name = "Mapping.002"
    mapping_002.vector_type = 'POINT'
    #Location
    mapping_002.inputs[1].default_value = (0.0, 0.0, 0.0)
    #Rotation
    mapping_002.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    mapping_002.inputs[3].default_value = (0.800000011920929, 0.800000011920929, 7.299999713897705)

    #node Noise Texture.001
    noise_texture_001 = birch_tree_bark.nodes.new("ShaderNodeTexNoise")
    noise_texture_001.name = "Noise Texture.001"
    noise_texture_001.noise_dimensions = '3D'
    noise_texture_001.noise_type = 'FBM'
    noise_texture_001.normalize = True
    #Scale
    noise_texture_001.inputs[2].default_value = 3.0
    #Detail
    noise_texture_001.inputs[3].default_value = 15.0
    #Roughness
    noise_texture_001.inputs[4].default_value = 0.5916666984558105
    #Lacunarity
    noise_texture_001.inputs[5].default_value = 2.0
    #Distortion
    noise_texture_001.inputs[8].default_value = 0.0

    #node Mapping.001
    mapping_001 = birch_tree_bark.nodes.new("ShaderNodeMapping")
    mapping_001.name = "Mapping.001"
    mapping_001.vector_type = 'POINT'
    #Location
    mapping_001.inputs[1].default_value = (0.0, 0.0, 0.0)
    #Rotation
    mapping_001.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    mapping_001.inputs[3].default_value = (1.0, 1.0, 6.0)

    #node Voronoi Texture
    voronoi_texture = birch_tree_bark.nodes.new("ShaderNodeTexVoronoi")
    voronoi_texture.name = "Voronoi Texture"
    voronoi_texture.distance = 'CHEBYCHEV'
    voronoi_texture.feature = 'F1'
    voronoi_texture.normalize = False
    voronoi_texture.voronoi_dimensions = '3D'
    #Scale
    voronoi_texture.inputs[2].default_value = 1.0
    #Detail
    voronoi_texture.inputs[3].default_value = 0.0
    #Roughness
    voronoi_texture.inputs[4].default_value = 0.5
    #Lacunarity
    voronoi_texture.inputs[5].default_value = 2.0
    #Randomness
    voronoi_texture.inputs[8].default_value = 1.0

    #node ColorRamp.001
    colorramp_001 = birch_tree_bark.nodes.new("ShaderNodeValToRGB")
    colorramp_001.name = "ColorRamp.001"
    colorramp_001.color_ramp.color_mode = 'RGB'
    colorramp_001.color_ramp.hue_interpolation = 'NEAR'
    colorramp_001.color_ramp.interpolation = 'LINEAR'

    #initialize color ramp elements
    colorramp_001.color_ramp.elements.remove(colorramp_001.color_ramp.elements[0])
    colorramp_001_cre_0 = colorramp_001.color_ramp.elements[0]
    colorramp_001_cre_0.position = 0.0
    colorramp_001_cre_0.alpha = 1.0
    colorramp_001_cre_0.color = (0.008580949157476425, 0.008580949157476425, 0.008580949157476425, 1.0)

    colorramp_001_cre_1 = colorramp_001.color_ramp.elements.new(0.3909090459346771)
    colorramp_001_cre_1.alpha = 1.0
    colorramp_001_cre_1.color = (0.9527517557144165, 0.9527517557144165, 0.9527517557144165, 1.0)

    colorramp_001_cre_2 = colorramp_001.color_ramp.elements.new(0.49090898036956787)
    colorramp_001_cre_2.alpha = 1.0
    colorramp_001_cre_2.color = (0.008580949157476425, 0.008580949157476425, 0.008580949157476425, 1.0)


    #node ColorRamp
    colorramp = birch_tree_bark.nodes.new("ShaderNodeValToRGB")
    colorramp.name = "ColorRamp"
    colorramp.color_ramp.color_mode = 'RGB'
    colorramp.color_ramp.hue_interpolation = 'NEAR'
    colorramp.color_ramp.interpolation = 'LINEAR'

    #initialize color ramp elements
    colorramp.color_ramp.elements.remove(colorramp.color_ramp.elements[0])
    colorramp_cre_0 = colorramp.color_ramp.elements[0]
    colorramp_cre_0.position = 0.42272698879241943
    colorramp_cre_0.alpha = 1.0
    colorramp_cre_0.color = (0.00435684435069561, 0.00435684435069561, 0.00435684435069561, 1.0)

    colorramp_cre_1 = colorramp.color_ramp.elements.new(0.6409092545509338)
    colorramp_cre_1.alpha = 1.0
    colorramp_cre_1.color = (0.812196671962738, 0.812196671962738, 0.812196671962738, 1.0)


    #node Mix
    mix = birch_tree_bark.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'LINEAR_LIGHT'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    #Factor_Float
    mix.inputs[0].default_value = 0.1133333295583725

    #node Clamp
    clamp = birch_tree_bark.nodes.new("ShaderNodeClamp")
    clamp.name = "Clamp"
    clamp.hide = True
    clamp.clamp_type = 'MINMAX'
    #Min
    clamp.inputs[1].default_value = 0.0
    #Max
    clamp.inputs[2].default_value = 1.0


    #Set locations
    noise_texture_003.location = (-267.8474426269531, -420.8607482910156)
    bump.location = (320.62017822265625, -199.8921661376953)
    bump_001.location = (525.1470336914062, -332.1177978515625)
    noise_texture_002.location = (-969.1334228515625, 688.85400390625)
    colorramp_003.location = (-742.66552734375, 681.3453369140625)
    bump_002.location = (977.3782348632812, -182.11727905273438)
    material_output.location = (2108.162109375, 330.31463623046875)
    displacement.location = (1505.4908447265625, -537.0250854492188)
    principled_bsdf.location = (1402.5858154296875, 312.6984558105469)
    mapping.location = (-1003.658203125, 124.3302230834961)
    colorramp_002.location = (760.3242797851562, 182.3679656982422)
    noise_texture_004.location = (-808.5922241210938, 162.93765258789062)
    colorramp_004.location = (-577.214111328125, 147.37506103515625)
    mix_001.location = (831.5877075195312, 609.7543334960938)
    texture_coordinate.location = (-2482.420654296875, 68.03762817382812)
    noise_texture.location = (-1355.470458984375, -98.5422134399414)
    mapping_002.location = (-1707.496337890625, 229.39263916015625)
    noise_texture_001.location = (-1921.0780029296875, -228.92750549316406)
    mapping_001.location = (-1205.7213134765625, 683.43505859375)
    voronoi_texture.location = (-54.99856185913086, 109.7565689086914)
    colorramp_001.location = (345.6084289550781, 388.8555908203125)
    colorramp.location = (-1651.1910400390625, -300.04400634765625)
    mix.location = (-1190.16845703125, 128.5996856689453)
    clamp.location = (-1355.470458984375, -398.5422058105469)

    #Set dimensions
    noise_texture_003.width, noise_texture_003.height = 140.0, 100.0
    bump.width, bump.height = 140.0, 100.0
    bump_001.width, bump_001.height = 140.0, 100.0
    noise_texture_002.width, noise_texture_002.height = 140.0, 100.0
    colorramp_003.width, colorramp_003.height = 240.0, 100.0
    bump_002.width, bump_002.height = 140.0, 100.0
    material_output.width, material_output.height = 140.0, 100.0
    displacement.width, displacement.height = 140.0, 100.0
    principled_bsdf.width, principled_bsdf.height = 240.0, 100.0
    mapping.width, mapping.height = 171.6392822265625, 100.0
    colorramp_002.width, colorramp_002.height = 240.0, 100.0
    noise_texture_004.width, noise_texture_004.height = 140.0, 100.0
    colorramp_004.width, colorramp_004.height = 240.0, 100.0
    mix_001.width, mix_001.height = 140.0, 100.0
    texture_coordinate.width, texture_coordinate.height = 140.0, 100.0
    noise_texture.width, noise_texture.height = 140.0, 100.0
    mapping_002.width, mapping_002.height = 140.0, 100.0
    noise_texture_001.width, noise_texture_001.height = 140.0, 100.0
    mapping_001.width, mapping_001.height = 140.0, 100.0
    voronoi_texture.width, voronoi_texture.height = 140.0, 100.0
    colorramp_001.width, colorramp_001.height = 240.0, 100.0
    colorramp.width, colorramp.height = 240.0, 100.0
    mix.width, mix.height = 140.0, 100.0
    clamp.width, clamp.height = 140.0, 100.0

    #initialize birch_tree_bark links
    #noise_texture.Color -> mix.A
    birch_tree_bark.links.new(noise_texture.outputs[1], mix.inputs[2])
    #mapping_002.Vector -> mix.A
    birch_tree_bark.links.new(mapping_002.outputs[0], mix.inputs[6])
    #noise_texture.Color -> mix.B
    birch_tree_bark.links.new(noise_texture.outputs[1], mix.inputs[7])
    #mix.Result -> mapping.Vector
    birch_tree_bark.links.new(mix.outputs[2], mapping.inputs[0])
    #noise_texture_001.Color -> colorramp.Fac
    birch_tree_bark.links.new(noise_texture_001.outputs[1], colorramp.inputs[0])
    #voronoi_texture.Distance -> colorramp_001.Fac
    birch_tree_bark.links.new(voronoi_texture.outputs[0], colorramp_001.inputs[0])
    #colorramp_002.Color -> principled_bsdf.Roughness
    birch_tree_bark.links.new(colorramp_002.outputs[0], principled_bsdf.inputs[2])
    #voronoi_texture.Distance -> colorramp_002.Fac
    birch_tree_bark.links.new(voronoi_texture.outputs[0], colorramp_002.inputs[0])
    #mapping_001.Vector -> noise_texture_002.Vector
    birch_tree_bark.links.new(mapping_001.outputs[0], noise_texture_002.inputs[0])
    #noise_texture_002.Fac -> colorramp_003.Fac
    birch_tree_bark.links.new(noise_texture_002.outputs[0], colorramp_003.inputs[0])
    #colorramp_003.Color -> mix_001.A
    birch_tree_bark.links.new(colorramp_003.outputs[0], mix_001.inputs[2])
    #colorramp_001.Color -> mix_001.B
    birch_tree_bark.links.new(colorramp_001.outputs[0], mix_001.inputs[3])
    #colorramp_003.Color -> mix_001.Factor
    birch_tree_bark.links.new(colorramp_003.outputs[0], mix_001.inputs[0])
    #colorramp_001.Color -> mix_001.A
    birch_tree_bark.links.new(colorramp_001.outputs[0], mix_001.inputs[6])
    #voronoi_texture.Distance -> bump.Height
    birch_tree_bark.links.new(voronoi_texture.outputs[0], bump.inputs[2])
    #texture_coordinate.Object -> noise_texture_003.Vector
    birch_tree_bark.links.new(texture_coordinate.outputs[3], noise_texture_003.inputs[0])
    #bump.Normal -> bump_001.Normal
    birch_tree_bark.links.new(bump.outputs[0], bump_001.inputs[3])
    #noise_texture_003.Fac -> bump_001.Height
    birch_tree_bark.links.new(noise_texture_003.outputs[0], bump_001.inputs[2])
    #bump_001.Normal -> bump_002.Normal
    birch_tree_bark.links.new(bump_001.outputs[0], bump_002.inputs[3])
    #colorramp_003.Color -> bump_002.Height
    birch_tree_bark.links.new(colorramp_003.outputs[0], bump_002.inputs[2])
    #displacement.Displacement -> material_output.Displacement
    birch_tree_bark.links.new(displacement.outputs[0], material_output.inputs[2])
    #bump_002.Normal -> principled_bsdf.Normal
    birch_tree_bark.links.new(bump_002.outputs[0], principled_bsdf.inputs[5])
    #texture_coordinate.Object -> mapping_001.Vector
    birch_tree_bark.links.new(texture_coordinate.outputs[3], mapping_001.inputs[0])
    #principled_bsdf.BSDF -> material_output.Surface
    birch_tree_bark.links.new(principled_bsdf.outputs[0], material_output.inputs[0])
    #voronoi_texture.Distance -> displacement.Height
    birch_tree_bark.links.new(voronoi_texture.outputs[0], displacement.inputs[0])
    #mapping.Vector -> noise_texture_004.Vector
    birch_tree_bark.links.new(mapping.outputs[0], noise_texture_004.inputs[0])
    #noise_texture_004.Color -> colorramp_004.Fac
    birch_tree_bark.links.new(noise_texture_004.outputs[1], colorramp_004.inputs[0])
    #colorramp_004.Color -> voronoi_texture.Vector
    birch_tree_bark.links.new(colorramp_004.outputs[0], voronoi_texture.inputs[0])
    #mix_001.Result -> principled_bsdf.Base Color
    birch_tree_bark.links.new(mix_001.outputs[2], principled_bsdf.inputs[0])
    #texture_coordinate.Object -> mapping_002.Vector
    birch_tree_bark.links.new(texture_coordinate.outputs[3], mapping_002.inputs[0])
    #mapping_002.Vector -> noise_texture.Vector
    birch_tree_bark.links.new(mapping_002.outputs[0], noise_texture.inputs[0])
    #mapping_002.Vector -> noise_texture_001.Vector
    birch_tree_bark.links.new(mapping_002.outputs[0], noise_texture_001.inputs[0])
    #colorramp.Color -> clamp.Value
    birch_tree_bark.links.new(colorramp.outputs[0], clamp.inputs[0])
    #clamp.Result -> noise_texture.Roughness
    birch_tree_bark.links.new(clamp.outputs[0], noise_texture.inputs[4])

    
    if obj.data.materials:
        obj.data.materials[0] = mat  # Replace existing material
    else:
        obj.data.materials.append(mat)  # Add new material
    

