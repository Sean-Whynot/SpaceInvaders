from PIL import Image, ImageDraw
import random

def generate_starfield(width, height, num_stars, output_path):
    # Create a new black image
    image = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Add stars
    for _ in range(num_stars):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        # Vary star brightness
        brightness = random.randint(50, 255)
        draw.point((x, y), fill=(brightness, brightness, brightness))

    # Save the image
    image.save(output_path)

if __name__ == "__main__":
    generate_starfield(1920, 1080, 500, 'Images/background.png')
