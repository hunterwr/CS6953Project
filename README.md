# CS6953Project

## Run Arguments
**road_scene:** 

**road_conditions:** 

**sign:** 
'Stop Sign'

**road_width**
Road width.

**road_length**

**camera_location**

**camera_rotation**

**camera_scale**

**light_location**

**light_power**

**light_angle**

**time_of_day**
Time of day. E.g. day, midday, dusk

**ground_plane_size:**
Land ground plane size.

**plane:**
Land ground texture. E.g. rock, snow, mud, forest

**background:**
Background scene. E.g. sky, desert, city

**density:**
How many trees. E.g. no trees, some trees, many trees

**distance:** 
How far the trees are from the road.

**tree_type:**
Type of tree.

**particle_density:**
The density of rain or snow.

**start_frame**

**end_frame**

**samples**
Rendering samples.

**num_steps:**
How many steps the camera will move toward the sign.

**step_size:**
The step size camera move toward the sign.

# How to run blender headless with python script.
```bash
/path/to/Blender -b --python run.py
```

# Scene Generation Parameter List

  "road_scene": "Highway", "Two Lane" 
  "road_conditions": "Dry", "Wet"
  "sign" : "All Way Stop", "Bump", "Center Lane Turn", "Chevron", "Cross Road", "DIP", "Divided Highway Ahead", "Divided Highway Ends", "Divided Highway", "Do Not Pass", "Double Curve", "Keep
            Right", "Left Curve", "Left Turn Only", "Loose Gravel", "Low Clearance", "Merging Traffic", "Minimum Speed 40", "Narrow Bridge Ahead", "No Left Turn On Red", "No Left Turn", "No Passing Zone", "No Pedestrian Crossing", "No Right Turn On Red", "No Turn On Red", "No Turns", "No U-Turn", "One Way", "Pass With Care", "Pavement Ends", "Railroad Crossing", "Restricted Lane Ahead", "Right Curve", "Right Lane Ends", "Right Turn Only", "Right Turn Signal", "Road Closed", "Roadabout Traffic", "Sharp Left Turn", "Sharp Right Turn", "Side Road", "Slower Traffic Keep Right", "Soft Shoulder", "Speed Limit 50", "Stop", "T Intersection", "Turn Left Or Right", "Two Way Traffic", "Wrong Way", "Y Intersection", "Yield"
  "scratches": 0.0 to 1.0 
  "rust": 0.0 to 1.0 
  "snow": 0.0 to 1.0 
  "mud": 0.0 to 1.0 
  "camera_location": "12.5, -58, 6.68",
  "camera_rotation": "90, 0, 0",
  "camera_scale": 1.0,
  "light_location": "-28.398,59.799,19.12",
  "light_power": 3.0,
  "light_angle": 180,
  "time_of_day": "dawn",
  "ground_plane_size": 1000,
  "plane": "snow",
  "background": "sky",
  "density": "some trees",
  "distance": "close",
  "tree_type": "pine",
  "snow_type": "moderate",
  "frame_number": 450,
  "samples": 128,
  "num_steps": 1,
  "step_size": 5