# SOURCES USED
# [1] Stack Overflow. 2021. how the Image.ImageFont.ImageFont.getsize() command works?. [online] Available at: <https://stackoverflow.com/a/55801151> [Accessed 6 March 2021].

from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
import os
import io
import argparse
import jpeg_zip as jz
import exif_spam as es 

sizes = [[2048,2048], [1024,1024], [512,512], [256,256], [128,128], [1920,1080], [1280,720], [858,480], [480,360], [256,144], [2048,1536], [1280,1024], [1024,768], [800,600], [640,400]]

def resize(base_image, size, extension):
    width, height = size
    output_image = io.BytesIO()
    caption = str(width) + "x" + str(height) + "-" + extension
    image = Image.open(base_image).resize((width, height))
    font = ImageFont.load_default()
    text_w, text_h = font.getsize(caption) # [1]
    ImageDraw.Draw(image).text((width-text_w-5, height-text_h-2),caption,(0, 0, 0))
    image.save(output_image, extension, quality=95, subsampling=0)
    return output_image

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a set of test images to see how services process images')
    # Allow input of exactly one image file
    parser.add_argument('base_image', metavar='B', type=str, help='the base image file you will be resizing')
    # Allow input of at least one output filetype
    parser.add_argument('filetypes', metavar='F', type=str, help='a comma-separated list of file types')
    # Allow input of exactly one output folder
    parser.add_argument('output_folder', metavar='O', type=str, help='the folder you want to output to')
    # Allow input of at least one hidden file
    parser.add_argument('hide_files', metavar='H', type=str, nargs='*', help='the file (or files) you want to hide in the ZIP archive')
    # Parse the command line arguments
    args = parser.parse_args()


    base_image = args.base_image
    filetypes = args.filetypes.split(',')
    for ftype in filetypes: ftype = ftype.lower()

    # Standardise the file types
    if "jpg" in filetypes:
        filetypes.remove('jpg')
        filetypes.append('jpeg')

    output_folder = args.output_folder
    hide_files = args.hide_files

    try:
        # Try creating the output folder in case it doesn't already exist
        os.mkdir(output_folder)
    except:
        pass

    # Read in all of the files we want to hide for use later
    if hide_files != None and hide_files != []:
        hide_dict = {}
        for file in hide_files:
            with open(file, 'rb') as f: hide_dict[file] = f.read()

    # For each file type we want to generate...
    for filetype in filetypes:
        # ...and for each size we want to generate...
        for size in sizes:
            # ...resize the base image to the correct size and convert it to our chosen file type
            current_image = resize(base_image, size, filetype)

            # If the file type is JPEG, we can do ZIP and EXIF steg as well
            if filetype.lower() == "jpeg":
                # If we have files we want to hide...
                if args.hide_files != []:
                    # ...run the jpeg_steg function from the jpeg steg module
                    current_image = jz.jpeg_steg(current_image, hide_dict)
                # Run the exif_spam function from the exif spam module
                current_image = es.exif_spam(current_image.getvalue())
            # Save out our newly stegged file
            with open(output_folder + '/' + str(size[0]) + 'x' + str(size[1]) + '.' + filetype, 'wb+') as f:
                f.write(current_image.getvalue())


