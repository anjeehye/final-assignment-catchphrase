"""

"""

import tkinter as tk
from PIL import Image, ImageTk
import skimage.transform as st
from skimage import img_as_ubyte

from catchphrase_module import catchphrase_images


# %%


class catchphrase_gui(tk.Tk):
    def __init__(self, filename, reveal_number):
        tk.Tk.__init__(self)

        # GUI settings: title, font, color scheme, image size
        tk.Tk.wm_title(self, "Catchphrase!")
        self.option_add("*Font", "courier")
        self.colors = {
                'background': '#1a1a1a', #'#a140d4'
                'highlight': '#48e9d0', #'#eaac86'
                }
        img_max_dimension = 600  # max width/height (in pixels)

        self.images = catchphrase_images(filename, reveal_number)

        # Rescale the image
        self.images = self.image_rescale(self.images, img_max_dimension)

        container = tk.Frame(self, padx=10, pady=10,
                             bg=self.colors['highlight'])
        container.pack(expand=True)

        self.frames = {}

        for f in (StartPage, GamePage, FinalReveal):
            frame = f(container, self, self.images, reveal_number)
            self.frames[f] = frame
            frame.config(bg=self.colors['background'], padx=20, pady=20)
            frame.grid(row=0, column=0, sticky="nsew")
            # Center the frame
            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(2, weight=1)
            frame.rowconfigure(0, weight=1)
            frame.rowconfigure(2, weight=1)

        self.show_frame(StartPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def image_rescale(self, images, max_dimension):
        # if the image is too big, rescale it so that either its width/height is
        # not bigger than max_dimension
        width = images[0].shape[1]
        height = images[0].shape[0]

        if (width > max_dimension) or (height > max_dimension):
            if width > height:
                factor = max_dimension/width
            else:
                factor = max_dimension/height

            if len(images[1].shape) == 2:
                color = False
            else:
                color = True

            for i in range(0, len(images)):
                images[i] = st.rescale(images[i], factor, multichannel = color)
                images[i] = img_as_ubyte(images[i])
        return images

class StartPage(tk.Frame):
    def __init__(self, parent, controller, images, reveal_number):
        tk.Frame.__init__(self, parent)

        startpage_frame = tk.Frame(self, bg=controller.colors['background'])
        startpage_frame.grid(row=1, column=1)

        instructions = "There's an image behind the mask. \
A piece will be revealed at a time - {} pieces will be revealed in total. \
Try to guess what the image is!".format(reveal_number)

        label_title = tk.Label(startpage_frame, text="CATCHPHRASE",
                               font="Courier 40 bold", padx=10, pady=10,
                               fg=controller.colors['highlight'],
                               bg=controller.colors['background'])
        label_title.grid(column=0, row=0)

        label_instructions = tk.Label(startpage_frame, text=instructions,
                                      wraplength=400, padx=30, pady=30,
                                      bg=controller.colors['highlight'],
                                      fg=controller.colors['background'])
        label_instructions.grid(column=0, row=3, padx=10, pady=10)

        button_start = tk.Button(startpage_frame, text="Start game!!", padx=10,
                                 command=lambda: controller.show_frame(GamePage))
        button_start.grid(column=0, row=4, padx=10, pady=10)


class GamePage(tk.Frame):
    def __init__(self, parent, controller, images, reveal_number):
        tk.Frame.__init__(self, parent)

        self.reveal = []
        self.counter = 1

        gamepage_frame = tk.Frame(self, bg=controller.colors['background'])
        gamepage_frame.grid(row=1, column=1)

        for i in range(0, reveal_number+2):
            reveal_section = ImageTk.PhotoImage(image=Image.fromarray(images[i]))
            self.reveal.append(reveal_section)

        self.old_mask_label = tk.Label(gamepage_frame, image=self.reveal[0])
        self.old_mask_label.grid(column=0, row=0, padx=10, pady=10)

        button_reveal = tk.Button(gamepage_frame, text="Reveal a piece.",
                                  command=lambda: self.reveal_piece(gamepage_frame, self.reveal, self.counter, button_reveal, reveal_number))
        button_reveal.grid(column=0, row=1, pady=5)

        button_end = tk.Button(gamepage_frame, text="Show me the answer.",
                               command=lambda: controller.show_frame(FinalReveal))
        button_end.grid(column=0, row=2, pady=5)


    def reveal_piece(self, gamepage_frame, reveal_sections, counter, button, reveal_number):   
        if self.reveal_button_display(button, reveal_number) is False:
            return

        self.old_mask_label.grid_forget()

        reveal_label = tk.Label(gamepage_frame, image=reveal_sections[counter])
        reveal_label.grid(column=0, row=0, padx=10, pady=10)
        self.old_mask_label = reveal_label
        self.counter = self.counter + 1

        self.reveal_button_display(button, reveal_number)

    def reveal_button_display(self, button, reveal_number):
        if self.counter <= (reveal_number):
            pass
        else:
            button.grid_forget()
            return False


class FinalReveal(tk.Frame):
    def __init__(self, parent, controller, images, reveal_number):
        tk.Frame.__init__(self, parent)

        reveal_frame = tk.Frame(self, bg=controller.colors['background'])
        reveal_frame.grid(row=1, column=1)

        self.original_image = ImageTk.PhotoImage(image=Image.fromarray(images[reveal_number+1]))
        img_label = tk.Label(reveal_frame, image=self.original_image)
        img_label.grid(column=0, row=1, padx=10, pady=10)


def play_catchphrase(filename, reveal_number=3):
    """Play catchphrase.

    The image is divided into 9 rectangular pieces, and each piece is revealed 
    in turn until one of the contestants is able to identify the image.

    Example:
        >>> play_catchphrase('my_image.jpg', 4)

    Argument:
        filename: the name of the image file inside the 'images' folder
        integer: the number of pieces to be revealed (default 3)

    Raises
        TypeError: if a non-integer input is given for the second argument.
        ValueError: if a value below 1 or above 8 is given for the second argument.
    """
    if isinstance(reveal_number, int) is False:
        raise TypeError('Your second argument must be a whole number.')
    elif reveal_number < 1:
        raise ValueError('You should reveal at least one section.')
    elif reveal_number > 8:
        raise ValueError('You cannot reveal more than 8 sections!')

    window = catchphrase_gui(filename, reveal_number)
    window.mainloop()


if __name__ == '__main__':
    play_catchphrase('cd.jpg', 4)
