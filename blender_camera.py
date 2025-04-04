# Camera position funtions
import bpy
import math
import os
import random
import bmesh
import bpy_extras
import mathutils
from mathutils import Vector
#from PIL import Image, ImageDraw
import numpy as np

def add_camera(target_directory, car=None, lane_positions=None, camera_lane_number=2, background="dunes", lane_offset_z=5.0):
    """
    Adds a camera to the scene.
    
    If a car object is provided and exists, the camera is positioned relative to it
    using presets. Otherwise, if lane_positions is provided, the camera is placed at the
    center of the selected lane (and oriented forward along that lane). If neither is available,
    a default position is used.
    
    Args:
        target_directory (str): Directory for background image.
        car (Object): Car object. If provided, its bounding box is used.
        lane_positions (list): List of lanes, where each lane is a list of (x, y, z) coordinates.
        selected_lane_index (int): Lane index (0-based) to place the camera on if car is not provided.
        background (str): Name of the background image (without extension) in textures/Background.
        lane_offset_z (float): Vertical offset above the lane for camera placement.
    """
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.name = "Camera"
    selected_lane_index = camera_lane_number

    if car is not None and bpy.data.objects.get(car.name):
        # Use car-based placement
        def get_combined_bounding_box(obj):
            all_objects = [obj] + list(obj.children_recursive)
            coords = []
            for o in all_objects:
                if o.type == 'MESH':
                    for corner in o.bound_box:
                        world_corner = o.matrix_world @ Vector(corner)
                        coords.append(world_corner)
            if not coords:
                return None, None
            min_corner = Vector((min(v[i] for v in coords) for i in range(3)))
            max_corner = Vector((max(v[i] for v in coords) for i in range(3)))
            return min_corner, max_corner

        min_corner, max_corner = get_combined_bounding_box(car)
        center = (min_corner + max_corner) / 2
        dimensions = max_corner - min_corner
        car_length = dimensions.y
        car_height = dimensions.z
        car_width = dimensions.x

        camera_presets = {
            "behind_car": {
                "back_offset_multiplier": -2.0,
                "side_offset_multiplier": 0.5,
                "height_offset_multiplier": 0.5
            },
            "front_car": {
                "back_offset_multiplier": 1.0,
                "side_offset_multiplier": 0.0,
                "height_offset_multiplier": 0.5
            },
            "top_down": {
                "back_offset_multiplier": 0.0,
                "side_offset_multiplier": 0.0,
                "height_offset_multiplier": 5.0
            },
            "driver_view": {
                "back_offset_multiplier": 1.0,
                "side_offset_multiplier": 1.0,
                "height_offset_multiplier": 1.0
            }
        }
        preset = camera_presets["behind_car"]
        back_offset = Vector((0, car_length * preset["back_offset_multiplier"], 0))
        side_offset = Vector((car_width * preset["side_offset_multiplier"], 0, 0))
        height_offset = Vector((0, 0, car_height * preset["height_offset_multiplier"]))
        camera.location = center + back_offset + side_offset + height_offset

        direction = (center - camera.location).normalized()
        camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        print("[add_camera] Camera positioned based on car bounds.")
    elif lane_positions is not None and len(lane_positions) > selected_lane_index:
        # Use lane-based placement
        lane = lane_positions[selected_lane_index]
        if len(lane) < 2:
            # If only one point exists, use a default orientation
            pt = lane[0]
            camera.location = Vector((pt[0], pt[1], pt[2] + lane_offset_z))
            camera.rotation_euler = (math.radians(90), 0, 0)
            print("[add_camera] Only one lane point available; using default rotation.")
        else:
            first_pt = lane[0]
            second_pt = lane[1]
            camera.location = Vector((first_pt[0], first_pt[1], first_pt[2] + lane_offset_z))
            forward_dir = (Vector(second_pt) - Vector(first_pt)).normalized()
            camera.rotation_euler = forward_dir.to_track_quat('-Z', 'Y').to_euler()
            camera.rotation_euler.z += math.radians(-3) #offset by a 3 units in -z
            print(f"[add_camera] Camera placed at lane {selected_lane_index + 1} center, facing forward along the lane.")
    else:
        # Fallback default position
        print("[add_camera] Neither car nor lane positions available. Using default camera position.")
        camera.location = Vector((12.5, -58, 6.68))
        camera.rotation_euler = (math.radians(90), 0, 0)

    # Set as active camera
    bpy.context.scene.camera = camera

    # Background plane (preserving your existing setup)
    bpy.ops.mesh.primitive_plane_add(size=1)
    background_plane = bpy.context.object
    background_plane.name = "Background Plane"
    background_plane.scale = (900.0, 600.0, 0.0)
    background_plane.rotation_euler = camera.rotation_euler
    background_plane.location = (0.0, 700, 100)
    background_plane.parent = camera
    background_plane.matrix_parent_inverse = camera.matrix_world.inverted()

    material = bpy.data.materials.new(name="BackgroundMaterial")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    texture_node = nodes.new(type='ShaderNodeTexImage')
    output_node.location = (400, 0)
    principled_node.location = (200, 0)
    texture_node.location = (0, 0)
    path = f"{target_directory}/textures/Background/{background}.jpg"
    if os.path.exists(path):
        image = bpy.data.images.load(path)
        texture_node.image = image
    else:
        print(f"[add_camera] Background image not found at {path}")
        return
    links.new(texture_node.outputs["Color"], principled_node.inputs["Base Color"])
    links.new(texture_node.outputs['Color'], principled_node.inputs['Emission Color'])
    principled_node.inputs['Emission Strength'].default_value = 0.3
    links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])
    background_plane.data.materials.append(material)
    bpy.context.view_layer.objects.active = background_plane
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.cube_project()
    bpy.ops.object.mode_set(mode='OBJECT')

    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 1000

    #Motion blur
    scene.render.use_motion_blur = False
    scene.render.motion_blur_shutter = 2.0  # 0.5 is standard, tweak for intensity

    #Wide Angle Lens
    #camera.data.lens = 40  # Wide angle, dashcam-style
    #camera.data.sensor_width = 36  # Full-frame sensor size

    # --- Depth of Field ---
    #camera.data.dof.use_dof = True
    #camera.data.dof.focus_object = car  # Keep the car in focus
    #camera.data.dof.aperture_fstop = 1.5  # Lower = stronger background blur

    def add_jitter(camera, strength=0.01, scale=15.0):
        """
        Adds noise to the camera's rotation to simulate dashcam shake.
        
        :param camera: The camera object to apply shake to.
        :param strength: Intensity of shake (radians). Try 0.01–0.05 for realism.
        :param scale: How frequently the shake changes. Higher = smoother, lower = more jittery.
        """
        if camera.animation_data is None:
            camera.animation_data_create()

        if camera.animation_data.action is None:
            camera.animation_data.action = bpy.data.actions.new(name="CameraAction")


        for i, axis in enumerate(['rotation_euler']):
            for axis_idx in range(3):  # X, Y, Z
                fcurve = camera.animation_data.action.fcurves.find(axis, index=axis_idx)
                if fcurve is None:
                    fcurve = camera.animation_data.action.fcurves.new(data_path=axis, index=axis_idx)
                    fcurve.keyframe_points.insert(1, camera.rotation_euler[axis_idx])
                
                # Add a noise modifier
                noise = fcurve.modifiers.new(type='NOISE')
                noise.strength = strength
                noise.scale = scale
                noise.phase = 0
                noise.depth = 1

    #add_jitter(camera, strength=0.02, scale=10.0)
    return camera

class CameraController:
    """
    Controls camera movement
    
    3 Modes:
      - random: random camera movement, ensures traffic signs remain in view while providing different perspectives of the scene.
      - dashcam_linear: moves camera linearly along selected lane
      - dashcam_curved: uses raw lane points for a warped / curved road
    """

    def __init__(
        self,
        camera,
        road_boundaries,
        sign_name="Simple Sign",
        height_range=(4, 10),
        lane_positions=None,
        mode="dashcam",
        camera_lane_number=2
    ):
        """
        Args:
            camera: Blender camera object
            road_boundaries: list of (x, y, z) for road edges
            sign_name: name of the sign object in Blender
            height_range: (min_z, max_z) clamp for camera
            lane_positions: a list of lanes, each a list of (x, y, z) points
                            e.g. warp_scene returns [ [pt0, pt1, ...], [pt0, pt1, ...], ... ]
            mode: "random", "dashcam_linear", "dashcam_curved"
            selected_lane_index: user-chosen lane index (0-based)
        """
        self.camera = camera
        self.road_boundaries = road_boundaries
        self.sign_obj = bpy.data.objects.get(sign_name)
        if not self.sign_obj:
            raise ValueError(f"Sign object '{sign_name}' not found in scene")
        
        self.sign_position = self.sign_obj.location.copy()

         # Store initial position to avoid straying too far
        self.initial_position = self.camera.location.copy()

        self.height_range = height_range
        self.mode = mode

        # Basic boundary data
        self.road_start_y = min(p[1] for p in road_boundaries)
        self.road_end_y   = max(p[1] for p in road_boundaries)
        self.road_left_x  = min(p[0] for p in road_boundaries)
        self.road_right_x = max(p[0] for p in road_boundaries)
        self.road_width   = self.road_right_x - self.road_left_x
        self.road_length  = self.road_end_y   - self.road_start_y

        
        # Lane positions
        self.lane_positions = lane_positions or []  # list of lanes
        self.selected_lane_index = camera_lane_number

        #Set up tracking history to avoid repeating positions
        self.position_history = []
        self.max_history = 10
        self.movement_ranges = {
            'x': (-self.road_width * 0.1, self.road_width * 0.1),
            'y': (-25, 25),
            'z': (-1, 1)
        }
        self.failed_attempts = 0
        self.max_failed_attempts = 5

        # dashcam mode
        self.use_dashcam_lane = [] #store the lane index

        # curved mode using raw lane points from warp_scene
        self.curved_lane_points = []
        if self.lane_positions:
            if 0 <= self.selected_lane_index < len(self.lane_positions):
                self.curved_lane_points = self.lane_positions[self.selected_lane_index]
            else:
                print(f"[CameraController] Invalid selected_lane_index={self.selected_lane_index}, using lane 3.")
                self.curved_lane_points = self.lane_positions[2]

        # For the curved approach, track index
        self.current_lane_point_index = 0
        self.used_initial_camera_loc = False  # So the first call doesn't jump

        # Store camera’s original location from add_camera
        self.initial_camera_location = self.camera.location.copy()

        print(f"[CameraController] mode={self.mode}, selected_lane_index={self.selected_lane_index}")
        if self.lane_positions:
            print(f" - Found {len(self.lane_positions)} lanes total")

    def step(self, step_size):
        """
        
        If self.mode=='dashcam', move along the lane with optional jitter.
        If self.mode=='random', pick a random offset. Then face the sign,
        check if it’s in view, etc. Return True if sign is in view.
        """
        if self.mode == "dashcam_linear" and self.dashcam_lane:
            return self._dashcam_linear(step_size)
        elif self.mode == "dashcam":
            return self.dashcam_curved()
        else:
            return self._random_step()

    # Random movement 
    def _random_step(self):
        old_loc = self.camera.location.copy()
        old_rot = self.camera.rotation_euler.copy()

        if len(self.position_history) >= self.max_history:
            self.position_history.pop(0)
        self.position_history.append(tuple(old_loc))

        for attempt in range(10):
            # random offsets
            dx = random.uniform(*self.movement_ranges['x'])
            dy = random.uniform(*self.movement_ranges['y'])
            dz = random.uniform(*self.movement_ranges['z'])

            new_pos = self.camera.location + Vector((dx, dy, dz))
            new_pos = self.clamp_position(new_pos)

            # skip if too similar to recent
            if any((Vector(p) - new_pos).length < 2.0 for p in self.position_history[-3:]):
                continue

            self.camera.location = new_pos
            if not self.is_position_on_road(new_pos):
                self.move_towards_road_center()

            self.adjust_to_view_sign()
            if self.is_sign_in_view():
                self.failed_attempts = 0
                return True

        # fallback
        self.failed_attempts += 1
        if self.failed_attempts >= self.max_failed_attempts:
            print("[CameraController] random: failed -> reset near sign")
            self.camera.location = Vector((
                self.sign_position.x - random.uniform(40, 50),
                self.sign_position.y - random.uniform(50, 60),
                self.height_range[0] + random.uniform(2,4)
            ))
            self.failed_attempts = 0
            self.adjust_to_view_sign()
        else:
            # revert
            self.camera.location = old_loc
            self.camera.rotation_euler = old_rot
            sign_dir = self.get_sign_direction()
            self.camera.location += sign_dir*random.uniform(3,8)
            self.adjust_to_view_sign()

        return self.is_sign_in_view()

    #dashcam movement: straight lane
    def dashcam_linear(self, step_size=1.0):
        """
        - The camera remains at its initial position.
        - On subsequent calls, camera is moved forward along the y-axis by step_size,
        - camera rotation stays fixed
        """

        #initial dashcam location
        if not hasattr(self, 'used_initial_dashcam_loc'):
            self.used_initial_dashcam_loc = False
        if not self.used_initial_dashcam_loc:
            print("[dashcam_linear] Using the camera's existing location from add_camera for the first step.")
            self.used_initial_dashcam_loc = True

            # Also store the initial x,z
            self.dashcam_init_x = self.camera.location.x
            self.dashcam_init_z = self.camera.location.z

            return True

        # After the first step, just move the camera forward in y,
        # keeping x and z the same as the initial dashcam location.
        current_loc = self.camera.location.copy()

        # Increment y by the step_size
        new_y = current_loc.y + step_size

        new_pos = Vector((self.dashcam_init_x, new_y, self.dashcam_init_z))
        # clamp it inside the road region or below min_z
        new_pos = self.clamp_position(new_pos)

        # Assign camera location
        self.camera.location = new_pos

        # Update the view layer so the camera's transform is applied
        bpy.context.view_layer.update()
        return True
    
    #dashcam along curved road
    def dashcam_curved(self, step_size=1, height_offset=7.0):# sign_factor=0.1, local_blend=0.4, window_size=1):
        """
        Moves the camera along self.curved_lane_points.
       
        """
        # Ensure lane_positions is available.
        if not (self.lane_positions and len(self.lane_positions) > 0):
            print("No lane positions available; cannot dashcam.")
            return False

        # Get the list of raw lane points for the selected lane.
        try:
            lane_points = self.lane_positions[self.selected_lane_index]
        except IndexError:
            print("Selected lane index out of range.")
            return False

        # Initialize if no index
        if not hasattr(self, 'current_lane_point_index'):
            self.current_lane_point_index = 0

        # Get the current lane point.
        current_index = self.current_lane_point_index
        current_point = lane_points[current_index]
        print(f"Camera moving to lane point index {current_index}: {current_point}")

        # Add a height offset to the z coordinate so the camera is above the road.
        camera_position = Vector((current_point[0], current_point[1], current_point[2] + height_offset))
        self.camera.location = camera_position

        # Determine the forward direction.
        if current_index < len(lane_points) - 1:
            next_point = lane_points[current_index + 1]
            forward_direction = (Vector(next_point) - Vector(current_point)).normalized()
        else:
            forward_direction = Vector((0, 1, 0))  # Default forward if at the last point

        # Rotate the camera to face the forward direction.
        self.camera.rotation_euler = forward_direction.to_track_quat('-Z', 'Y').to_euler()

        # Advance the index by step_size.
        self.current_lane_point_index = (current_index + int(step_size)) % len(lane_points)

        # Update the scene so that changes are applied.
        bpy.context.view_layer.update()
        
        return True
    
    #camera helper methods
    def is_position_on_road(self, position):
        """Check if a position is within the road boundaries (with buffer)."""
        buffer_x = self.road_width * 0.1
        return (self.road_left_x + buffer_x <= position[0] <= self.road_right_x - buffer_x
                and self.road_start_y <= position[1] <= self.road_end_y)

    def is_sign_in_view(self, margin=0.15, eps=1e-3):
        """
        Check if the sign is fully visible from the camera location
        (all bounding-box corners in front & within the camera frustum).
        """
        scene = bpy.context.scene
        bbox_corners = [self.sign_obj.matrix_world @ Vector(corner)
                        for corner in self.sign_obj.bound_box]

        projected = [
            bpy_extras.object_utils.world_to_camera_view(scene, self.camera, c)
            for c in bbox_corners
        ]
        camera_matrix = self.camera.matrix_world.inverted()

        # Check corners in view
        for co in projected:
            # co.x, co.y in [0..1], but we allow margin
            if not (-margin - eps <= co.x <= 1+margin+eps and
                    -margin - eps <= co.y <= 1+margin+eps):
                return False

        # Check corners are in front (Blender camera sees negative Z)
        for c in bbox_corners:
            if (camera_matrix @ c).z > 0:
                # If z>0 means behind camera in Blender
                return False

        return True

    def get_sign_direction(self):
        """Unit vector from camera to sign."""
        return (self.sign_obj.location - self.camera.location).normalized()

    def adjust_to_view_sign(self):
        """Rotate camera to face sign, ignoring roll."""
        direction = self.get_sign_direction()
        track_quat = direction.to_track_quat('-Z', 'Y')
        self.camera.rotation_euler = track_quat.to_euler()
        self.camera.rotation_euler.z = 0  # zero out roll

    def clamp_position(self, pos):
        """Prevent going off the road region, clamp Z to height_range."""
        buffer_val = self.road_width * 0.1
        x = max(self.road_left_x+buffer_val, min(pos.x, self.road_right_x-buffer_val))
        y = max(self.road_start_y, min(pos.y, self.road_end_y))
        z_min, z_max = self.height_range
        z = max(z_min, min(pos.z, z_max))
        return Vector((x, y, z))

    def move_towards_road_center(self):
        """Nudge camera back toward center of road if it's off-limits."""
        rx = (self.road_left_x + self.road_right_x)*0.5
        ry = (self.road_start_y + self.road_end_y)*0.5
        loc = self.camera.location
        self.camera.location.x += (rx - loc.x)*0.05
        self.camera.location.y += (ry - loc.y)*0.05

