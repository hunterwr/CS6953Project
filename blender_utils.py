import bpy

def clear_scene():
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

    current_mode = bpy.context.object.mode

    if current_mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.mode_set(mode='OBJECT')

    for obj in bpy.data.objects:
        # Collect all Geometry Nodes modifiers
        geo_modifiers = [mod for mod in obj.modifiers if mod.type == 'NODES']

        # Remove each Geometry Nodes modifier from the object
        for mod in geo_modifiers:
            obj.modifiers.remove(mod)
            
    for node_group in bpy.data.node_groups:
        if node_group.bl_idname == 'GeometryNodeTree':
            bpy.data.node_groups.remove(node_group)
            
    # Delete all objects (mesh and non-mesh)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Clear all materials from the Blender file
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)

    # Clear all mesh data from the Blender file
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)

    # Clear all other data blocks (like textures, images, etc.)
    for texture in bpy.data.textures:
        bpy.data.textures.remove(texture)

    for image in bpy.data.images:
        bpy.data.images.remove(image)


        
    for curves in bpy.data.curves:
        bpy.data.curves.remove(curves)


def wipe_blender():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    

def apply_blenderkit_material(obj_name, asset_base_id, keyword):
    obj = bpy.data.objects.get(obj_name)
    if obj:
        # Download and apply material using asset_base_id
        bpy.ops.view3d.blenderkit_disclaimer_widget(message="Use the 'S' key over the asset bar to search similar assets.", url="https://github.com/BlenderKit/blenderkit/wiki/BlenderKit-add-on-documentation#assetbar", fadeout_time=8, tip=True)
        bpy.data.window_managers["WinMan"].blenderkitUI.asset_type = 'MATERIAL'
        bpy.data.window_managers["WinMan"].blenderkit_mat.search_keywords = keyword
        bpy.ops.scene.blenderkit_download(asset_index=0, target_object=obj_name, material_target_slot=0, model_rotation=(0, 0, 0))
        bpy.ops.view3d.blenderkit_download_gizmo_widget(asset_base_id=asset_base_id)


        print(f"BlenderKit material {asset_base_id} applied to {obj_name}.")
    else:
        print(f"Object '{obj_name}' not found!")
    