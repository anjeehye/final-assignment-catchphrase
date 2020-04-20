"""
This module contains the functions for playing Catchphrase.

The functions import an image located in the 'images' folder. The image is
then divided into 9 (3*3) sections. One section will be revealed at a time.
The user can decide the number of sections to be revealed (deafult 3).

This file is exported to 'catchphrase_gui.py' as a module and contains the
following functions:

    Helper Functions:
    * image_importer(filename) - returns NumPy array of an image
    * image_mask(img) - returns a black mask
    * image_sections(img) - returns coordinates of each of the 9 sections
    * unmask(img, reveal_number) - returns a list of partially masked images
    Main Function:
    * catchphrase_main(filename, reveal_number)
"""

import os
import imageio
from matplotlib import pyplot
import math
import random
import numpy


# %% Helper Functions

def image_importer(filename):
    """Imports an image from the 'images' folder.

    Argument:
        filename: a string representing the name of the image file.

    Returns:
        A NumPy array.
    """
    filepath = os.path.join('images', filename)
    img = imageio.imread(filepath)

    return img


def image_mask(img):
    """ Creates a black mask the size of the image.

    Argument:
        img: a NumPy array.

    Returns:
        A NumPy array of black pixels with the same size as the img.

    Raises:
        TypeError: If the img is not a 2D or 3D NumPy array.
    """
    mask = numpy.array(img)

    if len(mask.shape) < 3:  # greyscale image (no channels)
        mask[:, :] = 0
    elif len(mask.shape) == 3:  # color image
        mask[:, :, 0:3] = 0
    else:
        raise TypeError('Unsupported image type.')

    return mask


def image_sections(img):
    """Divides the image into 9 sections.

    Argument:
        img: a NumPy array.

    Returns:
        A dictionary containing the x, y coordinates of each of the 9 sections.
        The keys of the dictionary are 'x1', 'x2', 'y1', and 'y2'.
    """
    img_height = img.shape[0]
    img_width = img.shape[1]

    # get coordinates for dividing up the image (3 x 3)
    x_one_third = math.trunc(img_width/3)
    x_two_thirds = math.trunc(img_width/3*2)
    y_one_third = math.trunc(img_height/3)
    y_two_thirds = math.trunc(img_height/3*2)

    x_coordinates = [0, x_one_third, x_two_thirds, img_width-1]
    y_coordinates = [0, y_one_third, y_two_thirds, img_height-1]

    section_coordinates = []

    for i in range(1, 4):
        for ii in range(1, 4):
            coordinates = {
                    'x1': x_coordinates[i-1],
                    'x2': x_coordinates[i],
                    'y1': y_coordinates[ii-1],
                    'y2': y_coordinates[ii]}
            section_coordinates.append(coordinates)

    return section_coordinates


def unmask(img, reveal_number):
    """Randomly select and unmask n number of sections.

    Example:
        >>> unmask(img, 3)

    Arguments:
        img: a NumPy array.
        reveal_number: an integer, the number of sections to be unmasked.
        (deafult is 3)

    Returns:
        A list containing:
            - a black mask
            - partially unmasked images
            - original image
    """
    mask = image_mask(img)
    section_coordinates = image_sections(img)

    # Select (reveal_number) random sections
    index = random.sample(range(1, 9), reveal_number)
    new_mask = numpy.array(mask)
    unmask_sections = [mask]  # First item in the list is a black mask

    for i in range(0, reveal_number):
        # Coordinates of the section to be revealed
        section_reveal = section_coordinates[index[i]]

        new_mask = numpy.array(new_mask)

        # Section of the image to be revealed
        img_reveal = img[section_reveal['y1']:section_reveal['y2'],
                         section_reveal['x1']:section_reveal['x2']]

        # replace the section of the new_mask with the image
        new_mask[section_reveal['y1']:section_reveal['y2'],
                 section_reveal['x1']:section_reveal['x2']] = img_reveal

        unmask_sections.append(new_mask)

    # Last item in the list is the original image
    unmask_sections.append(img)

    return unmask_sections


# %% Main Function

def catchphrase_main(filename, reveal_number=3):
    """Imports an image and processes it for the catchphrase game.

    Example:
        >>> catchphrase_images('image.jpg', 5)

    Arguments:
        filename: a string representing the name of the image file.
        reveal_number: an integer, the number of sections to be unmasked
        (default is 3)

    Returns:
        A list containing:
            - a black mask
            - partially unmasked images
            - original image

    Raises:
        TypeError: if a non-integer input is given for the second argument.
        ValueError: if a value below 1 or above 8 is given for the second
        argument.
    """

    if isinstance(reveal_number, int) is False:
        raise TypeError('Your second argument must be a whole number.')
    elif reveal_number < 1:
        raise ValueError('You should reveal at least one section.')
    elif reveal_number > 8:
        raise ValueError('You cannot reveal more than 8 sections!')

    img = image_importer(filename)
    unmask_images = unmask(img, reveal_number)

    return unmask_images


# %% Testing

if __name__ == '__main__':
    # Test the catchphrase_main function using pyplot.

    catchphrase_images = catchphrase_main('at.jpg')
    reveal_length = len(catchphrase_images)

    if len(catchphrase_images[0].shape) == 2:
        color = "gray"
    else:
        color = "viridis"

    input("Press enter to start.")
    pyplot.imshow(catchphrase_images[0], cmap=color)
    pyplot.pause(.1)

    for i in range(1, reveal_length-1):
        input("press enter to reveal a section")
        pyplot.imshow(catchphrase_images[i], cmap=color)
        pyplot.pause(.1)
    input('press enter for the final reveal.')
    pyplot.imshow(catchphrase_images[reveal_length-1], cmap=color)
