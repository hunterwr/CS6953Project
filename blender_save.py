import bpy

def render_and_save(output_path, frame_number, samples=32):
    
    scene = bpy.context.scene
    #Continue animation to update particles in scene
    #frame_number = 450 -set to arbitary value
    for i in range(1, frame_number + 1):
        scene.frame_set(i)

    scene.frame_set(frame_number) #set desired frame for output
    scene.render.filepath = output_path
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    scene.cycles.samples = samples

    scene.render.image_settings.file_format = 'PNG'

    # Render and save the image
    bpy.ops.render.render(write_still=True)

    return