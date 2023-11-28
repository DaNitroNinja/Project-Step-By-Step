from PIL import Image, ImageDraw, ImageFont

def create_step(image, caption, margin=10, font_size=12):
    draw = ImageDraw.Draw(image)
    
    # Choose a larger font size
    font = ImageFont.truetype("arial.ttf", font_size)

    # Calculate the size of the text
    text_width, text_height = draw.textbbox((0, 0), caption, font=font)[:2]

    # Calculate the position to anchor the caption with margin
    text_position = (margin, image.height - text_height - margin)

    # Draw the background rectangle for the caption
    background_position = (text_position[0] - margin, text_position[1] - margin)
    background_size = (text_position[0] + text_width + margin, text_position[1] + text_height + margin)
    draw.rectangle([background_position, background_size], fill="black")

    # Draw the caption on the image
    draw.text(text_position, caption, font=font, fill="white")

    return image

# Example usage
image = Image.new("RGB", (300, 200), "white")
captioned_image = create_step(image, "Step 1: Example Caption", margin=20, font_size=16)
captioned_image.show()
