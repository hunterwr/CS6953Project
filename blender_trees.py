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
    bpy.ops.curve.tree_add(
    do_update=True, 
    bevel=True, 
    prune=False, 
    showLeaves=False, 
    useArm=False, 
    seed=2, 
    handleType='0', 
    levels=2, 
    length=(0.8, 0.6, 0.5, 0.1), 
    lengthV=(0, 0.1, 0, 0), 
    taperCrown=0.5, 
    branches=(0, 55, 10, 1), 
    curveRes=(8, 5, 3, 1), 
    curve=(0, -15, 0, 0), 
    curveV=(20, 50, 75, 0), 
    curveBack=(0, 0, 0, 0), 
    baseSplits=3, 
    segSplits=(0.1, 0.5, 0.2, 0), 
    splitByLen=True, 
    rMode='rotate', 
    splitAngle=(18, 18, 22, 0), 
    splitAngleV=(5, 5, 5, 0), 
    scale=5, scaleV=2, 
    attractUp=(3.5, -1.89984, 0, 0), 
    attractOut=(0, 0.8, 0, 0), 
    shape='7', shapeS='10', 
    customShape=(0.5, 1, 0.3, 0.5), 
    branchDist=1.5, nrings=0, 
    baseSize=0.3, 
    baseSize_s=0.16, 
    splitHeight=0.2, 
    splitBias=0.55, 
    ratio=0.015, 
    minRadius=0.0015, 
    closeTip=False, 
    rootFlare=1, 
    autoTaper=True, 
    taper=(1, 1, 1, 1), 
    radiusTweak=(1, 1, 1, 1), 
    ratioPower=1.2, 
    downAngle=(0, 26.21, 52.56, 30), 
    downAngleV=(0, 10, 10, 10), 
    useOldDownAngle=True, 
    useParentAngle=True, 
    rotate=(99.5, 137.5, 137.5, 137.5), 
    rotateV=(15, 0, 0, 0), 
    scale0=1, 
    scaleV0=0.1, 
    pruneWidth=0.34, 
    pruneBase=0.12, 
    pruneWidthPeak=0.5, 
    prunePowerHigh=0.5,
    prunePowerLow=0.001, 
    pruneRatio=0.75, 
    leaves=150, 
    leafDownAngle=30, 
    leafDownAngleV=-10, 
    leafRotate=137.5, 
    leafRotateV=15, 
    leafScale=0.4, 
    leafScaleX=0.2, 
    leafScaleT=0.1, 
    leafScaleV=0.15, 
    leafShape='hex', 
    bend=0, 
    leafangle=-12, 
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
    
    obj = bpy.context.object  # Get the newly created object
    obj.name = name  # Rename the object
    
    select_object(name)
    move_selected_object(position)
    
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