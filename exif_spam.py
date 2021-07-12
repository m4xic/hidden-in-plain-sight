from exif import Image
DATETIME_STR_FORMAT = "%Y:%m:%d %H:%M:%S"
import sys
from datetime import datetime
import io

def exif_spam(image):
    exif_img = Image(image)

    # Test various different 'default' EXIF tags
    exif_tags = ["processing_software", "document_name", "image_description", "make", "model", "page_name", "software", "artist", "host_computer", "target_printer", "copyright", "sem_info", "spectral_sensitivity", "security_classification", "image_unique_id", "owner_name", "serial_number", "make_lens", "model_lens", "serial_number_lens", "unique_camera_model", "localized_camera_model", "reel_name", "camera_label", "comment", "device_manufacturer", "device_model"]

    custom_tags = {
        # Test non-sensical GPS handling (could be used for LSB steg)
        "gps_latitude": (4294967295, 4294967295, 4294967295),
        "gps_latitude_ref": "N",
        "gps_longitude": (4294967295, 4294967295, 4294967295),
        "gps_longitude_ref": "W",
        "gps_altitude": 4294967295,
        "gps_altitude_ref": 1,
        # Test date handling for 3 different fields
        "modify_date": datetime(year=2021, month=3, day=1, hour=1, minute=2, second=3).strftime(DATETIME_STR_FORMAT),
        "datetime_original": datetime(year=2021, month=3, day=1, hour=1, minute=2, second=3).strftime(DATETIME_STR_FORMAT),
        "create_date": datetime(year=2021, month=3, day=1, hour=1, minute=2, second=3).strftime(DATETIME_STR_FORMAT)
    }

    # For all of the default tags, write the name of the tag to the field
    for default_tag in exif_tags:
        exif_img.set(default_tag, default_tag)

    # For all of the special tags, write the special value to the field
    for custom_tag in custom_tags.keys():
        exif_img.set(custom_tag, custom_tags[custom_tag])

    # Open a BytesIO object (so it can be passed back for use in other programs)
    final = io.BytesIO()
    # Write the new image to the BytesIO object
    final.write(exif_img.get_file())
    return final