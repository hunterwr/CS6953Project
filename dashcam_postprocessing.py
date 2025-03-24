import cv2
import numpy as np
import random
import os
import argparse
from typing import Tuple, Optional

def apply_motion_blur(image, kernel_size=7, angle=90):
    """Apply motion blur to simulate camera movement"""
    # Create the motion blur kernel
    kernel = np.zeros((kernel_size, kernel_size))
    kernel[int((kernel_size-1)/2), :] = np.ones(kernel_size)
    kernel = kernel / kernel_size
    
    # Apply the custom kernel
    blurred = cv2.filter2D(image, -1, kernel)
    return blurred

def apply_stronger_motion_blur(image, strength=1.0):
    """Apply a stronger motion blur with random direction"""
    kernel_size = int(9 + 12 * strength)
    if kernel_size % 2 == 0:  # Ensure kernel size is odd
        kernel_size += 1
    
    # Create a motion blur kernel with random angle
    angle = random.randint(75, 105)  # Mostly horizontal but with variation
    
    # Create the motion blur kernel with angle
    kernel = np.zeros((kernel_size, kernel_size))
    
    # Calculate points on a line with the given angle
    center = kernel_size // 2
    for i in range(kernel_size):
        # Calculate position using angle
        x = center + int(np.cos(np.radians(angle)) * (i - center))
        y = center + int(np.sin(np.radians(angle)) * (i - center))
        
        if 0 <= x < kernel_size and 0 <= y < kernel_size:
            kernel[y, x] = 1
    
    # Normalize the kernel
    kernel = kernel / np.sum(kernel)
    
    # Apply the custom kernel
    blurred = cv2.filter2D(image, -1, kernel)
    return blurred

def apply_vignette(image, vignette_strength=0.7):
    """Apply a vignette effect around the edges"""
    height, width = image.shape[:2]
    
    # Create a vignette mask
    x_center = width // 2
    y_center = height // 2
    x = np.linspace(0, width - 1, width)
    y = np.linspace(0, height - 1, height)
    x, y = np.meshgrid(x, y)
    
    # Calculate distance from center
    dist = np.sqrt((x - x_center) ** 2 + (y - y_center) ** 2)
    
    # Normalize the distance
    max_dist = np.sqrt(x_center ** 2 + y_center ** 2)
    dist = dist / max_dist
    
    # Create the vignette mask
    mask = 1 - vignette_strength * dist
    mask = np.clip(mask, 0, 1)
    
    # Apply the mask to each channel
    for i in range(3):
        image[:, :, i] = image[:, :, i] * mask
    
    return image

def enhance_dynamic_range(image, strength=0.8):
    """Enhance the dynamic range to simulate poor HDR handling in dashcams"""
    # Create lookup table for a slight S-curve to increase contrast
    lookUpTable = np.empty((1, 256), np.uint8)
    for i in range(256):
        # Apply S-curve transformation
        value = 255 * (np.tanh((i/255.0 - 0.5) * (2 + 4 * strength)) * 0.5 + 0.5)
        lookUpTable[0, i] = np.clip(value, 0, 255)
    
    # Apply lookup table
    enhanced = cv2.LUT(image, lookUpTable)
    
    return enhanced

def simulate_overexposure(image, strength=0.6):
    """Simulate overexposed areas like in many dashcams"""
    # Create a mask for bright areas
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, bright_mask = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    
    # Expand bright areas slightly
    kernel = np.ones((5, 5), np.uint8)
    bright_mask = cv2.dilate(bright_mask, kernel, iterations=1)
    
    # Create overexposed version (whiter and lower contrast)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype("float32")
    hsv[:, :, 1] = hsv[:, :, 1] * 0.5  # Reduce saturation
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] + 30 * strength, 0, 255)  # Increase brightness
    overexposed = cv2.cvtColor(hsv.astype("uint8"), cv2.COLOR_HSV2BGR)
    
    # Blend original with overexposed areas
    result = image.copy()
    bright_mask = cv2.cvtColor(bright_mask, cv2.COLOR_GRAY2BGR) / 255.0
    result = image * (1 - bright_mask * strength) + overexposed * bright_mask * strength
    
    return result.astype(np.uint8)

def adjust_color_balance(image, contrast=1.1, brightness=0, saturation=1.1):
    """Adjust color balance to make the image look more like dashcam footage"""
    # Convert to HSV for better color manipulation
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype("float32")
    
    # Apply saturation adjustment
    hsv[:, :, 1] = hsv[:, :, 1] * saturation
    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
    
    # Apply value/brightness adjustment
    hsv[:, :, 2] = hsv[:, :, 2] * contrast + brightness
    hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
    
    # Convert back to BGR
    image = cv2.cvtColor(hsv.astype("uint8"), cv2.COLOR_HSV2BGR)
    
    return image

def add_noise(image, noise_level=10):
    """Add some random noise to simulate sensor imperfections"""
    # More realistic sensor noise with channel variance
    noise_r = np.random.randn(*image.shape[:2]) * noise_level * random.uniform(0.8, 1.2)
    noise_g = np.random.randn(*image.shape[:2]) * noise_level * random.uniform(0.8, 1.2)
    noise_b = np.random.randn(*image.shape[:2]) * noise_level * random.uniform(0.8, 1.2)
    
    noisy_img = image.copy().astype(np.float32)
    noisy_img[:, :, 0] += noise_b.reshape(image.shape[0], image.shape[1])
    noisy_img[:, :, 1] += noise_g.reshape(image.shape[0], image.shape[1])
    noisy_img[:, :, 2] += noise_r.reshape(image.shape[0], image.shape[1])
    
    return np.clip(noisy_img, 0, 255).astype(np.uint8)

def add_blocky_artifacts(image, block_size=8, strength=0.6):
    """Add blocky compression artifacts common in dashcams"""
    h, w = image.shape[:2]
    result = image.copy()
    
    # Process the image in blocks
    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            # Define the block region
            y_end = min(y + block_size, h)
            x_end = min(x + block_size, w)
            
            # Get the current block
            block = image[y:y_end, x:x_end].copy()
            
            # Apply block-level processing
            # 1. Average the colors slightly within blocks
            if random.random() < strength * 0.7:
                for c in range(3):
                    mean_val = np.mean(block[:, :, c])
                    block_strength = random.uniform(0.3, 0.7) * strength
                    block[:, :, c] = block[:, :, c] * (1 - block_strength) + mean_val * block_strength
            
            # 2. Enhance edges between blocks
            if x > 0 and random.random() < strength * 0.5:
                block[:, 0, :] = (block[:, 0, :] * 0.7 + block[:, 1, :] * 0.3).astype(np.uint8)
            
            if y > 0 and random.random() < strength * 0.5:
                block[0, :, :] = (block[0, :, :] * 0.7 + block[1, :, :] * 0.3).astype(np.uint8)
            
            # Update the result
            result[y:y_end, x:x_end] = block
    
    return result

def simulate_compression_artifacts(image, quality=85):
    """Simulate JPEG compression artifacts by recompressing the image"""
    # Save to a temporary file with compression
    temp_file = "temp_compressed.jpg"
    cv2.imwrite(temp_file, image, [cv2.IMWRITE_JPEG_QUALITY, quality])
    
    # Read back
    compressed_img = cv2.imread(temp_file)
    
    # Clean up
    if os.path.exists(temp_file):
        os.remove(temp_file)
    
    return compressed_img

def add_lens_flare(image, probability=0.2):
    """Occasionally add a simple lens flare effect"""
    if random.random() > probability:
        return image
    
    height, width = image.shape[:2]
    
    # Create a lens flare at a random position in the top portion of the image
    flare_x = random.randint(width // 3, width * 2 // 3)
    flare_y = random.randint(height // 4, height // 2)
    flare_size = min(width, height) // 8  # Smaller, more subtle flare
    
    # Calculate intensity based on distance from center
    y, x = np.ogrid[-flare_y:height-flare_y, -flare_x:width-flare_x]
    intensity = flare_size*flare_size / (x*x + y*y + 1)
    intensity = np.clip(intensity, 0, 1)
    
    # Apply the flare additively
    result = image.copy()
    
    # Create a more subtle, white-based flare
    flare_color = np.array([245, 245, 245])  # Almost white flare
    
    for c in range(3):
        result[:, :, c] = np.where(
            intensity > 0.05,
            np.clip(result[:, :, c] + intensity * flare_color[c] * 0.6, 0, 255),  # Reduced intensity
            result[:, :, c]
        )
    
    return result

def add_timestamp(image, opacity=0.8):
    """Add a typical dashcam timestamp to the image"""
    from datetime import datetime
    
    # Create a copy to avoid modifying the original
    result = image.copy()
    
    # Current date and time
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Add some random GPS coordinates sometimes
    if random.random() < 0.7:
        # Generate somewhat realistic but random coordinates
        lat = random.uniform(30, 45)
        lon = random.uniform(-120, -70)
        timestamp += f"   GPS: {lat:.6f}, {lon:.6f}"
    
    # Add a random company name sometimes
    companies = ["DashCam Pro", "RoadSafe", "DriveGuard", "SafetyView", "TripRecord"]
    if random.random() < 0.6:
        company = random.choice(companies)
        timestamp = company + "   " + timestamp
    
    # Position: bottom of the image
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    font_thickness = 2
    color = (255, 255, 255)  # White text
    
    # Get text size and position
    text_size = cv2.getTextSize(timestamp, font, font_scale, font_thickness)[0]
    text_x = 10
    text_y = image.shape[0] - 20
    
    # Add a semi-transparent background for the text
    overlay = result.copy()
    bg_top = text_y - text_size[1] - 10
    bg_bottom = result.shape[0]
    bg_left = 0
    bg_right = text_size[0] + 30
    cv2.rectangle(overlay, (bg_left, bg_top), (bg_right, bg_bottom), (0, 0, 0), -1)
    
    # Apply the overlay with transparency
    cv2.addWeighted(overlay, opacity, result, 1 - opacity, 0, result)
    
    # Add the text
    cv2.putText(result, timestamp, (text_x, text_y), font, font_scale, color, font_thickness)
    
    return result

def apply_auto_exposure(image, strength=0.5):
    """Simulate auto-exposure adjustments that dashcams make"""
    # Calculate the mean brightness of the image
    mean_brightness = np.mean(image)
    
    # Target brightness (mid-gray)
    target_brightness = 127
    
    # Calculate adjustment factor (how much to brighten/darken)
    # Use strength parameter to control how aggressive the adjustment is
    adjustment = (target_brightness - mean_brightness) * strength
    
    # Apply adjustment
    adjusted = image.astype(np.float32) + adjustment
    adjusted = np.clip(adjusted, 0, 255).astype(np.uint8)
    
    return adjusted

def apply_rolling_shutter(image, amount=3):
    """Simulate subtle rolling shutter effect sometimes seen in dashcam footage"""
    if amount <= 0:
        return image
        
    height, width = image.shape[:2]
    result = image.copy()
    
    # Calculate offset for each row
    for y in range(height):
        offset = int(np.sin(y / height * np.pi) * amount)
        if offset == 0:
            continue
            
        # Shift row by offset
        if offset > 0:
            result[y, offset:] = image[y, :-offset]
        else:
            offset = abs(offset)
            result[y, :-offset] = image[y, offset:]
    
    return result

def display_image(window_name: str, image, wait_key: int = 0, scale: float = 1.0):
    """
    Display an image in a window
    
    Args:
        window_name: Name for the window
        image: Image to display
        wait_key: Time to wait in ms (0 = wait until key pressed)
        scale: Scale factor for display (e.g., 0.5 for half size)
    """
    if scale != 1.0:
        h, w = image.shape[:2]
        new_h, new_w = int(h * scale), int(w * scale)
        display_img = cv2.resize(image, (new_w, new_h))
    else:
        display_img = image.copy()
    
    cv2.imshow(window_name, display_img)
    cv2.waitKey(wait_key)

def display_side_by_side(original: np.ndarray, processed: np.ndarray, 
                        title: str = "Original vs Processed", scale: float = 0.8) -> np.ndarray:
    """
    Display two images side by side for comparison
    
    Args:
        original: Original image
        processed: Processed image
        title: Window title
        scale: Display scale factor
        
    Returns:
        Combined image
    """
    # Create copies to avoid modifying originals
    orig = original.copy()
    proc = processed.copy()
    
    # Ensure both images have same height (take the smaller one)
    h1, w1 = orig.shape[:2]
    h2, w2 = proc.shape[:2]
    
    # Resize to match heights if needed
    if h1 != h2:
        target_h = min(h1, h2)
        aspect1 = w1 / h1
        aspect2 = w2 / h2
        w1_new = int(target_h * aspect1)
        w2_new = int(target_h * aspect2)
        orig = cv2.resize(orig, (w1_new, target_h))
        proc = cv2.resize(proc, (w2_new, target_h))
    
    # Add labels (Optional)
    cv2.putText(orig, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(proc, "Processed", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Combine images horizontally
    combined = np.hstack((orig, proc))
    
    # Display
    if scale != 1.0:
        h, w = combined.shape[:2]
        combined = cv2.resize(combined, (int(w*scale), int(h*scale)))
    
    cv2.imshow(title, combined)
    cv2.waitKey(1)  # Show without blocking
    
    return combined

def apply_dashcam_effects(image_path: str, strength: float = 0.7, 
                          visualize: bool = False, step_by_step: bool = False,
                          wait_time: int = 0) -> np.ndarray:
    """
    Apply various effects to make the image look like it was taken from a dashcam
    
    Args:
        image_path: Path to the input image
        strength: Overall effect strength (0.0 to 1.0)
        visualize: Whether to display the image at each step
        step_by_step: Wait for key press after each step
        wait_time: Time to wait between steps in ms (0 = wait for key press)
        
    Returns:
        Processed image
    """
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")
    
    # Keep original for comparison
    original = image.copy()
    current = image.copy()
    
    if visualize:
        display_image("Original Image", original, 1 if not step_by_step else wait_time)
    
    # Apply auto-exposure adjustment (common in dashcams) - more aggressive
    current = apply_auto_exposure(current, strength=0.6 * strength)
    if visualize:
        combined = display_side_by_side(original, current, "Step 1: Auto-exposure adjustment")
        if step_by_step:
            cv2.waitKey(wait_time)
    
    # Apply enhanced dynamic range
    current = enhance_dynamic_range(current, strength=0.9 * strength)
    if visualize:
        combined = display_side_by_side(original, current, "Step 2: Dynamic range enhancement")
        if step_by_step:
            cv2.waitKey(wait_time)
    
    # Apply stronger motion blur
    if random.random() < 0.9 * strength:
        current = apply_stronger_motion_blur(current, strength=strength)
        if visualize:
            combined = display_side_by_side(original, current, "Step 3: Motion blur")
            if step_by_step:
                cv2.waitKey(wait_time)
    
    # Apply color adjustments - dashcams often have lower color accuracy
    contrast = 1.0 + (0.4 * strength)
    saturation = 1.0 - (0.25 * strength)  # More desaturated
    brightness = random.randint(-15, 5)  # Slight random brightness shift
    current = adjust_color_balance(current, contrast=contrast, brightness=brightness, saturation=saturation)
    if visualize:
        combined = display_side_by_side(original, current, "Step 4: Color adjustment")
        if step_by_step:
            cv2.waitKey(wait_time)
    
    # Simulate overexposed areas (common in dashcams)
    current = simulate_overexposure(current, strength=0.8 * strength)
    if visualize:
        combined = display_side_by_side(original, current, "Step 5: Overexposure simulation")
        if step_by_step:
            cv2.waitKey(wait_time)
    
    # Add more significant vignette effect (common in cheaper lenses)
    current = apply_vignette(current, vignette_strength=0.5 * strength)
    if visualize:
        combined = display_side_by_side(original, current, "Step 6: Vignette effect")
        if step_by_step:
            cv2.waitKey(wait_time)
    
    # Add more substantial noise (sensor noise)
    current = add_noise(current, noise_level=10 * strength)
    if visualize:
        combined = display_side_by_side(original, current, "Step 7: Sensor noise")
        if step_by_step:
            cv2.waitKey(wait_time)
    
    # Add blocky artifacts first
    current = add_blocky_artifacts(current, block_size=8, strength=0.7 * strength)
    if visualize:
        combined = display_side_by_side(original, current, "Step 8: Blocky artifacts")
        if step_by_step:
            cv2.waitKey(wait_time)
    
    # Simulate compression artifacts (dashcams use heavy compression)
    quality = max(55 - int(35 * strength), 20)  # Much lower quality (20-55 range)
    current = simulate_compression_artifacts(current, quality=quality)
    if visualize:
        combined = display_side_by_side(original, current, "Step 9: Compression artifacts")
        if step_by_step:
            cv2.waitKey(wait_time)
    
    # Apply subtle rolling shutter effect
    if random.random() < 0.4 * strength:
        current = apply_rolling_shutter(current, amount=int(5 * strength))
        if visualize:
            combined = display_side_by_side(original, current, "Step 10: Rolling shutter")
            if step_by_step:
                cv2.waitKey(wait_time)
    
    # Show final comparison if visualizing
    if visualize:
        final_comparison = display_side_by_side(original, current, "Final Result: Original vs Dashcam")
        cv2.waitKey(0 if step_by_step else wait_time)
    
    return current

def process_and_save(image_path, strength=1.0, visualize=False, step_by_step=False):
    """Process an image and save it back to the same location"""
    try:
        # Apply dashcam effects
        processed_image = apply_dashcam_effects(
            image_path, 
            strength=strength,
            visualize=visualize,
            step_by_step=step_by_step
        )
        
        # Save back to the original path
        cv2.imwrite(image_path, processed_image)
        
        return True
    except Exception as e:
        print(f"Error processing image {image_path}: {str(e)}")
        return False

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Apply dashcam-like effects to an image')
    
    parser.add_argument('image_path', type=str, help='Path to the input image')
    parser.add_argument('--output', '-o', type=str, help='Path to save the output image (if not specified, displays only)')
    parser.add_argument('--strength', '-s', type=float, default=1.0, help='Effect strength (0.0 to 1.0)')
    parser.add_argument('--visualize', '-v', action='store_true', help='Visualize each step')
    parser.add_argument('--step-by-step', '-b', action='store_true', help='Wait for key press after each step')
    parser.add_argument('--wait-time', '-w', type=int, default=0, help='Time to wait between steps in ms (0 = wait for key press)')
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    if not os.path.exists(args.image_path):
        print(f"Error: Image file not found: {args.image_path}")
        exit(1)
    
    try:
        # Apply effects with visualization
        processed = apply_dashcam_effects(
            args.image_path,
            strength=args.strength,
            visualize=True,  # Always visualize when running as script
            step_by_step=args.step_by_step,
            wait_time=args.wait_time
        )
        
        # Save if output path is provided
        if args.output:
            cv2.imwrite(args.output, processed)
            print(f"Processed image saved to: {args.output}")
        
        print("\nPress any key to exit...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)
