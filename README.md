# Hidden in plain sight 🕵🏽

This repository is comprised of all the code I developed as part of my Final Year Project for BSc Cyber Security at the University of Warwick. The following information is adapted from a section from my full dissertation, which was submitted in June 2021.

## Tools Developed
As part of this project, a variety of tools were developed to help automate important tasks, such as generating a set of test images or comparing checksums of different images in bulk.

### EXIF Stress Tester (`exif_spam.py`)
One tool developed during this project is the EXIF Stress Tester. The tool takes an input JPEG image and adds a variety of pre-defined EXIF tags (36 in total, including timestamps of creation and modification, the image author, copyright information and camera specifications, among others). This tool was made as it was necessary to create images in bulk with different EXIF configurations. For example: if an image had a geotag containing a GPS co-ordinate that does not exist – in testing, the value `(4294967295, 4294967295, 4294967295)` was used – the website could respond in a variety of ways: ignoring the tag, removing it, or attempting to display it. It was also suggested that some tags may be left alone due to legal reasons, such as the copyright tag.

> The following EXIF tags were set to equal themselves (e.g. the `image_description` tag would be set to the value `image_description`):
> ```
> “processing_software”, “document_name”, “image_description”, “make”, “model”, “page_name”, “software”, “artist”, “host_computer”, “target_printer”, “copyright”, “sem_info”, “spectral_sensitivity”, “security_classification”, “image_unique_id”, “owner_name”, “serial_number”, “make_lens”, “model_lens”, “serial_number_lens”, “unique_camera_model”, “localized_camera_model”, “reel_name”, “camera_label”, “comment”, “device_manufacturer”, “device_model”

> The following EXIF tags were set to the following values:
> ```
> "gps_latitude": (4294967295, 4294967295, 4294967295)
> "gps_latitude_ref": "N"
> "gps_longitude": (4294967295, 4294967295, 4294967295)
> "gps_longitude_ref": "W”
> "gps_altitude": 4294967295
> "gps_altitude_ref": 1
> "modify_date": 01:02:03, March 1 2021
> "datetime_original": 01:02:03, March 1 2021
> "create_date": 01:02:03, March 1 2021


### JPEG-ZIP Creator (`zip_steg.py`)
Another tool that was developed was a program to create a combined JPEG-ZIP file – this is a JPEG image file that has a ZIP file concatenated on the end. The user provides a cover file and a list of files they want to hide. The program then ZIPs the files in memory and outputs the image and the ZIP archive combined in to one file. This program was created for use in the initial tests to see if websites would accept a hidden ZIP file inside the JPEG. It was also created to allow for code reuse in later parts of the experiments.

### Least Significant Bit (`lsb.py`)
Another tool used for this project was the lsb.py module. This takes an input PNG image, opens it using PIL (the Python Imaging Library, a module that allows for interaction with image files) and creates a representation of the image as a NumPy array (a Python module that is commonly used for mathematical operations). The program then takes a user-inputted message and converts it to binary. This binary representation of the message is then embedded in the least-significant bits of each of the red, green, and blue channels of each of the pixels in the image. The program also allows a user to reconstruct a message from an image. This tool was developed from scratch to allow for full flexibility over how this module could be embedded in in other tools (for example, bulk generating images for the tests); existing tools that are used on the command-line such as Steghide were found to be more difficult to use with Python compared to a native Python module such as this.

### Test Image Generator (`image_gen.py`)
The Image Generator was created specifically for the first part of this project, the Image Processing Experiment. This program allows a user to specify different file types and whether they wanted to embed a ZIP file in the test images. The program would then, from a base image, generate a variety of different image sizes and formats to see which methods of processing were performed by different websites. This tool was created as it allowed flexibility in customising the parameters of the tests on-the-fly and made the process of creating test images much faster than if they were to be created manually.

### Steganography Image Generator and Checker (`steg_doer.py` and `steg_checker.py`)
The final tools that were created for this project were for the second part of the investigation, the Steganography Experiment. These tools were called `steg_doer` and `steg_checker`. The former would perform a similar function to `image_gen.py` – it creates test images to different specifications. This program, however, embeds steganographic broadcasts using the different methods. It also uses a much smaller number of different formats and sizes, for reasons that will be discussed later in this paper. `steg_checker`, on the other hand, takes the resulting images after they have been uploaded and downloaded from the target websites and examines them to see if the messages that were embedded are still intact. It uses a third-party tool, `pattern.py`, to verify the full integrity of the message. Both tools were developed for the same reason as `image_gen.py`; the experiment necessitated the ability to generate batches of images quickly and have full control over the process.

## Third-Party Tools
### Gallery Downloader (`gallery-dl`)
gallery-dl is a Python module distributed via the Python Package Index (PyPI). It is a popular command line tool that allows a user to automatically scrape images from several websites, including Flickr, Instagram, Twitter, and Tumblr (mikf, 2021). This allowed the images used in the experiments to be downloaded quickly and easily from most of the websites tested on.

### Discrete Cosine Transform (`OutGuess`)
> 💡 OutGuess build available at [**resurrecting-open-source-projects/outguess**](https://github.com/resurrecting-open-source-projects/outguess)

OutGuess is a steganography tool originally created by Niels Provos of the University of Michigan in 1999. It uses the Discrete Cosine Transform method to embed a steganographic message in the quantisation table of a JPEG image. OutGuess has since been maintained by the open-source community on GitHub (Provos, et al., 2018).

### Pattern Creator (`pattern.py`, a Python version of Metasploit’s `pattern_create.rb`)
> > 💡 Original `pattern_create.rb` available at [**ickerwx/pattern**](https://github.com/ickerwx/pattern)

`pattern_create.rb` is a utility included with the Metasploit Framework; this is a series of tools that allow a user to exploit vulnerabilities on remote systems for security research. (Rapid7, 2021) The `pattern_create` tool specifically allows a user to create a non-repeating pattern of a specified length. In exploit development, this is commonly used for buffer overflows to see where an attacker can write to in memory (Offensive Security, n.d.). For this project, it was used to create a deterministic message of a specified length to allow for easy integrity checking after processing – simply passing the resulting string to the program is enough to check if it is fully intact. pattern.py is a Python version of this program created by a GitHub user `ickerwx` (ickerwx, 2019).

### AutoHotkey
AutoHotkey is a popular Windows scripting language used to automate desktop tasks (AutoHotkey, 2021). For this project, it was used to scrape images from websites that did not work correctly via `gallery-dl`, such as Facebook – the script would simply right-click each image on a page and save it to the desktop for later analysis.
