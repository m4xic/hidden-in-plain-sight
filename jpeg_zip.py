import sys
import io
from zipfile import ZipFile
from PIL import Image

def jpeg_steg(jpeg, hide_files):
    try:
        # Create a BytesIO object and store the image content in it
        jpeg_bytes = io.BytesIO()
        im = Image.open(jpeg)
        im.save(jpeg_bytes, 'jpeg')

        # Create a BytesIO object and store the ZIP file in it
        zip_bytes = io.BytesIO()
        zip_file = ZipFile(zip_bytes, 'w')
        # For each provided file that should be added...
        for file_set in hide_files.keys():
            # Add each file to the ZIP file
            zip_file.writestr(file_set, hide_files[file_set])
        zip_file.close()

        # Combine the two BytesIO objects to one continuous stream
        combined_file = io.BytesIO()
        combined_file.write(jpeg_bytes.getvalue())
        combined_file.write(zip_bytes.getvalue())
        # Return the completed file
        return combined_file
    except Exception as e:
        print("[!] Hit an exception. Stopping...")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("[!] Non-interactive usage: jpeg-zip.py <jpeg file> <file to hide>")
        sys.exit(1)
    else:
        jpeg = sys.argv[1]
        hide = sys.argv[2]
    with open(hide, 'rb') as hide_bytes:
        out_bytes = jpeg_steg(jpeg, {hide: hide_bytes.read()})
    with open('hidden-' + jpeg, 'wb') as steg_jpeg:
        steg_jpeg.write(out_bytes.getvalue())
