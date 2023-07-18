import random
from PIL import ImageDraw, ImageFont, Image


def random_string_generator():
    lore_ipsum_str = "lore ipsum "
    random_string = ""
    for x in range(random.randint(0, 10)):
        random_string = lore_ipsum_str * x

    return random_string


def gen_random_page():
    generated_page = ''
    for w in range(random.randint(1, 3)):
        for y in range(random.randint(1, 10)):
            generated_page += (random_string_generator() + "\n")
        for z in range(random.randint(0, 3)):
            generated_page += "\n"
    return generated_page


def convert_text_to_png(input_file, output_file, font_size):
    # Read text from input file
    with open(input_file, 'r') as file:
        text = file.read()


    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"  # Replace with the actual path to your font file
    font = ImageFont.truetype(font_path, font_size)

    # Create a temporary image to calculate text size
    temp_image = Image.new('RGB', (1, 1))
    temp_draw = ImageDraw.Draw(temp_image)

    # Get text size
    text_width, text_height = temp_draw.textbbox((0, 0), text, font=font)[2:]

    # Create a new image with white background
    image = Image.new('RGB', (text_width + 20, text_height + 20), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Render text onto the image
    draw.text((10, 10), text, font=font, fill=(0, 0, 0))

    # Save the image as a PNG file
    image.save(output_file, 'PNG')
    print("Image saved as", output_file)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open('lore_ipsum.txt', 'w') as save_lore_text:
        save_lore_text.write(gen_random_page())

    input_filename = "lore_ipsum.txt"
    output_filename = "lore_ipsum2.png"
    font_size = 14

    convert_text_to_png(input_filename, output_filename, font_size)
    """font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"  # Replace with the actual path to your font file
    font = ImageFont.truetype(font_path, font_size)
    print(font.font_variant())"""
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
