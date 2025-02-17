import bpy

import sys
import os

script_name = bpy.context.space_data.text.name

# Get the absolute path of the script
script_filepath = bpy.data.texts[script_name].filepath

script_directory = os.path.dirname(script_filepath)


#### CHANGE TARGET DIRECTORY TO SHARED FOLDER LOCATION######
target_directory = script_directory
os.chdir(target_directory)

sys.path.append(os.getcwd())
import blender_utils as utils



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


    add_leaf_material(leaves_obj.name, target_directory + r'./textures\\Trees\\birch_leaf.png')
    utils.apply_blenderkit_material(name, "e6075cd1-22ef-471e-a6b3-5a65aab646fa", "birch bark")


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


    add_leaf_material(leaves_obj.name, target_directory + r'./textures\\Trees\\fir_branch.png')
    add_bark_material(tree_obj.name, target_directory + r'./textures\\Trees\\Bark014_8K-JPG\\Bark014_8K-JPG_Color.jpg')


        
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


def create_birch_tree(position=(0, 0, 0), height=6, trunk_thickness=0.1):
    """
    Creates a birch tree.

    :param position: Tuple of (x, y, z) coordinates for the tree's position.
    :param height: Height of the tree.
    :param trunk_thickness: Thickness of the tree trunk.
    """
    pass

def create_custom_tree(position=(0, 0, 0), trunk_height=5, canopy_shape="sphere", canopy_size=3):
    """
    Creates a custom tree with specified parameters.

    :param position: Tuple of (x, y, z) coordinates for the tree's position.
    :param trunk_height: Height of the tree trunk.
    :param canopy_shape: Shape of the canopy (e.g., "sphere", "cone").
    :param canopy_size: Size of the canopy.
    """
    pass

def create_forest(tree_count=100, area_size=(50, 50)):
    """
    Creates a forest by randomly distributing trees within a specified area.

    :param tree_count: Number of trees to generate.
    :param area_size: Tuple of (width, depth) for the forest area.
    """
    pass

def add_grass(position=(0, 0, 0), area_size=(10, 10), density=100):
    """
    Adds grass to the scene.

    :param position: Tuple of (x, y, z) coordinates for the center of the grass area.
    :param area_size: Tuple of (width, depth) for the grass area.
    :param density: Number of grass blades per unit area.

    Note: Consider using the BlenderKit library or Grass Essentials for realistic grass assets.
    """
    pass

def add_foliage(position=(0, 0, 0), area_size=(10, 10), density=50):
    """
    Adds foliage to the scene, such as shrubs and small plants.

    :param position: Tuple of (x, y, z) coordinates for the center of the foliage area.
    :param area_size: Tuple of (width, depth) for the foliage area.
    :param density: Number of foliage instances per unit area.

    Note: Botaniq or Quixel Megascans can be referenced for high-quality foliage assets.
    """
    pass

def add_trees(tree_type="oak", count=10, area_size=(20, 20)):
    """
    Adds multiple trees of a specified type to the scene.

    :param tree_type: Type of tree to add (e.g., "oak", "pine", "birch").
    :param count: Number of trees to add.
    :param area_size: Tuple of (width, depth) for the tree distribution area.

    Note: The Grove 3D or Modular Tree Add-on could be used for hyper-realistic tree generation.
    """
    pass



#create_birch_tree('tree12', target_directory)

# BlenderKit material ID (replace with actual material ID)
material_id = "e6075cd1-22ef-471e-a6b3-5a65aab646fa"

# Object to apply material to
object_name = "Cube"  # Change this to your object's name

# Download and apply BlenderKit material using the ID
bpy.ops.asset_bundle.download(asset_type='MATERIAL', asset_id=material_id)

# Function to find and apply the material once downloaded
def apply_downloaded_material(obj_name, material_id):
    obj = bpy.data.objects.get(obj_name)
    if obj is None:
        print(f"Object '{obj_name}' not found.")
        return
    
    # Wait for the material to appear in Blender's materials list
    for mat in bpy.data.materials:
        if material_id in mat.get("asset_data", {}).get("id", ""):
            if obj.data.materials:
                obj.data.materials[0] = mat  # Replace first material
            else:
                obj.data.materials.append(mat)  # Assign new material
            print(f"Applied material '{mat.name}' to '{obj_name}'")
            return
    
    print(f"Material with ID '{material_id}' not found in materials list.")

# Apply material after download
apply_downloaded_material(object_name, material_id)