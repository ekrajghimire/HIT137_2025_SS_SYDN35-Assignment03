import cv2
import tkinter as tk


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