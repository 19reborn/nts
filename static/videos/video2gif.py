import cv2
import imageio
import numpy as np
from PIL import Image, ImageEnhance

def mp4_to_gif_cv2(input_mp4, output_gif):
    """ Convert an MP4 video to a high-quality GIF while preserving original brightness. """

    # Open video file
    cap = cv2.VideoCapture(input_mp4)
    fps = cap.get(cv2.CAP_PROP_FPS)  # Get original FPS
    frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert BGR (OpenCV) to RGB (PIL format)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)

        # **Brightness Correction** (Fix dark GIFs)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.1)  # Adjust brightness (1.0 = original, 1.1 = slightly brighter)

        # Convert image to optimized palette-based GIF with Floyd-Steinberg dithering
        img = img.convert("P", palette=Image.ADAPTIVE, colors=256, dither=Image.FLOYDSTEINBERG)
        frames.append(img)

    cap.release()  # Release video capture

    # Save as GIF with optimized brightness & color
    frames[0].save(
        output_gif, 
        save_all=True, 
        append_images=frames[1:], 
        duration=int(1000 / fps),  # Convert FPS to milliseconds per frame
        loop=0, 
        optimize=True
    )

    print(f"Conversion completed! GIF saved as {output_gif}")

# Example usage
input_mp4 = "static/videos/intro_demo.mp4"
output_gif = input_mp4.replace(".mp4", ".gif")
mp4_to_gif_cv2(input_mp4, output_gif)
