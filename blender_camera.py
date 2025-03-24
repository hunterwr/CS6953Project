# Camera position funtions


import bpy
import math
import os
import random
import bmesh
import bpy_extras
import mathutils
from mathutils import Vector

def add_camera(target_directory, background="dunes" , location=(0.0, -19.409, 14.526), rotation=(69.127, 0.000008, 0.569964), scale=1.0):
    """
    Adds a camera to the scene at a specified location, rotation, and scale.

    :location: Tuple (x, y, z) - Camera position in meters.
    :rotation: Tuple (x, y, z) - Camera rotation in degrees.
    :scale: Float - Scale of the camera (default 1.0).
    """
    # Create a new camera object
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.name = "Camera"

    # Set Camera Location
    camera.location = location

    # Convert degrees to radians and set rotation, blender uses radians
    camera.rotation_euler = (
        math.radians(rotation[0]),  # X Rotation
        math.radians(rotation[1]),  # Y Rotation
        math.radians(rotation[2])   # Z Rotation
    )

    # Set Camera Scale
    camera.scale = (scale, scale, scale)

    # Set as active camera
    bpy.context.scene.camera = camera
    
    
    # Adding a background and attach it to camera
    bpy.ops.mesh.primitive_plane_add(size=1)
    background_plane = bpy.context.object
    background_plane.name = "Background Plane"
    
    background_plane.scale = (1200.0, 800.0, 0.0)
    background_plane.rotation_euler = camera.rotation_euler
    background_plane.location = (0.0, 380.0, 280.0)
    
    # Set the parent of the background plane to the camera
    background_plane.parent = camera
    background_plane.matrix_parent_inverse = camera.matrix_world.inverted()
    
    # Create a new material
    material = bpy.data.materials.new(name="BackgroundMaterial")
    material.use_nodes = True

    nodes = material.node_tree.nodes
    links = material.node_tree.links

    nodes.clear()

    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    texture_node = nodes.new(type='ShaderNodeTexImage')

    # Set node locations
    output_node.location = (400, 0)
    principled_node.location = (200, 0)
    texture_node.location = (0, 0)
    
    path = f"{target_directory}/textures/Background/{background}.jpg"
    
    if os.path.exists(path):
        image = bpy.data.images.load(path)
        texture_node.image = image
    else:
        return

    # Link nodes
    links.new(texture_node.outputs["Color"], principled_node.inputs["Base Color"])
    links.new(texture_node.outputs['Color'], principled_node.inputs['Emission Color'])
    principled_node.inputs['Emission Strength'].default_value = 0.3
    links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])

    # Assign the material to the background plane
    background_plane.data.materials.append(material)
    
    # Enter edit mode on the background plane and perform cube projection UV unwrap
    bpy.context.view_layer.objects.active = background_plane
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.cube_project()
    bpy.ops.object.mode_set(mode='OBJECT')
    
    #define frames for animation
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 500
        
    return camera


class CameraController:
    """
    Controls camera movement to ensure traffic signs remain in view
    while providing different perspectives of the scene.
    """
    
    def __init__(self, camera, road_boundaries, sign_name="Simple Sign", height_range=(4, 10)):
        """
        Initialize the camera controller.
        
        Args:
            camera: Blender camera object to control
            road_boundaries: List of coordinates defining road boundaries
            sign_name: Name of the traffic sign object to keep in view
            height_range: Min and max heights for camera positioning
        """
        self.camera = camera
        self.road_boundaries = road_boundaries
        self.sign_obj = bpy.data.objects.get(sign_name)
        if not self.sign_obj:
            raise ValueError(f"Sign object '{sign_name}' not found in scene")
            
        self.height_range = height_range
        self.road_start_y = min(p[1] for p in road_boundaries)
        self.road_end_y = max(p[1] for p in road_boundaries)
        self.road_left_x = min(p[0] for p in road_boundaries)
        self.road_right_x = max(p[0] for p in road_boundaries)
        self.road_width = self.road_right_x - self.road_left_x
        self.road_length = self.road_end_y - self.road_start_y
        
        # Store initial position to avoid straying too far
        self.initial_position = self.camera.location.copy()
        
        # Set up tracking history to avoid repeating positions
        self.position_history = []
        self.max_history = 10
        
        # Movement ranges in XYZ, relative to current position
        self.movement_ranges = {
            'x': (-self.road_width * 0.1, self.road_width * 0.1),
            'y': (-25, 25),  # Forward/back movement range
            'z': (-1, 1)     # Height adjustment range
        }
        
        # Track failed attempts to find good positions
        self.failed_attempts = 0
        self.max_failed_attempts = 5
        
        # Store the sign's world position for reference
        self.sign_position = self.sign_obj.location.copy()
        
        print(f"Camera controller initialized with road boundaries: {road_boundaries}")
        print(f"Sign position: {self.sign_position}")
    
    def is_position_on_road(self, position):
        """Check if a position is within the road boundaries"""
        buffer = self.road_width * 0.1  # Small buffer from edge
        return (self.road_left_x + buffer <= position[0] <= self.road_right_x - buffer and
                self.road_start_y <= position[1] <= self.road_end_y)
    
    def is_sign_in_view(self):
        """
        Check if the entire traffic sign is fully visible from the current camera position.
        Returns True if all corners are visible, False otherwise.
        """
        scene = bpy.context.scene
        
        # Get sign's bounding box corners in world space
        bbox_corners = [self.sign_obj.matrix_world @ Vector(corner) for corner in self.sign_obj.bound_box]

        # Convert corners to camera space
        camera_matrix = self.camera.matrix_world.inverted()
        projected_corners = [bpy_extras.object_utils.world_to_camera_view(scene, self.camera, corner) for corner in bbox_corners]

        # Check if ALL corners are inside the camera frame
        all_corners_visible = all(0 < co_2d.x < 1 and 0 < co_2d.y < 1 for co_2d in projected_corners)

        # Ensure all corners are in front of the camera (positive Z in camera space)
        all_corners_in_front = all((camera_matrix @ corner).z > 0 for corner in bbox_corners)

        # The sign is fully visible only if ALL corners are inside the camera frame AND in front of the camera
        return all_corners_visible and all_corners_in_front

    
    def get_sign_direction(self):
        """Get normalized direction vector from camera to sign"""
        cam_loc = self.camera.location
        sign_loc = self.sign_obj.location
        direction = Vector((sign_loc.x - cam_loc.x, 
                           sign_loc.y - cam_loc.y,
                           sign_loc.z - cam_loc.z))
        return direction.normalized()
    
    def adjust_to_view_sign(self):
        """Adjust camera rotation to look at the sign"""
        direction = self.get_sign_direction()
        
        # Create a rotation quaternion that points in the direction of the sign
        track_quat = direction.to_track_quat('-Z', 'Y')
        
        # Convert to Euler rotation
        self.camera.rotation_euler = track_quat.to_euler()
        
        # Add some random variation to rotation (within small range)
        # self.camera.rotation_euler.x += random.uniform(-0.1, 0.1)
        self.camera.rotation_euler.z = 0
        # self.camera.rotation_euler.y += random.uniform(-0.05, 0.05)
    
    def move_towards_road_center(self):
        """Move camera back toward road center if it's too far off"""
        road_center_x = (self.road_left_x + self.road_right_x) / 2
        
        # Calculate vector to road center
        current_x = self.camera.location.x
        move_x = (road_center_x - current_x) * 0.05  # Move 20% of the way
        
        # Apply movement
        self.camera.location.x += move_x
    
    def step(self):
        """
        Move the camera to a new position that keeps the sign in view
        Returns True if successful, False if couldn't find a valid position
        """
        original_location = self.camera.location.copy()
        original_rotation = self.camera.rotation_euler.copy()
        
        # Store current position in history
        if len(self.position_history) >= self.max_history:
            self.position_history.pop(0)
        self.position_history.append((self.camera.location.x, self.camera.location.y, self.camera.location.z))
        
        # Try to find a new valid position
        for attempt in range(10):  # Try up to 10 times to find a good position
            # Random movement in all directions
            new_x = self.camera.location.x + random.uniform(*self.movement_ranges['x'])
            new_y = self.camera.location.y + random.uniform(*self.movement_ranges['y'])
            new_z = self.camera.location.z + random.uniform(*self.movement_ranges['z'])
            
            # Ensure height stays within reasonable range
            new_z = max(min(new_z, self.height_range[1]), self.height_range[0])
            
            # Check if new position is too similar to recent positions
            too_similar = False
            for pos in self.position_history[-3:]:  # Check last 3 positions
                distance = ((new_x - pos[0])**2 + (new_y - pos[1])**2 + (new_z - pos[2])**2)**0.5
                if distance < 2.0:  # If too close to a recent position
                    too_similar = True
                    break
            
            if too_similar:
                continue
            
            # Apply new position
            self.camera.location = mathutils.Vector((new_x, new_y, new_z))
            
            # Check if we're still on the road
            if not self.is_position_on_road((new_x, new_y, new_z)):
                self.move_towards_road_center()
            
            # Adjust camera to look at sign
            # self.adjust_to_view_sign()
            
            # Check if sign is visible after adjustment
            if self.is_sign_in_view():
                
                self.failed_attempts = 0
                return True
        
        # If we couldn't find a good position, adjust camera to directly face the sign
        self.failed_attempts += 1
        
        if self.failed_attempts >= self.max_failed_attempts:
            # Reset to a known good position near the sign
            print("Failed to find a good position, resetting to known position")
            self.camera.location = mathutils.Vector((
                self.sign_position.x - random.uniform(40, 50),
                self.sign_position.y - random.uniform(50, 60),
                self.height_range[0] + random.uniform(2, 4)
            ))
            self.failed_attempts = 0
        else:
            # Restore original position
            self.camera.location = original_location
            self.camera.rotation_euler = original_rotation
            
            # Try moving toward the sign
            sign_dir = self.get_sign_direction()
            self.camera.location += sign_dir * random.uniform(3, 8)
            self.adjust_to_view_sign()
        
        return self.is_sign_in_view()
