"""
Summarize into one ultimate function
    - return a list containing:
        mask, one revealed, ... x revealed, original image
"""

import os
import imageio
from matplotlib import pyplot
import math
import random
import numpy
#import skimage.transform as st
#from skimage import img_as_ubyte


# %% Image Import

def image_importer(filename):
    """Imports image

    Argument:
        - string: name of the image file

    Returns:
        - image numpy array
        (rescaled if its width or height is greater than 500 px)
    """
    filepath = os.path.join('images', filename)

    img = imageio.imread(filepath)
#    img = image_rescale(img)

    return img


#def image_rescale(img):
#    """
#    if the width or height of the image is greater than 500 px,
#    scale down so that the max length is 500
#    """
#    width = img.shape[1]
#    height = img.shape[0]
#    
#    if len(img.shape) == 2:
#        color = False
#    else:
#        color = True
#    
#    print(color)
#
#    if (width > 500) or (height > 500):
#        if width > height:
#            factor = 500/width
#        else:
#            factor = 500/height
#        img = st.rescale(img, factor, multichannel = color)
#        img = img_as_ubyte(img)
#
#    return img

# %% Image Processing


def image_mask(img):
    # Create a black mask the size of the image
    mask = numpy.array(img)

    if len(mask.shape) < 3:
        # a greyscale image (no channels)
        mask[:, :] = 0
    elif len(mask.shape) == 3:
        mask[:, :, 0:3] = 0
    else:
        raise TypeError('Unsupported image type.')

    return mask


def image_divider(img):
    """Divide the image into 9 sections

    Example:
        >>> image_divider(img)

    Argument:
        - img numpy array

    Returns:
        A dictionary containing the x, y coordinates of each of the 9 sections.
    """
    img_height = img.shape[0]
    img_width = img.shape[1]

    # get coordinates for dividing up the image (3 x 3)
    x_one_third = math.trunc(img_width/3)
    x_two_thirds = math.trunc(img_width/3*2)
    y_one_third = math.trunc(img_height/3)
    y_two_thirds = math.trunc(img_height/3*2)

    x_coor = [0, x_one_third, x_two_thirds, img_width-1]
    y_coor = [0, y_one_third, y_two_thirds, img_height-1]

    section_coordinates = []

    for i in range(1, 4):
        for ii in range(1, 4):
            coordinates = {
                    'x1': x_coor[i-1],
                    'x2': x_coor[i],
                    'y1': y_coor[ii-1],
                    'y2': y_coor[ii]}
            section_coordinates.append(coordinates)
    return section_coordinates


def unmask(img, reveal_number):
    """Randomly select and unmask (reveal_number) number of sections.

    Example:
        >>> unmask(img, 3)

    Arguments:
        - image numpy array
        - number of sections to be unmasked

    Returns:
        A list containing:
            - a black mask
            - partially unmasked images
            - original image
    """
    mask = image_mask(img)
    section_coordinates = image_divider(img)

    # get (reveal_number) number of random numbers
    index = random.sample(range(1, 9), reveal_number)
    new_mask = numpy.array(mask)
    unmask_sections = [mask]

    for i in range(0, reveal_number):
        section_reveal = section_coordinates[index[i]]
        new_mask = numpy.array(new_mask)

        img_reveal = img[section_reveal['y1']:section_reveal['y2'],
                         section_reveal['x1']:section_reveal['x2']]

        new_mask[section_reveal['y1']:section_reveal['y2'],
                 section_reveal['x1']:section_reveal['x2']] = img_reveal

        unmask_sections.append(new_mask)

    unmask_sections.append(img)
    return unmask_sections


# %% The Ultimate Function

def catchphrase_images(filename, reveal_number=3):
    """Process the image and return a list of numpy arrays
    to be used for the catchphrase game.

    Example:
        >>> catchphrase_images('example.jpg', 3)

    Arguments:
        - image filename
        - number of sections to be unmasked

    Returns:
        A list containing:
            - a black mask
            - partially unmasked images
            - original image
    """
    img = image_importer(filename)
    unmask_images = unmask(img, reveal_number)

    return unmask_images


if __name__ == '__main__':
    unmask_images = catchphrase_images('cd.jpg')
    reveal_length = len(unmask_images)

    if len(unmask_images[0].shape) == 2:
        color="gray"
    else:
        color="viridis"

    input("Press enter to start.")
    pyplot.imshow(unmask_images[0], cmap=color)
    pyplot.pause(.1)

    for i in range(1, reveal_length-1):
        input("press enter to reveal a section")
        pyplot.imshow(unmask_images[i], cmap=color)
        pyplot.pause(.1)
    input('press enter for the final reveal.')
    pyplot.imshow(unmask_images[reveal_length-1], cmap=color)