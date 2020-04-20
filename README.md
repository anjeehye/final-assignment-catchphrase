# Catchphrase

Play the Catchphrase game on a GUI.

An image is hidden behind a black mask. The image is divided into 9 rectangular pieces, and each piece is revealed in turn until one of the contestants is able to identify the image.

## Getting Started

### Contents
- /images
- catchphrase_module.py
- catchphrase_gui.py
- test_catchphrase.py
- requirements.txt

Required packages are listed under ```requirements.txt```.

## Instructions
Place your image file in the ```/images``` folder.
Open ```catchphrase_gui.py```, play the Catchphrase game using the following command:
```
play_catchphrase_gui(filename, reveal_number)
```
If ```reveal_number``` is left empty, 3 pieces will be revealed by default.