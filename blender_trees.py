import bpy

def create_oak_tree(position=(0, 0, 0), height=5, canopy_radius=3):
    """
    Creates an oak tree.

    :param position: Tuple of (x, y, z) coordinates for the tree's position.
    :param height: Height of the tree.
    :param canopy_radius: Radius of the tree's canopy.
    """
    pass

def create_pine_tree(name, position=(0, 0, 0), height=7, trunk_radius=0.2):
    """
    Creates a pine tree.

    :param position: Tuple of (x, y, z) coordinates for the tree's position.
    :param height: Height of the tree.
    :param trunk_radius: Radius of the tree trunk.
    """
    bpy.ops.curve.tree_add(do_update=True, chooseSet='5', bevel=True, prune=False, showLeaves=True, useArm=False, seed=0, handleType='0', levels=4, length=(1, 0.2, 0.55, 0.45), lengthV=(0, 0.1, 0.25, 0.25), taperCrown=0, branches=(0, 75, 16, 10), curveRes=(12, 4, 3, 2), curve=(0, 20, -10, 0), curveV=(40, 30, 15, 10), curveBack=(0, 0, 0, 0), baseSplits=0, segSplits=(0, 0.35, 0.6, 0), splitByLen=True, rMode='rotate', splitAngle=(0, 12, 18, 0), splitAngleV=(0, 0, 0, 0), scale=35, scaleV=15, attractUp=(0, 0.35, 0.25, 0.15), attractOut=(0, 0, 0, 0), shape='8', shapeS='7', customShape=(0.5, 1, 0.35, 0.1), branchDist=1.85, nrings=0, baseSize=0.33, baseSize_s=0.5, splitHeight=0.2, splitBias=0, ratio=0.015, minRadius=0.002, closeTip=True, rootFlare=1.3, autoTaper=True, taper=(1, 1, 1, 1), radiusTweak=(1, 1, 1, 1), ratioPower=1.2, downAngle=(90, 130, 45, 45), downAngleV=(0, 30, 10, 10), useOldDownAngle=False, useParentAngle=True, rotate=(99.5, 137.5, -45, -60), rotateV=(15, 0, 15, 45), scale0=1, scaleV0=0.1, pruneWidth=0.4, pruneBase=0.3, pruneWidthPeak=0.6, prunePowerHigh=0.5, prunePowerLow=0.001, pruneRatio=1, leaves=25, leafDownAngle=45, leafDownAngleV=10, leafRotate=137.5, leafRotateV=0, leafScale=1, leafScaleX=1, leafScaleT=0, leafScaleV=0, leafShape='rect', bend=0, leafangle=0, horzLeaves=True, leafDist='6', bevelRes=1, resU=4, armAnim=False, previewArm=False, leafAnim=False, frameRate=1, loopFrames=0, wind=1, gust=1, gustF=0.075, af1=1, af2=1, af3=4, makeMesh=False, armLevels=2, boneStep=(1, 1, 1, 1))
    
    bpy.data.objects["tree"].name = name
    
    select_object(name)
    move_selected_object(position)
    
    # selecet the leaves
    bpy.ops.material.new()
    bpy.ops.image.open(filepath="C:\\Users\\Hunter Rogers\\Desktop\\Personal\\University of Utah\\DEep cap\\CS6953Project\\assets\\fir_branch_02_by_nellygraceng-d9lcsgk.png", directory="C:\\Users\\Hunter Rogers\\Desktop\\Personal\\University of Utah\\DEep cap\\CS6953Project\\assets\\", files=[{"name":"fir_branch_02_by_nellygraceng-d9lcsgk.png", "name":"fir_branch_02_by_nellygraceng-d9lcsgk.png"}], show_multiview=False)
    bpy.ops.node.link(detach=False, drag_start=(-30.6074, 201.239))
    # select tree trunk
    bpy.ops.object.convert(target='MESH')
    bpy.ops.material.new()
    bpy.ops.node.nw_add_textures_for_principled(filepath="C:\\Users\\Hunter Rogers\\Desktop\\Personal\\University of Utah\\DEep cap\\CS6953Project\\assets\\Bark014_8K-JPG\\Bark014_8K-JPG_NormalGL.jpg", directory="C:\\Users\\Hunter Rogers\\Desktop\\Personal\\University of Utah\\DEep cap\\CS6953Project\\assets\\Bark014_8K-JPG\\", files=[{"name":"Bark014.png", "name":"Bark014.png"}, {"name":"Bark014_8K-JPG_NormalGL.jpg", "name":"Bark014_8K-JPG_NormalGL.jpg"}, {"name":"Bark014_8K-JPG_Color.jpg", "name":"Bark014_8K-JPG_Color.jpg"}], relative_path=True)
    
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


bpy.ops.object.select_all(action='SELECT')  # Select all objects
bpy.ops.object.delete()  # Delete selected objects

create_pine_tree("tree1", position=(0,0,0)) #

create_pine_tree("tree2", position=(0,2,0))
create_pine_tree("tree3", position=(2,0,0))
create_pine_tree("tree4", position=(0,0,2))



#Hi