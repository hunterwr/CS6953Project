import bpy


import math
import bpy
import time 

import texture_utils as textures 

def road_presets(scene = 'Two Lane', conditions = 'Dry',target_directory = None):
    if scene == 'Two Lane': 
        create_road_edges(
        road_width=50,road_height=1, 
        road_length=300,
        left_edge_start = (-(50/2),-50,0),
        name='Road_Edges',
        target_directory=target_directory,
        conditions= conditions)
        left_edge_start = (-(50/2),-50,0)
        road_width = 50
        road_length = 300 
        left_edge_start_x, left_edge_start_y, left_edge_start_z = left_edge_start
        left_edge_end = (left_edge_start_x, left_edge_start_y + road_length, left_edge_start_z)
        right_edge_start = (left_edge_start_x + road_width, left_edge_start_y, left_edge_start_z)
        right_edge_end = (right_edge_start[0], right_edge_start[1] + road_length, right_edge_start[2])
        road_boundaries = [left_edge_start, left_edge_end, right_edge_start, right_edge_end]
        lane_1 = (0.25*road_width +left_edge_start[0], left_edge_start[1],left_edge_start[2])
        lane_2 = (0.75*road_width +left_edge_start[0], left_edge_start[1],left_edge_start[2])
        lane_positions = [ lane_1,lane_2]



    
      

        
        
    elif scene == 'Highway':
        
        ### Create the road ### 
        width = 50
                
        create_road_edges(
        road_width=width,road_height=1, 
        road_length=300,
        left_edge_start = (-(width/2),-50,0),
        name='Road_Edges',
        target_directory=target_directory,
        conditions=conditions)
        
        start = width*0.6031 +0.3643
        
        obj = bpy.data.objects.get('Road_Edges')
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        # Duplicate the object
        bpy.ops.object.duplicate()

        # Get the newly duplicated object (it will now be the active object)
        obj2 = bpy.context.object  

        # Move the duplicated object  
        obj2.location.x = -(width / 2) + start

       
        
        ### Pull in and place guardrails, lights, and barriers 
        left_edge_start = (-(50/2),-50,0)
        road_width = 50
        road_length = 300 


        left_edge_start_x, left_edge_start_y, left_edge_start_z = left_edge_start
        offset  =  (-(width / 2) + start) - left_edge_start_x
        
        left_edge_end = (left_edge_start_x, left_edge_start_y + road_length, left_edge_start_z)
        right_edge_start = (left_edge_start_x + road_width+ offset, left_edge_start_y, left_edge_start_z)
        right_edge_end = (right_edge_start[0], right_edge_start[1] + road_length, right_edge_start[2])
        road_boundaries = [left_edge_start, left_edge_end, right_edge_start, right_edge_end]
        total_width = right_edge_start[0] - left_edge_start_x

        lane_1 = (0.224*total_width + left_edge_start[0], left_edge_start[1],left_edge_start[2])
        lane_2 = (0.415*total_width + left_edge_start[0], left_edge_start[1],left_edge_start[2])
        lane_3 = (0.631*total_width + left_edge_start[0], left_edge_start[1],left_edge_start[2]) 
        lane_4 = (0.8288*total_width + left_edge_start[0], left_edge_start[1],left_edge_start[2])
        lane_positions = [ lane_1,lane_2,lane_3,lane_4]
        
        guardrails_path = target_directory+r'/textures/Roads/objects/traffic-barrier-_00a35510-614d-44ee-905b-25072de5c7da/traffic-barrier-guardrail-type-01_1K_0e77ca0d-9e51-4816-a7b3-2d26d9575f47.blend'
        lights_path = target_directory+r'/textures/Roads/objects/street-light-pac_8356b020-1297-4647-9251-4585ccaa8b4a/street-light-pack_2K_98a43fe4-433c-488b-b1d6-e9929b3aff64.blend'
        cement_barrier= target_directory+r'/textures/Roads/objects/concrete-blockad_629ae09d-4a37-4868-ba29-a60a83c2455d/concrete-blockade_1K_367f5d49-efce-41bb-9039-31072550d5b1.blend'




        # bpy.ops.object.modifier_add(type='MIRROR')

        ### Add Cement Barrier 
        with bpy.data.libraries.load(cement_barrier, link=False) as (data_from, data_to):
                    # Load all objects in the .blend file
                    data_to.objects = data_from.objects 
        #            obj = data_to.objects[0]
        #            if obj is not None:
        #                obj = bpy.data.objects.get(obj)   
        #                bpy.context.collection.objects.link(obj)
        #               
        #                obj.scale = (6.0, 6.0, 6.0)
        #                obj.location = (15, -40.0, 1.0) 
        #                bpy.context.object.rotation_euler[2] = math.radians(90)

                    
        for obj in data_to.objects:
            if obj is not None:
                bpy.context.collection.objects.link(obj)
                # Reset location (set to 0, 0, 0)
        
                obj.scale = (2.35, 2.35, 2.35)
                obj.location = (15.0/2, -40.0/2, 1.0/2) 
                
                obj.rotation_euler[2] = math.radians(45)
                obj.location = (-7, -21, 0) 
                
        obj = bpy.data.objects.get('RoadBlockade_02')        
        array_modifier = obj.modifiers.new(name="Array", type='ARRAY')
        array_modifier.count = 20  # Number of array copies
        array_modifier.use_relative_offset = True  # Use constant offset (for linear array)
        array_modifier.relative_offset_displace = (1.0, 0.0, 0.0)  # Offset along the X-axis


        ###guardrails 
        with bpy.data.libraries.load(guardrails_path, link=False) as (data_from, data_to):
            # Load all objects in the .blend file
            data_to.objects = data_from.objects 
            
        for obj in data_to.objects:
            if obj is not None:
                bpy.context.collection.objects.link(obj)
                obj.scale = (2.5, 2.5, 2.5)
                obj.rotation_euler.z+=math.radians(45)
        
                obj.location = (-12, -7.0, 1.0) 
                obj.rotation_mode = 'XYZ' 
        #        obj.rotation_euler = (math.radians(90),0,0)
                
        #        obj.rotation_euler.z+=math.radians(90)
        obj = bpy.data.objects.get('Plane.001')        
        array_modifier = obj.modifiers.new(name="Array", type='ARRAY')
        array_modifier.count = 23  # Number of array copies
        array_modifier.use_relative_offset = True  # Use constant offset (for linear array)
        array_modifier.relative_offset_displace = (0.0, 1.0, 0.0)  # Offset along the X-axis


        with bpy.data.libraries.load(guardrails_path, link=False) as (data_from, data_to):
        # Load all objects in the .blend file
            data_to.objects = data_from.objects 
            
        for obj in data_to.objects:
            if obj is not None:
                bpy.context.collection.objects.link(obj)
                obj.scale = (2.5, 2.5, 2.5)
                obj.rotation_euler.z+=math.radians(-45)
        
                obj.location = (22.5, -6.0, 1.0) 
                obj.rotation_mode = 'XYZ' 
        #        obj.rotation_euler = (math.radians(90),0,0)
                
        #        obj.rotation_euler.z+=math.radians(90)
        obj = bpy.data.objects.get('Plane.002')        
        array_modifier = obj.modifiers.new(name="Array", type='ARRAY')
        array_modifier.count = 23  # Number of array copies
        array_modifier.use_relative_offset = True  # Use constant offset (for linear array)
        array_modifier.relative_offset_displace = (0.0, -1.0, 0.0)  # Offset along the X-axis

        ### Add Overhead Lights ### 
        with bpy.data.libraries.load(lights_path, link=False) as (data_from, data_to):
        # Load all objects in the .blend file
            data_to.objects = data_from.objects 
            
        for obj in data_to.objects:
            if obj is not None and obj.name =='Street Light 1':
                bpy.context.collection.objects.link(obj)
                obj.scale = (5, 5, 5)
                obj.rotation_euler.z+=math.radians(-90)

                obj.location = (58.0, -45, 1.0) 
                obj.rotation_mode = 'XYZ' 

        obj = bpy.data.objects.get('Street Light 1')        
        array_modifier = obj.modifiers.new(name="Array", type='ARRAY')
        array_modifier.count =5 # Number of array copies
        array_modifier.use_relative_offset = True  # Use constant offset (for linear array)
        array_modifier.relative_offset_displace = (-40, 0.0, 0.0)  # Offset along the X-axis

        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        # Duplicate the object
        bpy.ops.object.duplicate()

        # Get the newly duplicated object (it will now be the active object)
        obj2 = bpy.context.object  

        # Move the duplicated object  
        obj2.location= (-28.0, 200, 1.0) 
        obj2.rotation_euler.z+=math.radians(180)

    return road_boundaries,lane_positions

def apply_blenderkit_material(obj_name, asset_base_id):

#    

    obj = bpy.data.objects.get(obj_name)

    bpy.data.window_managers["WinMan"].blenderkitUI.asset_type = 'MATERIAL'
    bpy.data.window_managers["WinMan"].blenderkit_mat.search_keywords = '4k Wet Road 02'
    bpy.ops.view3d.blenderkit_asset_bar_widget(do_search=False, keep_running=True)
    
    bpy.ops.scene.blenderkit_download(asset_index=0, target_object=obj_name, material_target_slot=0, model_rotation=(0, 0, 0),model_location =obj.location)

    

def unwrap_uv(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66)  # Auto UV Unwrap
    bpy.ops.object.mode_set(mode='OBJECT')
    
    

def create_road_edges(road_width,road_height, road_length,left_edge_start = (0,0,0),name='Road_Edges',target_directory = None, conditions = 'Dry'):
    
# Create a cube
    
    verts = [(0,0,0),(0,road_length,0),(road_width,road_length,0),(road_width,0,0),(0.15*road_width,0,road_height),
            (0.15*road_width,road_length,road_height),(.85*road_width,road_length,road_height),(0.85*road_width,0,road_height)]
    faces = [(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    

    mymesh = bpy.data.meshes.new(name)
    myobject = bpy.data.objects.new(name, mymesh)
    mymesh.from_pydata(verts, [], faces)
    mymesh.update()
    myobject.data.materials.clear()
  
    myobject.location = left_edge_start 
    bpy.context.collection.objects.link(myobject)
    bpy.context.view_layer.objects.active = myobject 
    
    bpy.ops.object.modifier_add(type='BEVEL')
    bpy.context.object.modifiers["Bevel"].affect = 'EDGES'
    bpy.context.object.modifiers["Bevel"].segments = 11
    bpy.context.object.modifiers["Bevel"].angle_limit = 0.0802852
    bpy.context.object.modifiers["Bevel"].width = 1.89
#    
    unwrap_uv(myobject)
#    
    length_width_ratio = road_length/road_width
###    search_blenderkit_asset('4k Wet Road 02')
#   try:
#        apply_blenderkit_material(myobject.name,asset_base_id=asset_base_id)
#   except:
#        create_road_edges(road_width=road_width,road_height=road_height, road_length=road_length,left_edge_start = (0,0,0),name='Road_Edges',asset_base_id="4b99930c-2ebd-4fb3-9c5a-d3a61fece0c7")
        
    # apply_blenderkit_material(myobject.name,asset_base_id=asset_base_id)
    
    # bpy.context.view_layer.update() 
    # obj = bpy.data.objects.get(name) 
    # bpy.context.view_layer.objects.active = obj
    if conditions == 'Wet':
        textures.apply_blenderkit_wetRoad(myobject,target_directory=target_directory)
        bpy.data.materials["4K Wet road 02"].node_tree.nodes["Mapping"].inputs['Rotation'].default_value[2] = 1.5708
        bpy.data.materials["4K Wet road 02"].node_tree.nodes["Mapping"].inputs['Location'].default_value[0] = 1.3
        bpy.data.materials["4K Wet road 02"].node_tree.nodes["Mapping"].inputs['Location'].default_value[1] = -.05
        bpy.data.materials["4K Wet road 02"].node_tree.nodes["Mapping"].inputs['Scale'].default_value[0] = -1.6044*length_width_ratio-0.1581
        bpy.data.materials["4K Wet road 02"].node_tree.nodes["Mapping"].inputs['Scale'].default_value[1] = 0.0175*road_length+1.2
    else:
        textures.apply_blenderkit_dryRoad(myobject,target_directory=target_directory)
    
        bpy.data.materials["Patched road 02"].node_tree.nodes["Mapping"].inputs['Rotation'].default_value[2] = 1.5708
        bpy.data.materials["Patched road 02"].node_tree.nodes["Mapping"].inputs['Location'].default_value[0] = 1.3
        bpy.data.materials["Patched road 02"].node_tree.nodes["Mapping"].inputs['Location'].default_value[1] = -.05
        bpy.data.materials["Patched road 02"].node_tree.nodes["Mapping"].inputs['Scale'].default_value[0] = -1.6044*length_width_ratio-0.1581
        bpy.data.materials["Patched road 02"].node_tree.nodes["Mapping"].inputs['Scale'].default_value[1] = 0.0175*road_length+1.2
        
        
 










def create_spline_road(width,length,spline_start=(0,0,0),spline_end=(20,20,0), curvature_points = 2, curvature_score =1,texture_path = None,texture_scaling=1):
    
    
    ####### Create the Base Curvature ########
    # Create a simple road
    curve_data = bpy.data.curves.new(name="BezierCurve", type='CURVE')
    curve_data.dimensions = '2D'

    # Create a new spline
    spline = curve_data.splines.new(type='BEZIER')

    #  spline.bezier_points[i].handle_right = (curvature_score*1,0,0) 
    points = []
    if curvature_points > 2:
        
        step = abs((spline_end[0] - spline_start[0]) / (curvature_points - 1))
        for i in range(1, curvature_points - 1):  # skip the first and last point
            x = spline_start[0] + i * step
            y = spline_start[1] + i * step
            points.append((x, y, 0))

    
    spline.bezier_points.add(count=curvature_points - 1)  

    # Set the first and last control points
    spline.bezier_points[0].co = spline_start
    spline.bezier_points[-1].co = spline_end

    # Set the intermediate points
    for i in range(1, curvature_points - 1):
        spline.bezier_points[i].co = points[i - 1]

    # Set the handles for the control points to ensure the curve doesn't close
    for i in range(curvature_points):
        if i == 0 or i == curvature_points - 1:
            # Start and end points should not have handles pointing away from the curve
            spline.bezier_points[i].handle_left = spline.bezier_points[i].co
            spline.bezier_points[i].handle_right = spline.bezier_points[i].co
        else:
            # Set handles for intermediate points to create smooth curves
            spline.bezier_points[i].handle_left = (spline.bezier_points[i].co[0] - curvature_score, spline.bezier_points[i].co[1], 0)
            spline.bezier_points[i].handle_right = (spline.bezier_points[i].co[0] + curvature_score, spline.bezier_points[i].co[1], 0)

    

    # Create a new curve object and link it to the scene
    curve_object = bpy.data.objects.new("Road", curve_data)
    bpy.context.collection.objects.link(curve_object)
    
    bpy.context.view_layer.objects.active = curve_object
    bpy.ops.node.new_geometry_nodes_modifier()
    
    node_tree = bpy.data.node_groups['Geometry Nodes']
    
    # grab the output node we just made 
    out_node = node_tree.nodes['Group Output'] 
    #grab the input node we just made
    in_node = node_tree.nodes['Group Input']
    
    # Create the Curve to Mesh node
    curve_to_mesh = node_tree.nodes.new(type='GeometryNodeCurveToMesh') 
    
    #link the curve to mesh to the inputs and outputs 
    node_tree.links.new(in_node.outputs['Geometry'], curve_to_mesh.inputs['Curve'])
    node_tree.links.new(curve_to_mesh.outputs['Mesh'],out_node.inputs['Geometry'])
    
    
    ### Add profile Curve ### 
    profile_curve = node_tree.nodes.new(type="GeometryNodeCurvePrimitiveLine")
    
    #link the curve
    
    node_tree.links.new(profile_curve.outputs['Curve'],curve_to_mesh.inputs['Profile Curve'])
    
    ### Adjust Curve Mesh ####
    profile_curve.inputs['Start'].default_value = (width,0,0)
    
    
    ## create set material node ##
    
    set_material = node_tree.nodes.new(type='GeometryNodeSetMaterial')
    
    
    ###create new material###
    mat = bpy.data.materials.new(name="RoadMaterial")
 #     obj.data.materials.append(mat) 
    
    mat.use_nodes = True
    
    #set to the newly created material 
    set_material.inputs['Material'].default_value = mat
    
    
    ## link in the appropriate place
    node_tree.links.new(curve_to_mesh.outputs['Mesh'],set_material.inputs['Geometry'])
    node_tree.links.new(set_material.outputs['Geometry'],out_node.inputs['Geometry'])
    
    
    ###Store Named Attribute###
    
    store_named_attribute_X = node_tree.nodes.new(type='GeometryNodeStoreNamedAttribute')
    store_named_attribute_X.inputs['Name'].default_value = 'Gradient X'
    
    node_tree.links.new(in_node.outputs['Geometry'],store_named_attribute_X.inputs['Geometry'])
    node_tree.links.new(store_named_attribute_X.outputs['Geometry'],curve_to_mesh.inputs['Curve'])
    
    
    
    store_named_attribute_Y = node_tree.nodes.new(type='GeometryNodeStoreNamedAttribute')
    store_named_attribute_Y.inputs['Name'].default_value = 'Gradient Y'
    
    node_tree.links.new(profile_curve.outputs['Curve'],store_named_attribute_Y.inputs['Geometry'])
    node_tree.links.new(store_named_attribute_Y.outputs['Geometry'],curve_to_mesh.inputs['Profile Curve'])
    
    bpy.context.view_layer.objects.active.data.materials.append(mat)
    
    #### switch to shaders... 
    bpy.context.view_layer.objects.active = curve_object
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create the Principled BSDF shader
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    uv_map1 = nodes.new(type = 'ShaderNodeAttribute')
    uv_map1.attribute_name = 'Gradient X'
    uv_map2 = nodes.new(type = 'ShaderNodeAttribute')
    uv_map2.attribute_name = 'Gradient Y'
    
    
    
    ####SWITCH X AND Y IF NEEDED ###### 
    
    ## Add Spline Parameter ## 
    Spline_Parameter_X  = node_tree.nodes.new(type = 'GeometryNodeSplineParameter')
    node_tree.links.new(Spline_Parameter_X.outputs['Length'],store_named_attribute_X.inputs['Value'])
   
   
    Spline_Parameter_Y  = node_tree.nodes.new(type = 'GeometryNodeSplineParameter')
    node_tree.links.new(Spline_Parameter_Y.outputs['Factor'],store_named_attribute_Y.inputs['Value'])

    
    
    ###Converter Combine XYZ ->SHADERS ###
    combine_xyz = nodes.new(type='ShaderNodeCombineXYZ')
    links.new(uv_map1.outputs['Fac'],combine_xyz.inputs['X'])
    links.new(uv_map2.outputs['Fac'],combine_xyz.inputs['Y'])
    
    
    
    ## Create Image Texture Node ## 
    tex_image = nodes.new(type="ShaderNodeTexImage")
    tex_image.image = bpy.data.images.load(texture_path)  
    
    ### Create Divide Node ### 
    vector_math = nodes.new(type='ShaderNodeVectorMath')
    vector_math.operation = 'DIVIDE'
    vector_math.inputs[1].default_value = (texture_scaling,1,1)
    links.new(combine_xyz.outputs['Vector'],vector_math.inputs['Vector'])
    links.new(vector_math.outputs['Vector'],tex_image.inputs['Vector'])
    links.new(tex_image.outputs['Color'],bsdf.inputs['Base Color'])
    
    ##Create Output Material 
    material_output = nodes.new(type='ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'],material_output.inputs['Surface'])
    
    return 
    
def test():
    print('Test')
    return 

def create_curved_road(radius=10, angle=90, width=2):
    """
    Creates a curved road segment.

    :param radius: Radius of the curve.
    :param angle: Angle of the curve in degrees.
    :param width: Width of the road.
    """
    pass

def create_multilane_road(lanes=2, length=10, width_per_lane=2):
    """
    Creates a multilane road segment.

    :param lanes: Number of lanes.
    :param length: Length of the road.
    :param width_per_lane: Width of each lane.
    """
    pass

def create_road_with_exit(main_length=10, exit_length=5, width=2, exit_angle=30):
    """
    Creates a road segment with an exit.

    :param main_length: Length of the main road.
    :param exit_length: Length of the exit road.
    :param width: Width of the road.
    :param exit_angle: Angle of the exit road relative to the main road.
    """
    pass

def create_intersection(road_count=4, road_width=2):
    """
    Creates an intersection with the specified number of connecting roads.

    :param road_count: Number of roads connecting at the intersection.
    :param road_width: Width of each connecting road.
    """
    pass

def create_roundabout(radius=10, lane_count=1, lane_width=2):
    """
    Creates a roundabout.

    :param radius: Radius of the roundabout.
    :param lane_count: Number of lanes in the roundabout.
    :param lane_width: Width of each lane.
    """
    pass

def create_bridge(length=20, width=4, height=5):
    """
    Creates a bridge segment.

    :param length: Length of the bridge.
    :param width: Width of the bridge.
    :param height: Height of the bridge above the ground.
    """
    pass

def create_tunnel(length=20, width=4, height=3):
    """
    Creates a tunnel segment.

    :param length: Length of the tunnel.
    :param width: Width of the tunnel.
    :param height: Height of the tunnel.
    """
    pass

def create_road_network():
    """
    Creates a complex road network by combining multiple road elements.
    """
    pass
