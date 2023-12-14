# image_crypt.py

from PIL import Image
import os


def embed_text(image_path, python_code, start_marker="#Yvqgmp^o#", end_marker="#9r&7vY#"):
    binary_code = ''.join(format(ord(char), '08b') for char in (start_marker + python_code + end_marker))

    image = Image.open(image_path)
    file_name, file_extension = os.path.splitext(os.path.basename(image_path))
    width, height = image.size
    pixels = image.load()

    binary_index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            if binary_index < len(binary_code):
                r = (r & 0xFE) | int(binary_code[binary_index])
                binary_index += 1

            pixels[x, y] = (r, g, b)

    output_folder = 'out'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_path = os.path.join(output_folder, f'{file_name}_embed{file_extension}')
    image.save(output_path)


def extract_text(image_path, start_marker="#Yvqgmp^o#", end_marker="#9r&7vY#"):
    image = Image.open(image_path)
    width, height = image.size
    pixels = image.load()

    extracted_binary = ''
    for y in range(height):
        for x in range(width):
            r, _, _ = pixels[x, y]
            extracted_binary += str(r & 1)

    extracted_chars = [extracted_binary[i:i+8] for i in range(0, len(extracted_binary), 8)]
    extracted_text = ''.join(chr(int(char, 2)) for char in extracted_chars)

    if start_marker in extracted_text and end_marker in extracted_text:
        start_index = extracted_text.find(start_marker) + len(start_marker)
        end_index = extracted_text.find(end_marker)
        extracted_code = extracted_text[start_index:end_index]
        return extracted_code.strip()
    else:
        return None
