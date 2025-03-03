import bpy

import sys
import os
import random
from mathutils import Vector
import texture_utils as textures 


def create_birch_tree(name, target_directory, position=(0, 0, 0), height=7, trunk_radius=0.2, seed=0):
    """
    Creates a pine tree.

    :param position: Tuple of (x, y, z) coordinates for the tree's position.
    :param height: Height of the tree.
    :param trunk_radius: Radius of the tree trunk.
    """
    bpy.ops.curve.tree_add(
        do_update=True, 
        chooseSet='5', 
        bevel=True, 
        prune=False, 
        showLeaves=True, 
        useArm=False, 
        seed=seed, 
        handleType='0', 
        levels=4, 
        length=(1, 0.2, 0.55, 0.45), 
        lengthV=(0, 0.1, 0.25, 0.25), 
        taperCrown=0, 
        branches=(0, 75, 16, 10), 
        curveRes=(12, 4, 3, 2), 
        curve=(0, 20, -10, 0), 
        curveV=(40, 30, 15, 10), 
        curveBack=(0, 0, 0, 0), 
        baseSplits=0, 
        segSplits=(0, 0.35, 0.6, 0), 
        splitByLen=True, 
        rMode='rotate', 
        splitAngle=(0, 12, 18, 0), 
        splitAngleV=(0, 0, 0, 0), 
        scale=35, 
        scaleV=15, 
        attractUp=(0, 0.35, 0.25, 0.15), 
        attractOut=(0, 0, 0, 0), 
        shape='8', 
        shapeS='7', 
        customShape=(0.5, 1, 0.35, 0.1), 
        branchDist=1.85, 
        nrings=0, 
        baseSize=0.33, 
        baseSize_s=0.5, 
        splitHeight=0.2, 
        splitBias=0, 
        ratio=0.015, 
        minRadius=0.002, 
        closeTip=True, 
        rootFlare=1.3, 
        autoTaper=True, 
        taper=(1, 1, 1, 1), 
        radiusTweak=(1, 1, 1, 1), 
        ratioPower=1.2, 
        downAngle=(90, 130, 45, 45), 
        downAngleV=(0, 30, 10, 10), 
        useOldDownAngle=False, 
        useParentAngle=True, 
        rotate=(99.5, 137.5, -45, -60), 
        rotateV=(15, 0, 15, 45), 
        scale0=1, 
        scaleV0=0.1, 
        pruneWidth=0.4, 
        pruneBase=0.3, 
        pruneWidthPeak=0.6, 
        prunePowerHigh=0.5, 
        prunePowerLow=0.001, 
        pruneRatio=1, 
        leaves=20, 
        leafDownAngle=45, 
        leafDownAngleV=10, 
        leafRotate=137.5, 
        leafRotateV=0, 
        leafScale=1, 
        leafScaleX=1, 
        leafScaleT=0, 
        leafScaleV=0, 
        leafShape='rect', 
        bend=0, 
        leafangle=0, 
        horzLeaves=True, 
        leafDist='6', 
        bevelRes=1, 
        resU=4, 
        armAnim=False, 
        previewArm=False, 
        leafAnim=False, 
        frameRate=1, 
        loopFrames=0, 
        wind=1, 
        gust=1, 
        gustF=0.075, 
        af1=1, 
        af2=1, 
        af3=4, 
        makeMesh=False, 
        armLevels=2, 
        boneStep=(1, 1, 1, 1))
    
    bpy.data.objects["tree"].name = name
    
    select_object(name)
    move_selected_object(position)
    
    # selecet the leaves
    # Deselect everything first
    bpy.ops.object.select_all(action='DESELECT')

    # Get the new tree object
    tree_obj = bpy.data.objects.get(name)

    if tree_obj:
        # Iterate through all objects and find the child named "leaves"
        leaves_obj = None
        for obj in bpy.data.objects:
            if obj.parent == tree_obj and obj.name == "leaves":
                leaves_obj = obj
                leaves_obj.name = name + "_leaves"  # Rename the leaves object
                break

        # Select and activate the leaves if found
        if leaves_obj:
            bpy.ops.object.select_all(action='DESELECT')  # Deselect everything
            leaves_obj.select_set(True)  # Select leaves
            bpy.context.view_layer.objects.active = leaves_obj  # Set as active
            print("Leaves object found and selected!")
        else:
            print("Leaves object not found under 'tree1'.")
    else:
        print("Tree1 object not found.")


    add_leaf_material(leaves_obj.name, target_directory + r'/textures/Trees/birch_leaf.png')
    textures.apply_birch_tree_bark(tree_obj)


def create_pine_tree(name, target_directory, position=(0, 0, 0), height=7, trunk_radius=0.2, seed=0):
    """
    Creates a pine tree.

    :param position: Tuple of (x, y, z) coordinates for the tree's position.
    :param height: Height of the tree.
    :param trunk_radius: Radius of the tree trunk.
    """
    bpy.ops.curve.tree_add(
        do_update=True, 
        chooseSet='5', 
        bevel=True, 
        prune=False, 
        showLeaves=True, 
        useArm=False, 
        seed=seed, 
        handleType='0', 
        levels=4, 
        length=(1, 0.2, 0.55, 0.45), 
        lengthV=(0, 0.1, 0.25, 0.25), 
        taperCrown=0, 
        branches=(0, 75, 16, 10), 
        curveRes=(12, 4, 3, 2), 
        curve=(0, 20, -10, 0), 
        curveV=(40, 30, 15, 10), 
        curveBack=(0, 0, 0, 0), 
        baseSplits=0, 
        segSplits=(0, 0.35, 0.6, 0), 
        splitByLen=True, 
        rMode='rotate', 
        splitAngle=(0, 12, 18, 0), 
        splitAngleV=(0, 0, 0, 0), 
        scale=35, 
        scaleV=15, 
        attractUp=(0, 0.35, 0.25, 0.15), 
        attractOut=(0, 0, 0, 0), 
        shape='8', 
        shapeS='7', 
        customShape=(0.5, 1, 0.35, 0.1), 
        branchDist=1.85, 
        nrings=0, 
        baseSize=0.33, 
        baseSize_s=0.5, 
        splitHeight=0.2, 
        splitBias=0, 
        ratio=0.015, 
        minRadius=0.002, 
        closeTip=True, 
        rootFlare=1.3, 
        autoTaper=True, 
        taper=(1, 1, 1, 1), 
        radiusTweak=(1, 1, 1, 1), 
        ratioPower=1.2, 
        downAngle=(90, 130, 45, 45), 
        downAngleV=(0, 30, 10, 10), 
        useOldDownAngle=False, 
        useParentAngle=True, 
        rotate=(99.5, 137.5, -45, -60), 
        rotateV=(15, 0, 15, 45), 
        scale0=1, 
        scaleV0=0.1, 
        pruneWidth=0.4, 
        pruneBase=0.3, 
        pruneWidthPeak=0.6, 
        prunePowerHigh=0.5, 
        prunePowerLow=0.001, 
        pruneRatio=1, 
        leaves=20, 
        leafDownAngle=45, 
        leafDownAngleV=10, 
        leafRotate=137.5, 
        leafRotateV=0, 
        leafScale=1, 
        leafScaleX=1, 
        leafScaleT=0, 
        leafScaleV=0, 
        leafShape='rect', 
        bend=0, 
        leafangle=0, 
        horzLeaves=True, 
        leafDist='6', 
        bevelRes=1, 
        resU=4, 
        armAnim=False, 
        previewArm=False, 
        leafAnim=False, 
        frameRate=1, 
        loopFrames=0, 
        wind=1, 
        gust=1, 
        gustF=0.075, 
        af1=1, 
        af2=1, 
        af3=4, 
        makeMesh=False, 
        armLevels=2, 
        boneStep=(1, 1, 1, 1))
    
    bpy.data.objects["tree"].name = name
    
    select_object(name)
    move_selected_object(position)
    
    # selecet the leaves
    # Deselect everything first
    bpy.ops.object.select_all(action='DESELECT')

    # Get the new tree object
    tree_obj = bpy.data.objects.get(name)

    if tree_obj:
        # Iterate through all objects and find the child named "leaves"
        leaves_obj = None
        for obj in bpy.data.objects:
            if obj.parent == tree_obj and obj.name == "leaves":
                leaves_obj = obj
                leaves_obj.name = name + "_leaves"  # Rename the leaves object
                break

        # Select and activate the leaves if found
        if leaves_obj:
            bpy.ops.object.select_all(action='DESELECT')  # Deselect everything
            leaves_obj.select_set(True)  # Select leaves
            bpy.context.view_layer.objects.active = leaves_obj  # Set as active
            print("Leaves object found and selected!")
        else:
            print("Leaves object not found under 'tree1'.")
    else:
        print("Tree1 object not found.")


    add_leaf_material(leaves_obj.name, target_directory + r'/textures/Trees/fir_branch.png')
    add_bark_material(tree_obj.name, target_directory + r'/textures/Trees/Bark014_8K-JPG/Bark014_8K-JPG_Color.jpg')


        
def add_leaf_material(leaves_obj_name, image_path):
    leaves_obj = bpy.data.objects.get(leaves_obj_name)
    if not leaves_obj:
        print(f"Object '{leaves_obj_name}' not found!")
        return

    mat = bpy.data.materials.get("LeafMaterial")
    if not mat:
        mat = bpy.data.materials.new(name="LeafMaterial")
    mat.use_nodes = True

    if leaves_obj.data.materials:
        leaves_obj.data.materials[0] = mat
    else:
        leaves_obj.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    for node in nodes:
        nodes.remove(node)

    principled = nodes.new(type="ShaderNodeBsdfPrincipled")
    principled.location = (0, 0)

    texture_node = nodes.new(type="ShaderNodeTexImage")
    texture_node.location = (-300, 0)
    texture_node.image = bpy.data.images.load(image_path)

    output = nodes.new(type="ShaderNodeOutputMaterial")
    output.location = (200, 0)

    links.new(texture_node.outputs["Color"], principled.inputs["Base Color"])
    links.new(principled.outputs["BSDF"], output.inputs["Surface"])
    links.new(texture_node.outputs["Alpha"], principled.inputs["Alpha"])

    mat.blend_method = 'HASHED'
    mat.use_screen_refraction = True
    mat.use_backface_culling = False
    mat.show_transparent_back = False
    mat.alpha_threshold = 0.5

    transparent = nodes.new(type="ShaderNodeBsdfTransparent")
    transparent.location = (-200, -100)

    mix_shader = nodes.new(type="ShaderNodeMixShader")
    mix_shader.location = (50, -50)

    links.new(transparent.outputs["BSDF"], mix_shader.inputs[1])
    links.new(principled.outputs["BSDF"], mix_shader.inputs[2])
    links.new(texture_node.outputs["Alpha"], mix_shader.inputs[0])
    links.new(mix_shader.outputs["Shader"], output.inputs["Surface"])

    print("Leaves material updated for partial light blocking.")

def add_bark_material(tree_obj_name, bark_texture_path):
    tree_obj = bpy.data.objects.get(tree_obj_name)
    if not tree_obj:
        print(f"{tree_obj_name} object not found!")
        return

    bark_mat = bpy.data.materials.get("BarkMaterial")
    if not bark_mat:
        bark_mat = bpy.data.materials.new(name="BarkMaterial")
    bark_mat.use_nodes = True

    if tree_obj.data.materials:
        tree_obj.data.materials[0] = bark_mat
    else:
        tree_obj.data.materials.append(bark_mat)

    bark_nodes = bark_mat.node_tree.nodes
    bark_links = bark_mat.node_tree.links

    for node in bark_nodes:
        bark_nodes.remove(node)

    bark_principled = bark_nodes.new(type="ShaderNodeBsdfPrincipled")
    bark_principled.location = (0, 0)

    bark_texture_node = bark_nodes.new(type="ShaderNodeTexImage")
    bark_texture_node.location = (-300, 0)
    bark_texture_node.image = bpy.data.images.load(bark_texture_path)

    bark_output = bark_nodes.new(type="ShaderNodeOutputMaterial")
    bark_output.location = (200, 0)

    bark_links.new(bark_texture_node.outputs["Color"], bark_principled.inputs["Base Color"])
    bark_links.new(bark_principled.outputs["BSDF"], bark_output.inputs["Surface"])

    print("Bark material applied to tree!")
        

def move_selected_object(position):
    bpy.ops.transform.translate(value=position, 
    orient_type='GLOBAL', 
    orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
    orient_matrix_type='GLOBAL', mirror=False, 
    use_proportional_edit=False, 
    proportional_edit_falloff='SMOOTH', 
    proportional_size=1, 
    use_proportional_connected=False, 
    use_proportional_projected=False, 
    snap=False, snap_elements={'INCREMENT'}, 
    use_snap_project=False, 
    snap_target='CLOSEST', 
    use_snap_self=True, 
    use_snap_edit=True, 
    use_snap_nonedit=True, 
    use_snap_selectable=False)

def select_object(object_name):
    # Deselect all objects first
    bpy.ops.object.select_all(action='DESELECT')

    # Select the specific object
    if object_name in bpy.data.objects:
        obj = bpy.data.objects[object_name]
        obj.select_set(True)  # Select the object
        bpy.context.view_layer.objects.active = obj  # Set as active object
    else:
        print(f"Object '{object_name}' not found")




def generate_forest(target_directory, road_width, road_length, min_dist=3, max_dist=50, num_trees=10, tree_type='pine'):
    """
    Generates a forest around a road, placing trees only on both sides with varying widths.
    
    road_coords: List of (x, y, width) tuples defining the road path and width at each point.
    tree_density: Probability of placing a tree per unit area.
    """
      # Minimum distance from the road
    for i in range(num_trees):
          # Place trees on both sides of the road
          # Adjust tree count per segment based on width
            tree_x = random.uniform((road_width/2+min_dist), (road_width/2+min_dist)+max_dist) * random.choice([-1, 1])
            tree_y = random.uniform(0, road_length)  # Slight variation in position
            
            # if random.random() < tree_density:
            #     trees.append((tree_x, tree_y))
            tree_name = f'tree{i}'
            if tree_type == 'pine':
                create_pine_tree(tree_name, target_directory, position=(tree_x, tree_y, 0), seed=random.randint(1, 1000))
            elif tree_type == 'birch':
                create_birch_tree(tree_name, target_directory, position=(tree_x, tree_y, 0), seed=random.randint(1, 1000))

    print("Forest generation complete!")
    
    
def generate_preset_forest(target_directory, road_width, road_length, density="some trees", distance_from_road="close", tree_type="pine"):
    if density == "no trees":
        trees = 0
    elif density == "some trees":
        trees = 16
    elif density == "many trees":
        trees = 32
    if distance_from_road == "close":
        min_dist=3
        max_dist=20
    elif distance_from_road == "far":
        min_dist = 15
        max_dist = 60
    generate_forest(target_directory, road_width, road_length, min_dist=min_dist, max_dist=max_dist, num_trees=trees, tree_type=tree_type)

# def test_trees_script():
#     bpy.ops.object.select_all(action='SELECT')

#     # Delete all selected objects
#     bpy.ops.object.delete()

#     # Remove all collections except the default 'Collection'
#     for collection in bpy.data.collections:
#         if collection.name != "Collection":
#             bpy.data.collections.remove(collection)

#     # Remove all materials
#     for material in bpy.data.materials:
#         bpy.data.materials.remove(material)

#     # Remove all meshes
#     for mesh in bpy.data.meshes:
#         bpy.data.meshes.remove(mesh)

#     # Remove all cameras
#     for camera in bpy.data.cameras:
#         bpy.data.cameras.remove(camera)

#     # Remove all lights
#     for light in bpy.data.lights:
#         bpy.data.lights.remove(light)

#     # Remove all curves
#     for curve in bpy.data.curves:
#         bpy.data.curves.remove(curve)

#     # Remove all textures
#     for texture in bpy.data.textures:
#         bpy.data.textures.remove(texture)

#     # Remove all images
#     for image in bpy.data.images:
#         bpy.data.images.remove(image)

#     # Remove all actions (animation data)
#     for action in bpy.data.actions:
#         bpy.data.actions.remove(action)

#     create_birch_tree("tree1", target_directory, position=(0, 0, 0))


# test_trees_script()