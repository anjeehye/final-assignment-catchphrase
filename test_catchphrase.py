"""
Documentation
"""

import os
import imageio
import pytest

#import catchphrase_gui
import catchphrase_module


# %% Different Image Types
"""
Checks whether the individual modules work well

Check if the last item of the list is identical to the original image

Image comparison
https://matplotlib.org/3.1.1/api/testing_api.html#matplotlib.testing.decorators.image_comparison
"""

test_image_folder = 'test_images'

def test_catchphrase_image_color() :
    # Test color image
    test_filename = 'test_image_color.jpeg'
    test_img = os.path.join(test_image_folder, test_filename)
    result = catchphrase_module.catchphrase_main(test_img)
    # The last item of the list  identical to the original image
    test_path = os.path.join('images', test_img)
    img = imageio.imread(test_path)
    assert (result[4] == img).all() == True

def test_catchphrase_image_bw() :
    # Test greyscale image
    test_filename = 'test_image_greyscale.jpeg'
    test_img = os.path.join(test_image_folder, test_filename)
    result = catchphrase_module.catchphrase_main(test_img)
    test_path = os.path.join('images', test_img)
    img = imageio.imread(test_path)
    assert (result[4] == img).all() == True


# %% Testing invalid arguments

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