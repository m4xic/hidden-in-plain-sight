# SOURCES USED
# [1] Stack Overflow. 2021. Python int to binary string?. [online] Available at: <https://stackoverflow.com/questions/699866/python-int-to-binary-string> [Accessed 18 January 2021].
# [2] Stack Overflow, 2021. Extract LSB bit from a Byte in python. [online] Stack Overflow. Available at: <https://stackoverflow.com/questions/21341338/extract-lsb-bit-from-a-byte-in-python> [Accessed 18 January 2021].
# [3] GeeksforGeeks. 2021. Python | Convert String to Binary - GeeksforGeeks. [online] Available at: <https://www.geeksforgeeks.org/python-convert-string-to-binary/> [Accessed 18 January 2021].

from PIL import Image, UnidentifiedImageError
import numpy as np

def file_opener(filename):
    try:
        img = Image.open(filename)
        return [0, img]
    except (FileNotFoundError, UnidentifiedImageError) as e:
        return [1, e]

def write_array_to_image_clean(message, filename):
    """
    
    """
    img = Image.open(filename)
    image_array = np.array(img)
    #print(image_array)

    count = 0
    for h in range(img.height):
        for w in range(img.width):
            for rgb in range(3):
                if count < len(message):
                    # If we haven't finished encoding the whole message,
                    # get the current pixel we're looking at and convert
                    # the value to binary. Then, change the least signif
                    # bit to the one matching the message we're encoding
                    # and finally store that value back in the array
                    current_value = image_array[h][w][rgb]
                    current_value = (current_value & ~1) | int(message[count]) # [1]
                    image_array[h][w][rgb] = current_value
                else:
                    image_array[h][w][rgb] = 0
                count += 1
    return image_array

def write_array_to_image(message, filename):
    img = Image.open(filename)
    image_array = np.array(img)

    count = 0
    for h in range(img.height):
        for w in range(img.width):
            for rgb in range(3):
                if count < len(message):
                    # If we haven't finished encoding the whole message,
                    # get the current pixel we're looking at and convert
                    # the value to binary. Then, change the least signif
                    # bit to the one matching the message we're encoding
                    # and finally store that value back in the array
                    current_value = image_array[h][w][rgb]
                    current_value = (current_value & ~1) | int(message[count]) # [1]
                    image_array[h][w][rgb] = current_value
                else:
                    return image_array
                count += 1

def read_binary_from_image(filename):
    """
    This function uses a NumPy array from Pillow to read the LSB of each channel of each pixel.

    Parameters:
      - filename: the filename of the PIL.Image (subject to change, will use array)
      - checkstring: not yet developed, will be required to detect PIL.Image

    Returns:
      - final_message: the extracted message or None if no message found
    """

    img = Image.open(filename)
    image_array = np.array(img)

    message_binary = ""
    final_message = ""

    for h in range(img.height):
        for w in range(img.width):
            for rgb in range(3):
                current_value = image_array[h][w][rgb]
                current_value = (current_value & 1) # [2]
                message_binary += str(current_value)
    
                if len(message_binary) == 8:
                    final_message += chr(int(message_binary, 2))
                    if final_message.endswith("0001811954000"):
                        return final_message[:-13]
                    else:
                        message_binary = ""
                        continue
    return None

def message_to_binary(user_message, user_checkstring="0001811954000"):
    """
    This function converts a message to a binary string.

    Parameters:
      - message: the message you want to convert
      - checkstring: appended to the end to check for existence (optional)

    Returns:
      - array: the message as an array of bits
    """

    original_message = user_message + user_checkstring # construct the full message
    binary_message = [] # create an empty list for the bits to be stored in

    for ascii_letter in original_message: # convert the message one letter at a time
        binary_rep = format(ord(ascii_letter), 'b') # [3] - converting ascii to binary
        while len(binary_rep) < 8: # if the binary form has less than 8 bits, add 0s for padding
            binary_rep = "0" + binary_rep # without this, the conversion on the other end would fail!
        for bit in binary_rep: binary_message.append(bit) # append each bit to the list in order

    return binary_message # return the list of bits
        

def image_to_array(filename):
    """
    This function converts an PIL.Image to a NumPy array.

    Parameters:
      - filename: the filename of the file you want to open
    
    Returns:
      - array: an array of the pixels of the file - [h][w][rgb]
    """
    img = Image.open(filename)
    array = np.asarray(img)
    return array