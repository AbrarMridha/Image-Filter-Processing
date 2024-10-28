# This file contains the functions to create the GUI using tkinter
import tkinter as tk
from tkinter import filedialog, messagebox
from filter_functions import add_noise, triangle_filter, gaussian_filter, median_filter, kuwahara_filter
from image_utils import load_image, display_image


class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing Application")

        # Create GUI elements
        self.create_widgets()
        self.image = None  # Placeholder for loaded image
        self.noisy_image = None

    def create_widgets(self):
        # Upload button
        self.upload_btn = tk.Button(self.root, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack()

        # Add noise button
        self.noise_btn = tk.Button(self.root, text="Add Noise", command=self.add_noise, state=tk.DISABLED)
        self.noise_btn.pack()

        # Apply filter buttons
        self.triangle_btn = tk.Button(self.root, text="Apply Triangle Filter", command=self.apply_triangle_filter,
                                      state=tk.DISABLED)
        self.triangle_btn.pack()

        self.gaussian_btn = tk.Button(self.root, text="Apply Gaussian Filter", command=self.apply_gaussian_filter,
                                      state=tk.DISABLED)
        self.gaussian_btn.pack()

        self.median_btn = tk.Button(self.root, text="Apply Median Filter", command=self.apply_median_filter,
                                    state=tk.DISABLED)
        self.median_btn.pack()

        self.kuwahara_btn = tk.Button(self.root, text="Apply Kuwahara Filter", command=self.apply_kuwahara_filter,
                                      state=tk.DISABLED)
        self.kuwahara_btn.pack()

    def upload_image(self):
        # Open file dialog to select image
        file_path = filedialog.askopenfilename(title="Select an Image",
                                               filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            self.image = load_image(file_path)
            display_image(self.image, title="Original Image")

            # Enable the noise and filter buttons
            self.noise_btn.config(state=tk.NORMAL)
            self.triangle_btn.config(state=tk.NORMAL)
            self.gaussian_btn.config(state=tk.NORMAL)
            self.median_btn.config(state=tk.NORMAL)
            self.kuwahara_btn.config(state=tk.NORMAL)

    def add_noise(self):
        if self.image is not None:
            self.noisy_image = add_noise(self.image)
            display_image(self.noisy_image, title="Noisy Image")
        else:
            messagebox.showerror("Error", "Please upload an image first!")

    def apply_triangle_filter(self):
        if self.noisy_image is not None:
            filtered_image = triangle_filter(self.noisy_image)
            display_image(filtered_image, title="Triangle Filtered Image")
        else:
            messagebox.showerror("Error", "Please add noise to the image first!")

    def apply_gaussian_filter(self):
        if self.noisy_image is not None:
            sigma = 1.0  # You can add an input field to allow user-specified sigma
            filtered_image = gaussian_filter(self.noisy_image, sigma)
            display_image(filtered_image, title="Gaussian Filtered Image")
        else:
            messagebox.showerror("Error", "Please add noise to the image first!")

    def apply_median_filter(self):
        if self.noisy_image is not None:
            filtered_image = median_filter(self.noisy_image)
            display_image(filtered_image, title="Median Filtered Image")
        else:
            messagebox.showerror("Error", "Please add noise to the image first!")

    def apply_kuwahara_filter(self):
        if self.noisy_image is not None:
            filtered_image = kuwahara_filter(self.noisy_image)
            display_image(filtered_image, title="Kuwahara Filtered Image")
        else:
            messagebox.showerror("Error", "Please add noise to the image first!")