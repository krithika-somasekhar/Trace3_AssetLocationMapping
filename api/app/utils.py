import cv2
import numpy as np
from PIL import Image
from pdf2image import convert_from_bytes

def process_floor_plan_image(file_stream, file_ext, grid_size):
    try:
        if file_ext == 'pdf':
            # Handle PDF
            pdf_bytes = file_stream.read()
            images = convert_from_bytes(pdf_bytes)
            if not images:
                return None, 'No pages found in PDF file.'
            # Process the first page
            image = images[0]
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        else:
            # Handle image file
            file_bytes = np.frombuffer(file_stream.read(), np.uint8)
            opencv_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            if opencv_image is None:
                return None, 'Failed to decode image file.'

        # Apply grid overlay
        image_with_grid = apply_grid_overlay(opencv_image, grid_size)
        return image_with_grid, None
    except Exception as e:
        return None, f'Error processing image: {str(e)}'

def apply_grid_overlay(image, grid_size):
    image_with_grid = image.copy()
    height, width = image_with_grid.shape[:2]
    grid_color = (0, 0, 255)  # Red color in BGR

    # Draw vertical lines and labels
    for x in range(0, width, grid_size):
        cv2.line(image_with_grid, (x, 0), (x, height), grid_color, 1)
        for y in range(0, height, grid_size):
            cv2.putText(image_with_grid, f'({x // grid_size},{y // grid_size})',
                        (x + 2, y + 15), cv2.FONT_HERSHEY_SIMPLEX,
                        0.4, grid_color, 1)

    # Draw horizontal lines
    for y in range(0, height, grid_size):
        cv2.line(image_with_grid, (0, y), (width, y), grid_color, 1)

    return image_with_grid
