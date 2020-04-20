"""
Testing the script using pytest.
"""

import os
import imageio
import pytest

#import catchphrase_gui
import catchphrase_module


# %% Different Image Types
"""
Imports images from the 'images/test_images' folder, which contains a
rgb and a greyscale images. Then checks whether the images were imported
successfully by comparing the original image to the last item of the list 
returned by the catchphrase_main() function.
"""

test_image_folder = 'test_images'

def test_catchphrase_image_color() :
    # Test color image
    test_filename = 'test_image_color.jpeg'
    test_img = os.path.join(test_image_folder, test_filename)
    test_path = os.path.join('images', test_img)
    result = catchphrase_module.catchphrase_main(test_img)
    original_img = imageio.imread(test_path)
    assert (result[4] == original_img).all() == True

def test_catchphrase_image_bw() :
    # Test greyscale image
    test_filename = 'test_image_greyscale.jpeg'
    test_img = os.path.join(test_image_folder, test_filename)
    test_path = os.path.join('images', test_img)
    result = catchphrase_module.catchphrase_main(test_img)
    # read original image
    original_img = imageio.imread(test_path)
    assert (result[4] == original_img).all() == True


# %% Testing Errors

filename = 'at.jpg'

def test_catchphrase_gui_invalid_reveal_number() :
    with pytest.raises(TypeError) :
        catchphrase_module.catchphrase_main(filename, 'three')

def test_catchphrase_gui_invalid_too_small_reveal_number() :
    with pytest.raises(ValueError) :
        catchphrase_module.catchphrase_main(filename, -5)

def test_catchphrase_gui_invalid_zero_reveal_number() :
    with pytest.raises(ValueError) :
        catchphrase_module.catchphrase_main(filename, 0)

def test_catchphrase_gui_invalid_too_bit_reveal_number() :
    with pytest.raises(ValueError) :
        catchphrase_module.catchphrase_main(filename, 10)

# %% Style check
#! pycodestyle catchphrase_module.py
#! pycodestyle catchphrase_gui.py
#
## Covergae
#! pytest --cov
#! pytest --cov-report term-missing --cov
#! coverage report -m