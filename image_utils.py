# This file contains the image loading and displaying function
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk


# Load an image based on the filename provided by the user
def load_image(file_name):
    # Load and return the image as a Numpy array
    img = Image.open(file_name)
    return np.array(img)

# Display the image in a Tkinter window
def display_image(img_array, title = "Image"):
    img = Image.fromarray(img_array)
    img_tk = ImageTk.PhotoImage(img)

    # Create a new window to display the image
    window = tk.Toplevel()
    window.title(title)
    label = tk.Label(window, image=img_tk)
    label.image = img_tk  # Keep a reference to avoid garbage collection
    label.pack()