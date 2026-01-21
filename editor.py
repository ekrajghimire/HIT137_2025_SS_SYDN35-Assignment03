import cv2
import tkinter as tk


# Image Processor parent class
class ImageProcessor:
  def process(self, image):
    """ process method will be implmented by child classes for coressponding image processing logic"""
    raise NotImplementedError