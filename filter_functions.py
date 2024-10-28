# This file contains the code for the implementation of the filters.
import numpy as np

# Adding noise to the image
def add_noise(img, noise_amnt = 0.05):
    noisy_img = img.copy()
    num_salt = np.ceil(noise_amnt * img.size * 0.5)
    num_pepper = np.ceil(noise_amnt * img.size * 0.5)

    # Add salt
    coords = [np.random.randint(0, i -1, int(num_salt)) for i in img.shape]
    noisy_img[coords[0], coords[1]] = 255

    # Add pepper
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in img.shape]
    noisy_img[coords[0], coords[1]] = 0

    return noisy_img

# Triangle filter
def triangle_filter(img):
    kernel = np.array([[1, 2, 3, 2, 1],
                       [2, 4, 6, 4, 2],
                       [3, 6, 9, 6, 3],
                       [2, 4, 6, 4, 2],
                       [1, 2, 3, 2, 1]], dtype=np.float32)
    kernel = kernel / np.sum(kernel)
    return apply_convo(img, kernel)

# Gaussian filter
def gaussian_kernel(sigma):
    kernel_size = 5
    kernel = np.zeros((kernel_size, kernel_size), dtype=np.float32)
    center = kernel_size // 2

    for i in range(kernel_size):
        for j in range(kernel_size):
            x, y = i - center, j - center
            kernel[i, j] = np.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))

    kernel /= np.sum(kernel)
    return kernel

def gaussian_filter(img, sigma):
    kernel = gaussian_kernel(sigma)
    return apply_convo(img, kernel)

# Median filter
def median_filter(img, kernel_size = 5):
    x,y,z = img.shape
    filtered_img = np.zeros((x,y,z), dtype=np.uint8)
    pad_width = kernel_size // 2
    padded_img = np.pad(img, ((pad_width, pad_width), (pad_width, pad_width), (0, 0)), mode='edge')

    for k in range(z):  # For each channel (R, G, B)
        for i in range(pad_width, x + pad_width):
            for j in range(pad_width, y + pad_width):
                # Extract the neighborhood for the current channel
                neighborhood = padded_img[i - pad_width:i + pad_width + 1, j - pad_width:j + pad_width + 1, k]

                # Find the median value and assign it to the corresponding pixel
                filtered_img[i - pad_width, j - pad_width, k] = np.median(neighborhood)

    return filtered_img

# Kuwahara filter
def kuwahara_filter(img, kernel_size = 5):
    x,y,z = img.shape
    filtered_img = np.zeros((x,y,z), dtype=np.uint8)
    pad_width = kernel_size // 2
    padded_img = np.pad(img, ((pad_width, pad_width), (pad_width, pad_width), (0, 0)), mode='edge')

    for k in range(z):  # For each channel (R, G, B)
        for i in range(pad_width, x + pad_width):
            for j in range(pad_width, y + pad_width):
                # Define four subregions for the current channel
                regions = [
                    padded_img[i - pad_width:i + 1, j - pad_width:j + 1, k],  # Top-left
                    padded_img[i - pad_width:i + 1, j:j + pad_width + 1, k],  # Top-right
                    padded_img[i:i + pad_width + 1, j - pad_width:j + 1, k],  # Bottom-left
                    padded_img[i:i + pad_width + 1, j:j + pad_width + 1, k]  # Bottom-right
                ]

                # Compute the mean and variance of each region
                region_stats = [(np.mean(region), np.var(region)) for region in regions]

                # Select the region with the smallest variance
                best_region_mean, _ = min(region_stats, key=lambda x: x[1])

                # Assign the best region's mean to the output pixel
                filtered_img[i - pad_width, j - pad_width, k] = best_region_mean
    return filtered_img


def pad_img(image, pad_width):
    x,y,z = image.shape
    padded_img = np.pad(image, ((pad_width, pad_width), (pad_width, pad_width), (0, 0)), mode='edge')

    return padded_img

# Applying convolution
def apply_convo(image, kernel):
    x,y,z= image.shape
    pad_width = kernel.shape[0] // 2
    filtered_image = np.zeros((x, y, z), dtype=np.float32)
    padded_image = np.pad(image, ((pad_width, pad_width), (pad_width, pad_width), (0, 0)), mode='edge')


    for k in range(z):
        for i in range(pad_width, x + pad_width):
            for j in range(pad_width, y + pad_width):
                region = padded_image[i - pad_width:i + pad_width + 1, j - pad_width:j + pad_width + 1, k]
                filtered_image[i - pad_width, j - pad_width, k] = np.sum(region * kernel)

    return np.clip(filtered_image, 0, 255).astype(np.uint8)