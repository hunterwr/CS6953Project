import bpy




def create_straight_road(length=10, width=2):
    """
    Creates a straight road segment.

    :param length: Length of the road.
    :param width: Width of the road.
    """
    pass

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
