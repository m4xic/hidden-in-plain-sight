from PIL import Image
import sys
import os
import io
import argparse
import jpeg_zip as jz
from copy import copy
import exif
import time
from pattern import pattern_create as pc
import lsb

sizes = [[800,600],[1280,720],[2048,2048]]

payloads = {
    'small': {
        'exif': 15000,
        'image': 0.05,
        'zip': 0.5
    },
    'medium': {
        'exif': 31000,
        'image': 0.20,
        'zip': 1
    },
    'large': {
        'exif': 63000,
        'image': 0.35,
        'zip': 2
    }
}

def do_stego(base_image, output_folder):
    try:
        os.mkdir(output_folder)
    except:
        input("[!] Output folder already exists! Files may be overwritten. Press ENTER to continue.")

    # For each width and height combination...
    for width, height in sizes:
        # Create empty BytesIO objects to store a PNG and JPEG representation of the image
        jpeg_bytes, png_bytes = io.BytesIO(), io.BytesIO()
        with Image.open(args.base_image).resize((width, height)) as image:
            # Save the image as a JPEG to the JPEG BytesIO
            image.save(jpeg_bytes, 'jpeg', quality=95, subsampling=0)
            # Save the image as a PNG to the PNG BytesIO
            image.save(png_bytes, 'png')
        for payload_size in payloads.keys():
            # For each payload size...
            print(f"[!] {payload_size} for {width}x{height}...")

            # Generate the payload file for the LSB method
            lsb_size = int((width*height)*(payloads[payload_size]['image']))
            # If the LSB payload file doesn't exist...
            if not os.path.exists(f'{output_folder}/{width}x{height}-{payload_size}.txt'):
                # Open a file with the specific naming convention (for later access)
                with open(f'{output_folder}/{width}x{height}-{payload_size}.txt', 'w+') as payload_file:
                    # Use pattern_create to generate a payload of the correct length
                    payload_file.write(pc(length=lsb_size))

            # Generate the payload file for the EXIF method
            if not os.path.exists(f'{output_folder}/exif-{payload_size}.txt'):
                with open(f'{output_folder}/exif-{payload_size}.txt', 'w+') as exif_payload_file:
                    exif_payload_file.write(pc(length=payloads[payload_size]['exif']))

            # Generate a payload file for the ZIP method
            zip_size = int((width*height)*(payloads[payload_size]['zip']))
            if not os.path.exists(f'{output_folder}/{width}x{height}-zip-{payload_size}.txt'):
                with open(f'{output_folder}/{width}x{height}-zip-{payload_size}.txt', 'w+') as zip_payload_file:
                    zip_payload_file.write(pc(length=zip_size))

            # EXIF steganography
            # Create a copy of the JPEG bytes
            exif_bytes = copy(jpeg_bytes)
            # Open the image using the exif library
            exif_image = exif.Image(exif_bytes.getvalue())

            # Set the artist tag to the value of the EXIF payloas file
            with open(f'{output_folder}/exif-{payload_size}.txt', 'r') as exif_payload_file:
                exif_image.set('artist', exif_payload_file.read())

            # Write out the resulting file with the EXIF tag added
            with open(output_folder + f'/{width}x{height}-exif-{payload_size}.jpg', 'wb+') as f:
                f.write(exif_image.get_file())

            # LSB steganography
            # Open a temporary PNG file and write the PNG bytes in to it
            with open(f'{output_folder}/temp.png', 'wb+') as f:
                f.write(copy(png_bytes).getvalue())

            # Open the temporary file and use the LSB module to create a numpy array with the message embedded
            with open(f'{output_folder}/{width}x{height}-{payload_size}.txt', 'r') as payload_file:
                lsb_array = lsb.write_array_to_image(lsb.message_to_binary(payload_file.read(), "0001811954000"), f'{output_folder}/temp.png')

            # Create an image from the numpy array using PIL and save the new image
            lsb_image = Image.fromarray(lsb_array)
            lsb_image.save(f'{output_folder}/{width}x{height}-lsb-{payload_size}.png')

            # DCT steganography
            # > Done in Linux under OutGuess

            # ZIP steganography
            # Open the ZIP payload and create a JPEG-ZIP file with the hidden message inside
            with open(f'{output_folder}/{width}x{height}-zip-{payload_size}.txt', 'r') as payload_file:
                jpeg_bytes = jz.jpeg_steg(copy(jpeg_bytes), {'hidden.txt': payload_file.read()})

            # Write out the stegged ZIP file
            with open(f'{output_folder}/{width}x{height}-zip-{payload_size}.jpg', 'wb+') as output_file:
                output_file.write(jpeg_bytes.getvalue())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a set of images to test how websites perform steganography')
    # Allow input of exactly one image file
    parser.add_argument('base_image', metavar='B', type=str, help='the base image file you will be resizing')
    # Allow input of exactly one output folder
    parser.add_argument('result_folder', metavar='O', type=str, help='the folder of the results')
    # Parse the command line arguments
    args = parser.parse_args()

    do_stego(args.base_image, args.result_folder)