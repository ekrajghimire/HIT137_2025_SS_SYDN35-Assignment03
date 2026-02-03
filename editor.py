"""
Assignment: 3
Course: HIT137_Software-Now
Group Name: SYDNEY-35 (SYD-35)
Authors: Roshan Lamichhane (S399178), Ekraj Ghimire - (S398831), Sudip Sunar (S398629), Shrijan Neupane  (S398335)

Group Members:
Roshan Lamichhane - S399178
Ekraj Ghimire - S398831
Sudip Sunar - S398629
Shrijan Neupane - S398335


References:
-

"""

import cv2
import tkinter as tk
from tkinter import filedialog, messagebox  # message boxes for errors / confirmations
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
        if self.mode == "horizontal":
          flipCode = 1
        elif self.mode == "vertical":
          flipCode = 0
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


# ResizeProcessor child class
class ResizeProcessor(ImageProcessor):
    def __init__(self, scale):
        # scale is a float like 0.75, 1.0, 1.25
        self.scale = scale

    def process(self, image):
        """ implement the resizing logic """
        # TODO: insert reference here
        h, w = image.shape[:2]
        new_w = int(w * self.scale)
        new_h = int(h * self.scale)
        # avoid zero dimension errors
        new_w = max(1, new_w)
        new_h = max(1, new_h)
        return cv2.resize(image, (new_w, new_h))


# ContrastProcessor child class
class ContrastProcessor(ImageProcessor):
    def __init__(self, value):
        # value controls contrast in a small range (e.g. 0.5 - 1.5)
        self.value = value

    def process(self, image):
        """ implements logic to adjust contrast value"""
        return cv2.convertScaleAbs(image, alpha=self.value, beta=0)


# Menu bar for window
class MenuBar:
    def __init__(self,root,app):
        # menubar object
        menubar = tk.Menu(root)
        
        # create a file menu
        file_menu = tk.Menu(menubar)
        # add Open command to file menu
        file_menu.add_command(label="Open", command=app.open_image)
        # add Save command
        file_menu.add_command(label="Save", command=app.save_image)
        # add Save as command to file menu
        file_menu.add_command(label="Save As", command=app.save_image_as)
        # add a separator
        file_menu.add_separator()
        # add Exit command
        file_menu.add_command(label="Exit", command=app.exit_app) # It will exit the program with confirmation
        
        
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
        path = filedialog.askopenfilename(filetypes=[("Images","*.jpg *.png *.bmp *.jpeg")])
        
        if path:
            # read the image using opencv
            # return the read image and the path of the image
            return cv2.imread(path),path
        return None,None
    
    def save_image(self,image, default_path=None):
        """ save the current image using Save (or Save As when path is None) """
        if default_path:
            cv2.imwrite(default_path, image)
            return default_path
        # Save As dialog
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


# ImageState class to allow for redo and undo action on image
class ImageState:
    def __init__(self):
        self.original = None  # store the original image
        self.current = None
        self.undo_stack = []
        self.redo_stack = []

    def set_original(self, image):
        """ set or replace the original image """
        self.original = image
        self.current = image
        self.undo_stack.clear()
        self.redo_stack.clear()

    def set(self, image):
        """ track the action"""
        # Save previous state for undo
        if self.current is not None:
            self.undo_stack.append(self.current)
        self.current = image
        # Redo history is cleared after new action
        self.redo_stack.clear()

    def undo(self):
        """ allows undo action """
        if self.undo_stack:
            self.redo_stack.append(self.current)
            self.current = self.undo_stack.pop()

    def redo(self):
        """ redo the action """
        if self.redo_stack:
            self.undo_stack.append(self.current)
            self.current = self.redo_stack.pop()

    
# StatusBar class to display info on status bar
class StatusBar(tk.Label):
    """ display information on status bar"""
    
    def __init__(self, parent):
        super().__init__(parent, bd=1,relief=tk.SUNKEN, anchor="w")
        self.pack(fill=tk.X)
        self.config(text="No image loaded") # default text
    def update(self, name, image):
        # update the status bar with necessary information such as image name and resolution
        if image is None:
            self.config(text="No image loaded")
            return
        h, w = image.shape[:2]
        self.config(text=f"{name} | {w} x {h}")
    

# ControlPanel class contains buttons for image manipulation
class ControlPanel:
    def __init__(self, parent, app):
        self.frame = tk.Frame(parent, padx=10, pady=10)
        self.frame.grid(row=0, column=1, sticky="ns")

        tk.Label(self.frame, text="Image Tools",
                 font=("Arial", 11, "bold")).pack(pady=5)

        # Each button creates a processor object
        # and passes it to the main application
        
        # Grayscale conversion
        tk.Button(self.frame, text="Grayscale",
                  command=lambda: app.apply_processor(
                      GrayscaleProcessor(), "Grayscale applied")
                  ).pack(fill="x", pady=2)

        # Edge detection
        tk.Button(self.frame, text="Edge Detection",
                  command=lambda: app.apply_processor(
                      EdgeProcessor(), "Edge detection applied")
                  ).pack(fill="x", pady=2)

        # Rotate 90 degree
        tk.Button(self.frame, text="Rotate 90°",
                  command=lambda: app.apply_processor(
                      RotateProcessor(90), "Image rotated 90°")
                  ).pack(fill="x", pady=2)
        
         # Rotate 180 degree
        tk.Button(self.frame, text="Rotate 180°",
                  command=lambda: app.apply_processor(
                      RotateProcessor(180), "Image rotated 180°")
                  ).pack(fill="x", pady=2)

        # Rotate 270 degree
        tk.Button(self.frame, text="Rotate 270°",
                  command=lambda: app.apply_processor(
                      RotateProcessor(270), "Image rotated 270°")
                  ).pack(fill="x", pady=2)
        
        # Flip horizontal
        tk.Button(self.frame, text="Flip Horizontal",
                  command=lambda: app.apply_processor(
                      FlipProcessor("horizontal"),
                      "Image flipped horizontally")
                  ).pack(fill="x", pady=2)
        
          # Flip vertical
        tk.Button(self.frame, text="Flip Vertical",
                  command=lambda: app.apply_processor(
                      FlipProcessor("vertical"),
                      "Image flipped vertically")
                  ).pack(fill="x", pady=2)


        # Blur slider (small range)
        tk.Label(self.frame, text="Blur").pack(anchor="w", pady=(10, 0))
        self.blur_slider = tk.Scale(self.frame, from_=1, to=50, orient=tk.HORIZONTAL)
        self.blur_slider.pack(fill="x")
        self.blur_slider.config(
            command=lambda v: app.apply_processor(
                     BlurProcessor(int(v)),
                     f"Blur applied (k={int(v)})")
        )

        # Brightness slider (small range)
        tk.Label(self.frame, text="Brightness").pack(anchor="w", pady=(10, 0))
        self.brightness_slider = tk.Scale(
            self.frame, from_=-30, to=50, orient=tk.HORIZONTAL
        )
        self.brightness_slider.pack(fill="x")
        self.brightness_slider.config(
            command=lambda v: app.apply_processor(
                BrightnessProcessor(int(v)),
                f"Brightness adjusted ({int(v)})")
        )

        # Contrast slider (small realistic range ~0.5–1.5)
        tk.Label(self.frame, text="Contrast").pack(anchor="w", pady=(10, 0))
        self.contrast_slider = tk.Scale(
            self.frame, from_=-5, to=10, orient=tk.HORIZONTAL
        )
        self.contrast_slider.pack(fill="x")
        self.contrast_slider.config(
            command=lambda v: app.apply_processor(
                ContrastProcessor(1.0 + (int(v) / 10.0)),
                f"Contrast adjusted ({1.0 + (int(v) / 10.0)})")
        )

        # Resize slider (75%–125%)
        tk.Label(self.frame, text="Resize (%)").pack(anchor="w", pady=(10, 0))
        self.resize_slider = tk.Scale(
            self.frame,
            from_=75, to=200,
            orient=tk.HORIZONTAL
        )
        self.resize_slider.pack(fill="x")
        self.resize_slider.set(100)  # default = original size
        self.resize_slider.config(
            command=lambda v: app.apply_processor(
                ResizeProcessor(int(v)/100),
                f"Image resized to {v}%")
        )

        # information label to explain how actions work
        tk.Label(
            self.frame,
            text="Note: All actions are performed on original image.\nResult may vary due to this.",
            bg="#ccffcc"
        ).pack(pady=(40, 10))

         # student information
        tk.Label(
            self.frame,
            text="Student Details:\n"\
            "Group - SYDNEY-35(SYD-35)\n" \
            "Roshan Lamichhane - S399178\n" \
            "Ekraj Ghimire - S398831\n"\
            "Sudip Sunar - S398629\n"\
            "Shrijan Neupane - S398335",
            bg="#7fe67f",
            
        ).pack(pady=(40,0))

    def reset_controls(self):
        """ resets the values for blur, brightness and contrast slider """
        self.blur_slider.set(1)
        self.brightness_slider.set(0)
        self.contrast_slider.set(0)   # 0 => factor 1.0
        self.resize_slider.set(100)

# Main Application class
class ImageEditorApplication:
    """ Cordinates all components and logic of the program """
    def __init__(self,root):
        self.root = root
        # window details
        self.root.title("SYD35_Group_Image_Editor")
        self.root.geometry("950x650")

        # Create object of each window components
        self.state = ImageState()
        self.loader = ImageLoader()
        self.filename = ""
        # used during saving
        self.filepath = None

        main = tk.Frame(root)
        main.pack(fill=tk.BOTH, expand=True)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(0, weight=1)

        self.display = ImageDisplay(main)
        self.controls = ControlPanel(main, self)

        self.status = StatusBar(root)
        self.menu = MenuBar(root, self)
        
    def refresh(self):
        """ update the window"""
        if self.state.current is not None:
            self.display.show(self.state.current)
        self.status.update(self.filename, self.state.current)

    def open_image(self):
        """ implement the file dialog opening for image loading"""
        image, path = self.loader.open_image()
        if image is not None:
            self.state.set_original(image)
            self.filename = path.split("/")[-1]
            self.controls.reset_controls() # reset the sliders
            self.refresh()
    
    def apply_processor(self, processor, message):
        """ apply the corresponding processor for each image action"""
        if self.state.original is None:
            messagebox.showerror("Error", "No image loaded")
            return

        # always apply processor to the original image
        processed = processor.process(self.state.original)
        self.state.set(processed)
        self.refresh()


    def save_image(self):
        """ saves the image by opening file dialog or overwriting current file"""
        if self.state.current is None:
            messagebox.showerror("Error", "No image to save")
            return
        
        # if we already have a path, confirm overwrite
        if self.filepath:
            answer = messagebox.askyesno("Confirm Save", f"Overwrite existing file?\n{self.filepath}")
            if not answer:
                # user cancelled overwrite, so do Save As instead
                self.save_image_as()
                return
            path = self.loader.save_image(self.state.current, self.filepath)
        else:
            path = self.loader.save_image(self.state.current)
            self.filepath = path
            if path:
                self.filename = path.split("/")[-1]

    def save_image_as(self):
        """ saves image using Save As dialog """
        if self.state.current is None:
            messagebox.showerror("Error", "No image to save")
            return
        
        path = self.loader.save_image(self.state.current)
        if path:
            self.filepath = path
            self.filename = path.split("/")[-1]
            self.refresh()
    
    def undo(self):
        """ implement logic to undo the recent action """
        if self.state.current is None:
            messagebox.showerror("Error", "Nothing to undo")
            return

        self.state.undo()
        self.refresh()
    
    def redo(self):
        """implement logic to redo the recent action"""
        if self.state.current is None:
            messagebox.showerror("Error", "Nothing to redo")
            return

        self.state.redo()
        self.refresh()

    def exit_app(self):
        """ exit the application with confirmation """
        if messagebox.askokcancel("Exit", "Do you really want to exit?"):
            self.root.quit()
    
    
# Application entry point
if __name__== "__main__":
    root = tk.Tk()
    ImageEditorApplication(root)
    root.mainloop()