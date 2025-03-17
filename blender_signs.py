import bpy
import texture_utils as textures
import math
import bmesh
from mathutils import Vector
import os 

def generate_sign(road_boundaries,png_path ='textures/Signs/Signs/PNGs/Loose Gravel.png',scratches =0.25, rust = 0.25,rivets=False,snow = 0.0,mud = 0.0, sign_name = 'Simple Sign', target_directory = None ):
    # Create the pole

    print(road_boundaries)
    right_edge = road_boundaries[2][0]
    pole_end_points = create_pole(
        0.2,
        5,
        location=(right_edge + 3, 50, 5 / 2),
        texture_path=os.path.join(target_directory, 'textures/Signs/sign_pole_al.PNG')
    )


    # to center road 
    # roadwidth -(road_width-((road_width-offset)/2))
    # Create a simple square sign

    create_sign_square(
        5,
        5,
        text=None,
        start_location=(
            pole_end_points[0]-5/2,
            pole_end_points[1] - 2.5 * 0.2,
            pole_end_points[2] - 0.25
        ),
        name= sign_name
    )

    # Add a sign texture
    sign_obj = bpy.data.objects.get(sign_name)

    # texutils.apply_sign_png_conditions(sign_obj,png_path = os.path.join(target_directory,'textures/Signs/Signs/PNGs/Loose Gravel.png'),
#                                     scratches_on =0.5, rust_minor_on = 0.0, rust_major_on = False,rivets_on=False,snow=0.5,target_directory = target_directory)

    textures.apply_sign_png_conditions(sign_obj,png_path = os.path.join(target_directory,png_path),
                                        scratches_on =scratches, rust_minor_on = rust, rust_major_on = False,rivets_on=rivets,snow=snow,mud=mud,target_directory = target_directory)

def unwrap_uv(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66)  # Auto UV Unwrap
    bpy.ops.object.mode_set(mode='OBJECT')

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



def create_sign_square(width,height,text=None,start_location = (0,0,0),name='Sign'):
    
# Create a cube
    thickness =0.1
    verts = [(0,0,0),(0,thickness,0),(width,thickness,0),(width,0,0),(0,0,height),(0,thickness,height),(width,thickness,height),(width,0,height)]
    faces = [(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    

    mymesh = bpy.data.meshes.new(name)
    myobject = bpy.data.objects.new(name, mymesh)
    mymesh.from_pydata(verts, [], faces)
    mymesh.update()
    myobject.data.materials.clear()
  
    myobject.location = start_location  

    bpy.context.collection.objects.link(myobject) 
    if text != None:
        # Create text object
        bpy.ops.object.text_add(location=(width/2, -0.001, height/2))  # Adjust position to front face
        text_obj = bpy.context.object
        text_obj.data.body = text
        text_obj.data.align_x = 'CENTER'
        text_obj.data.align_y = 'CENTER'
        

        # Rotate text to face forward
        text_obj.rotation_euler= (1.5708,0,0)  # Rotate 90 degrees on X-axis

        # Scale text to fit cube
        text_obj.scale = (0.6, 0.6, 0.2)

        # Parent text to cube (optional)
        text_obj.parent = myobject





def add_sign_color(object, target_directory, texture_path = None):
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.context.view_layer.objects.active = object
    
    obj = object
    unwrap_uv(obj)
    textures.apply_blenderkit_sign_jpg(obj,target_directory=target_directory,base_color_path=texture_path)





def create_pole(radius,height, location = (0,0,0),texture_path = None):
    
    bpy.ops.mesh.primitive_cylinder_add(radius=radius,depth=height, location=location)
    
    
    
    obj = bpy.context.object  # Get the created object
    
    obj.data.materials.clear()

    
    
    
    mat = bpy.data.materials.new(name="PoleMaterial")
    obj.data.materials.append(mat)

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    

    # Create the Principled BSDF shader
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
#    bsdf.inputs['Base Color'].default_value = color  # Default is white
#      
    bsdf.location = (0, 0)
    bsdf.inputs['Metallic'].default_value = 1 # Make it a full metal
    bsdf.inputs['Roughness'].default_value = 0.8  # Slightly shiny metal 
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.cylinder_project()
    
    
    
    
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
#    uv_layer = obj.data.uv_layers.active.data
#    for uv in uv_layer:
#        uv.uv.x *= 1 # Stretch horizontally (default = 1.0)
#        uv.uv.y *= 10 # Stretch vertically (increase to fix compression)
        
    tex_image = nodes.new(type="ShaderNodeTexImage")
    tex_image.location = (-400, 0)
    tex_image.image = bpy.data.images.load(texture_path)  
    
    tex_coord = nodes.new(type="ShaderNodeTexCoord")
    tex_coord.location = (-600, 0)
    
    
        # ADD A MAPPING NODE TO CONTROL UV SCALE
    mapping = nodes.new(type="ShaderNodeMapping")
    mapping.location = (-500, 0)

    # Adjust the UV scale (X controls horizontal tiling, Y controls vertical stretching)
    mapping.inputs['Scale'].default_value[0] = 1.0  # Keep horizontal scaling normal
    mapping.inputs['Scale'].default_value[1] = 1  # Stretch vertically
    mapping.inputs['Rotation'].default_value[0] = 1.5708 #rotate
    
    
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])  # Connect UV to Mapping
    links.new(mapping.outputs['Vector'], tex_image.inputs['Vector']) 
    
    links.new(tex_image.outputs['Color'],bsdf.inputs['Base Color'])
    
    
    output = nodes.new(type="ShaderNodeOutputMaterial")
    output.location = (200, 0)
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    
    z_out = height/2+location[2]
    x_out = location[0]+radius
    y_out = location[1]+radius
    return [x_out,y_out,z_out]


def create_round_sign(radius, center_location, texture_path=None,thickness = 0.2):
    
    bpy.ops.mesh.primitive_cylinder_add(radius=radius,depth=thickness, location=center_location, rotation=(1.5708,0,0))
    
    obj = bpy.context.object  # Get the created object
    
    obj.data.materials.clear()
    
    




def create_stop_sign(radius, center_location, texture_path=None,thickness = 0.2):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius,depth=thickness, location=center_location, rotation=(1.5708,.785,0),vertices=8)
    
   
    # Get the created object
    obj = bpy.context.object

    # Switch to Edit Mode to modify the mesh
    bpy.ops.object.mode_set(mode='EDIT')

    # Select all vertices
    bpy.ops.mesh.select_all(action='SELECT')

    # Switch to Vertex Select mode
    bpy.ops.mesh.select_mode(type='VERT')

    # Calculate the angle between the vertices (45 degrees for an octagon)
    angle = math.pi / 4  # 45 degrees in radians

    # Loop through vertices and adjust their positions to form an octagon
    bpy.ops.transform.resize(value=(1, 1, 1))  # Reset any accidental scaling

    # Switch back to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.transform.rotate(value=math.radians(23), orient_axis='Y')

    # Optionally, apply transformations (location/rotation/scale)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    



def create_speed_limit_sign(position=(0, 0, 0), size=1, speed=50, reflectiveness=1.0, angle=0):
    """
    Creates a speed limit sign.

    :param position: Tuple of (x, y, z) coordinates for the sign's position.
    :param size: Size multiplier for the sign.
    :param speed: Speed limit to display on the sign.
    :param reflectiveness: Reflectiveness of the sign material.
    :param angle: Rotation angle of the sign in degrees.
    """
    pass

def create_yield_sign(position=(0, 0, 0), size=1, reflectiveness=1.0, angle=0):
    """
    Creates a yield sign.

    :param position: Tuple of (x, y, z) coordinates for the sign's position.
    :param size: Size multiplier for the sign.
    :param reflectiveness: Reflectiveness of the sign material.
    :param angle: Rotation angle of the sign in degrees.
    """
    pass

def create_custom_sign(position=(0, 0, 0), shape="rectangle", size=(1, 1), reflectiveness=1.0, angle=0):
    """
    Creates a custom sign with a specified shape.

    :param position: Tuple of (x, y, z) coordinates for the sign's position.
    :param shape: Shape of the sign (e.g., "rectangle", "circle", "triangle").
    :param size: Tuple of (width, height) for the sign dimensions.
    :param reflectiveness: Reflectiveness of the sign material.
    :param angle: Rotation angle of the sign in degrees.
    """
    pass

def create_warning_sign(position=(0, 0, 0), size=1, warning_text="", reflectiveness=1.0, angle=0):
    """
    Creates a warning sign with custom text.

    :param position: Tuple of (x, y, z) coordinates for the sign's position.
    :param size: Size multiplier for the sign.
    :param warning_text: Text to display on the sign.
    :param reflectiveness: Reflectiveness of the sign material.
    :param angle: Rotation angle of the sign in degrees.
    """
    pass

def create_directional_sign(position=(0, 0, 0), size=1, direction_text="", reflectiveness=1.0, angle=0):
    """
    Creates a directional sign with custom text.

    :param position: Tuple of (x, y, z) coordinates for the sign's position.
    :param size: Size multiplier for the sign.
    :param direction_text: Text to display on the sign (e.g., "Left", "Right").
    :param reflectiveness: Reflectiveness of the sign material.
    :param angle: Rotation angle of the sign in degrees.
    """
    pass

def create_sign_post(position=(0, 0, 0), height=3, diameter=0.1):
    """
    Creates a post to hold a road sign.

    :param position: Tuple of (x, y, z) coordinates for the post's position.
    :param height: Height of the post.
    :param diameter: Diameter of the post.
    """
    pass

def create_sign_network():
    """
    Creates a network of road signs by combining multiple sign elements.
    """
    pass
