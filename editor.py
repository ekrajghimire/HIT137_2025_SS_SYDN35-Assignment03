import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


# Image Processor parent class
class ImageProcessor:
  def process(self, image):
    """ process method will be implmented by child classes for coressponding image processing logic"""
    raise NotImplementedError
  

# GrayscaleProcessor child class
class GrayscaleProcessor(ImageProcessor):
  def process(self,image):
    """ implment the process logic for image grayscaling """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# EdgeProcessor child class
class EdgeProcessor(ImageProcessor):
  def process(self, image):
    """ implment the process logic for edge processing"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Canny works on grayscale images
    return cv2.Canny(gray, 100, 200)
  


# BlurProcessor child class
class BlurProcessor(ImageProcessor):
    def __init__(self, k):
        # Kernel size must be odd for Gaussian blur
        self.k = k if k % 2 == 1 else k + 1

    def process(self, image):
        """ implements gaussian blur to an image"""
        return cv2.GaussianBlur(image, (self.k, self.k), 0)

# BrightnessProcessor child class
class BrightnessProcessor(ImageProcessor):
    def __init__(self, value):
        self.value = value

    def process(self, image):
        """ implements logic to adjust brightness value"""
        return cv2.convertScaleAbs(image, beta=self.value)

# Flipprocessor child class
class FlipProcessor(ImageProcessor):
    def __init__(self, mode):
        self.mode = mode

    def process(self, image):
        """ implement logic to flip the image """
        # flipCode: 1 = horizontal, 0 = vertical
        flipCode = 0 
        if flipCode == "horizontal":
          flipCode = 1
        return cv2.flip(image, flipCode)

# RotateProcessor child class
class RotateProcessor(ImageProcessor):
    def __init__(self, angle):
        self.angle = angle

    def process(self, image):
        """ implement logic for rotating the image"""
        # opencv providers rotation helpers, they are built-in
        if self.angle == 90:
            # rotate 90 degree clockwise
            return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        if self.angle == 180:
            # rotate 180 degree
            return cv2.rotate(image, cv2.ROTATE_180)
        if self.angle == 270:
            # rotate 90 degree counter clockwise
            return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return image



# Menu bar for window
class MenuBar:
    def __init__(self,root,app):
        # menubar object
        menubar = tk.Menu(root)
        
        # create a file menu
        file_menu = tk.Menu(menubar)
        # add Open command to file menu
        file_menu.add_command(label="Open", command=app.open_image)
        # add Save as command to file menu
        file_menu.add_command(label="Save As", command=app.save_image)
        # add a separator
        file_menu.add_separator()
        # add Exit command
        file_menu.add_command(label="Exit", command=root.quit) # It will exit the program
        
        
        # create an edit menu
        edit_menu = tk.Menu(menubar)
        # add Undo command
        edit_menu.add_command(label="Undo", command=app.undo)
        # add redo command
        edit_menu.add_command(label="Redo", command=app.redo)
        
        
        # Add file_menu and edit_menu to the menubar
        menubar.add_cascade(label="File",menu=file_menu)
        menubar.add_cascade(label="Edit",menu=edit_menu)
        
        # assign the menubar to root
        root.config(menu=menubar)

# ImageLoader class for opening and saving images
class ImageLoader:
    """ implements methods for opening and saving image"""
    def open_image(self):
        """ loads images using file dialog"""
        # only open a single image (only the image types mentioned on assignment are allowed)
        path = filedialog.askopenfilename(filetypes=[("Images","*.jpg,*.png,*.bmp")])
        
        if path:
            # read the image using opencv
            # return the read image and the path of the image
            return cv2.imread(path),path
        return None,None
    
    def save_image(self,image):
        """ save the current image """
        path = filedialog.asksaveasfilename(defaultextension=".jpg") # default extension is jpg
        if path:
            cv2.imwrite(path, image)
            return path
        return None
        
# ImageDisplay class to display image on the window
class ImageDisplay:
    """ display the image on application """
    def __init__(self, parent):
        self.container = tk.Frame(parent, bg="black", height=420,width=500)
        self.container.grid(row=0, column=0, sticky="nsew")
        # Prevent frame from resizing to image size
        self.container.grid_propagate(False)

        self.label = tk.Label(self.container, bg="black")
        self.label.pack(expand=True)

        self.last_image = None

    def resize_to_fit(self, image):
        """ method to the fit the image within the frame"""
        # Reference: https://stackoverflow.com/questions/50422735/tkinter-resize-frame-and-contents-with-main-window
        # Get available frame size
        fw = self.container.winfo_width()
        fh = self.container.winfo_height()

        # Avoid division errors during startup
        if fw < 10 or fh < 10:
            return image

        h, w = image.shape[:2]
        # Maintain aspect ratio
        scale = min(fw / w, fh / h)
        return cv2.resize(image, (int(w * scale), int(h * scale)))

    def show(self, image):
        """ show the image on the application """
        self.last_image = image
        image = self.resize_to_fit(image)

        # Convert image format for Tkinter display
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Display the image
        tk_img = ImageTk.PhotoImage(Image.fromarray(image))
        # Keep reference to avoid garbage collection
        self.label.image = tk_img
        self.label.config(image=tk_img)

    
# Main Application class
class ImageEditorApplication:
    """ Cordinates all components and logic of the program """
    def __init__(self,root):
        self.root = root
        # window details
        self.root.title("SYD35_Group_Image_Editor")
    
    def open_image(self):
        """ implement the file dialog opening for image loading"""
        pass
    
    def save_image(self):
        """ implement the logic to save image"""
        pass
    
    def undo(self):
        """ implement logic to undo the recent action """
        pass   
    
    def redo(self):
        """implement logic to redo the recent action"""
        pass
    
    
