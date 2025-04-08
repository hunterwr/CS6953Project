from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

def overlay_bbox(image_path, bbox_file):
    # Load the image
    image = Image.open(image_path)
    
    # Read the bounding box data from the text file
    with open(bbox_file, 'r') as file:
        bbox_data = file.readline().strip().split()
    
    # Extract the bounding box values
    x, y, width, height = map(int, bbox_data)

    # Draw the bounding box on the image
    draw = ImageDraw.Draw(image)
    
    # Draw a rectangle: (x, y) is the top-left corner, (x+width, y+height) is the bottom-right corner
    draw.rectangle([x, y, x + width, y + height], outline="red", width=3)

    # Show the image with the bounding box
    plt.imshow(image)
    plt.axis('off')  # Hide axes
    plt.show()

# Example usage:
image_path = r'./output/samples17/images/image_1_20250408001410_a9cb23.png'  # Replace with the path to your image
bbox_file = r'output/samples17/labels/image_1_20250408001410_a9cb23_bbox.txt'  # Replace with the path to your bounding box file
overlay_bbox(image_path, bbox_file)

