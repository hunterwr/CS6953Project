import bpy

def render_and_save(output_path):
    
    bpy.context.scene.render.filepath = output_path
    
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.cycles.samples = 512

    # Set the image format (PNG, JPEG, etc.)
    bpy.context.scene.render.image_settings.file_format = 'PNG'  # Change to any format as needed

    # Render and save the image
    bpy.ops.render.render(write_still=True)

    return
    
