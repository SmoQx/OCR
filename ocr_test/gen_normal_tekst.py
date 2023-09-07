import random
from faker import Faker
from PIL import ImageDraw, ImageFont, Image
import os
from pathlib import Path


def rand_word_gen(how_many=1):
    # Create a Faker instance with the desired language
    fake = Faker('pl_PL')  # 'pl_PL' is the locale for Polish language
    # Generate random words
    random_word = ''
    for y in range(how_many):
        random_word += (fake.word() + ' ')
    return random_word


def gen_random_page(word_min: int = 1, word_max: int = 2):
    generated_page = ''
    for w in range(random.randint(1, 3)):
        for y in range(random.randint(1, 10)):
            generated_page += (rand_word_gen(random.randint(word_min, word_max)) + "\n")
        for z in range(random.randint(0, 3)):
            generated_page += "\n"
    return generated_page


def convert_text_to_png(input_file, output_file, font_size):
    if os.path.exists(input_file):
        # Read text from input file
        with open(input_file, 'r') as file:
            text = file.read()
    else:
        text = input_file


    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"  # Replace with the actual path to your font file
    font = ImageFont.truetype(font_path, font_size)

    # Create a temporary image to calculate text size
    temp_image = Image.new('RGB', (1, 1))
    temp_draw = ImageDraw.Draw(temp_image)

    # Get text size
    text_width, text_height = temp_draw.textbbox((0, 0), text, font=font)[2:]

    # Create a new image with white background
    image = Image.new('RGB', (text_width + 100, text_height + 80), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Render text onto the image
    draw.text((50, 50), text, font=font, fill=(0, 0, 0))

    # Save the image as a PNG file
    image.save(output_file, 'PNG')
    print("Image saved as", output_file)


if __name__ == '__main__':
    path_to_outputfile = Path("./temp/random.png")
    print(gen_random_page(10, 20))
    convert_text_to_png(gen_random_page(10, 20), path_to_outputfile, 30)
