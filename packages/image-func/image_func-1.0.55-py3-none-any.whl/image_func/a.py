from PIL import Image
from scipy.fftpack import fft2, ifft2
import numpy as np
import cv2
from skimage.morphology import binary_opening, binary_closing, disk

import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.color import rgb2gray
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from skimage import filters, img_as_float
from PIL import Image
import matplotlib.pylab as pylab

import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage.util import random_noise
from skimage import feature
import numpy as np

def generate_noisy_square(size=128, rotation=15, sigma=4, noise_mode='speckle', noise_mean=0.05):
    image = np.zeros((size, size), dtype=float)
    image[size//4:-size//4, size//4:-size//4] = 1
    image = ndi.rotate(image, rotation, mode='constant')
    image = ndi.gaussian_filter(image, sigma)
    image = random_noise(image, mode=noise_mode, mean=noise_mean)
    return image

def canny_edge_detection(image):
    # Compute the Canny filter for two values of sigma
    edges1 = feature.canny(image)
    edges2 = feature.canny(image, sigma=3)
    return edges1, edges2



def apply_convolution(image, kernel):
    convolved_image = cv2.filter2D(image, -1, kernel)
    return convolved_image

def apply_correlation(image, kernel):
    correlated_image = cv2.filter2D(image, -1, kernel)
    return correlated_image

def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m / sd)

def process_image(image_path):
    im = Image.open(image_path).convert('L')
    im_array = np.array(im)
    
    freq = fft2(im_array)
    im1 = ifft2(freq).real
    
    snr = signaltonoise(im1, axis=None)
    
    return im_array, im1, snr

def perform_fourier_transform(image_path):
    # Read input image and convert to grayscale
    img = cv2.imread(image_path, 0)

    # Calculate optimal size for Fourier transform
    optimalImg = cv2.copyMakeBorder(img, 0, cv2.getOptimalDFTSize(img.shape[0]) - img.shape[0], 0, cv2.getOptimalDFTSize(img.shape[1]) - img.shape[1], cv2.BORDER_CONSTANT, value=0)

    # Calculate the discrete Fourier transform
    dft_shift = np.fft.fftshift(cv2.dft(np.float32(optimalImg), flags=cv2.DFT_COMPLEX_OUTPUT))

    # Calculate magnitude spectrum
    magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]) + 1)

    # Reconstruct the image using inverse Fourier transform
    result = cv2.magnitude(cv2.idft(np.fft.ifftshift(dft_shift))[:, :, 0], cv2.idft(np.fft.ifftshift(dft_shift))[:, :, 1])

    return optimalImg, magnitude_spectrum, result

def apply_log_transform(image_path, output_path):
    # Read the image
    img = cv2.imread(image_path)

    # Apply log transform
    log_transformed = 255 * np.log(1 + img.astype(np.float32)) / np.log(1 + np.max(img))

    # Convert the data type
    log_transformed = log_transformed.astype(np.uint8)

    # Save the output image
    cv2.imwrite(output_path, log_transformed)



def apply_gamma_correction(image, gamma_values):
    gamma_corrected_images = []

    for gamma in gamma_values:
        gamma_corrected = np.array(255 * (image / 255) ** gamma, dtype='uint8')
        gamma_corrected_images.append(gamma_corrected)

    return gamma_corrected_images




def plot_image(image, title=""):
    plt.title(title, size=10)
    plt.imshow(image)
    plt.axis('off')

def plot_hist(channel, title=""):
    plt.hist(np.array(channel).ravel(), bins=256, range=(0, 256), color='r', alpha=0.3)
    plt.xlabel('Pixel Values', size=20)
    plt.ylabel('Frequency', size=20)
    plt.title(title, size=10)

def plot_original(im):
    im_r, im_g, im_b = im.split()
    plt.style.use('ggplot')
    plt.figure(figsize=(15, 5))
    plt.subplot(121)
    plot_image(im)
    plt.subplot(122)
    plot_hist(im_r, "Red Channel")
    plot_hist(im_g, "Green Channel")
    plot_hist(im_b, "Blue Channel")
    plt.yscale('log')
    plt.show()

def contrast(c):
    return 0 if c < 50 else (255 if c > 150 else int((255 * c - 22950) / 48))

def plot_stretched(imc):
    im_rc, im_gc, im_bc = imc.split()
    plt.style.use('ggplot')
    plt.figure(figsize=(15, 5))
    plt.subplot(121)
    plot_image(imc)
    plt.subplot(122)
    plot_hist(im_rc, "Contrast-Adjusted Red Channel")
    plot_hist(im_gc, "Contrast-Adjusted Green Channel")
    plot_hist(im_bc, "Contrast-Adjusted Blue Channel")
    plt.yscale('log')
    plt.show()



def histogram_equalization(image):
    hist = cv2.calcHist([image],[0],None,[256],[0,256])
    eq = cv2.equalizeHist(image)
    cdf = hist.cumsum()
    cdfnmhist = cdf * hist.max() / cdf.max()
    histeq = cv2.calcHist([eq],[0],None,[256],[0,256])
    cdfeq = histeq.cumsum()
    cdfnmhisteq = cdfeq * histeq.max() / cdf.max()
    
    return eq, hist, cdfnmhist, histeq, cdfnmhisteq


import cv2 as cv

def threshold_image(img, threshold_value):
    ret, thresh = cv.threshold(img, threshold_value, 255, cv.THRESH_BINARY)
    return thresh




import numpy as np
from scipy import signal

import matplotlib.pyplot as plt

def plot_image(image, title=""):
    plt.title(title, size=20)
    plt.imshow(image, cmap='gray')
    plt.axis('off')

def apply_gradient(im):
    ker_x = np.array([[-1, 1]])
    ker_y = np.array([[-1], [1]])
    im_x = signal.convolve2d(im, ker_x, mode='same')
    im_y = signal.convolve2d(im, ker_y, mode='same')
    im_mag = np.sqrt(im_x ** 2 + im_y ** 2)
    im_dir = np.arctan2(im_y, im_x)
    return im_x, im_y, im_mag, im_dir

def apply_laplacian(im):
    ker_laplacian = np.array([[0, -1, 0],
                              [-1, 4, -1],
                              [0, -1, 0]])
    im1 = np.clip(signal.convolve2d(im, ker_laplacian, mode='same'), 0, 1)
    return im1




def plot_img(image, title=""):
    pylab.title(title, size=10)
    pylab.imshow(image)
    pylab.axis('off')


def sobel_edge_detection(image):
    edges_x = filters.sobel_h(image)
    edges_y = filters.sobel_v(image)
    return np.clip(edges_x, 0, 1), np.clip(edges_y, 0, 1)



def generate_noisy_square(size=128, rotation=15, sigma=4, noise_mode='speckle', noise_mean=0.05):
    image = np.zeros((size, size), dtype=float)
    image[size//4:-size//4, size//4:-size//4] = 1
    image = ndi.rotate(image, rotation, mode='constant')
    image = ndi.gaussian_filter(image, sigma)
    image = random_noise(image, mode=noise_mode, mean=noise_mean)
    return image

def canny_edge_detection(image):
    # Compute the Canny filter for two values of sigma
    edges1 = feature.canny(image)
    edges2 = feature.canny(image, sigma=3)
    return edges1, edges2
def plot_canny(image, title="", ax=None):
    if ax is None:
        ax = pylab.gca()
    ax.set_title(title, fontsize=10)
    ax.imshow(image, cmap='gray')
    ax.axis('off')



def erosion(image, kernel_size):
    return cv2.erode(image, np.ones((kernel_size, kernel_size), np.uint8), iterations=1)

def dilation(image, kernel_size):
    return cv2.dilate(image, np.ones((kernel_size, kernel_size), np.uint8), iterations=1)

def opening(image, disk_size):
    return binary_opening(image, disk(disk_size))

def closing(image, disk_size):
    return binary_closing(image, disk(disk_size))
def threshold_image(image, threshold_value):
    _, binary_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    return binary_image



def load_image(file_path):
    img = cv2.imread(file_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def convert_to_gray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return gray

def threshold_image(image):
    ret, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh

def segment_image(image):
    kernel = np.ones((3, 3), np.uint8)
    closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=15)
    bg = cv2.dilate(closing, kernel, iterations=1)
    dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 0)
    ret, fg = cv2.threshold(dist_transform, 0.02 * dist_transform.max(), 255, 0)
    return fg

def plot_image(image, title=""):
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.title(title)
    plt.show()
def plot_images(image, title=""):
    plt.imshow(image, cmap='gray')
    plt.title(title, fontsize=10)
    plt.axis('off')


def fft():
    code = """
import matplotlib.pyplot as plt
from image_func import process_image

# Provide the path to the image file
image_path = r"C:\\Users\\arman\\Pictures\\floweer.jpg"

# Process the image using the process_image function from the sigtonoise package
processed_image, reconstructed_image, snr = process_image(image_path)

# Display the original image
plt.figure(figsize=(10, 5))
plt.imshow(processed_image, cmap='gray')
plt.axis('off')
plt.title('ORIGINAL IMAGE', size=15)
plt.show()

# Display the reconstructed image with SNR
plt.figure(figsize=(10, 5))
plt.imshow(reconstructed_image, cmap='gray')
plt.axis('off')
plt.title(f'IMAGE OBTAINED AFTER RECONSTRUCTION\nSNR: {snr:.2f}', size=15)
plt.show()
"""
    print(code)

def convolution():
    code=r"""
import cv2a
import numpy as np
from image_func import apply_convolution, apply_correlation
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread(r"C:\Users\arman\Pictures\floweer.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Define a convolution kernel
conv_kernel = np.ones((3, 3), np.float32) / 9

# Perform convolution
convolved_image = apply_convolution(image, conv_kernel)

# Define a correlation kernel
corr_kernel = np.array([[0, -1, 0],
                        [-1, 5, -1],
                        [0, -1, 0]])

# Perform correlation
correlated_image = apply_correlation(image, corr_kernel)

# Display the results or perform additional processing
# ...
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

axes[0].imshow(image)
axes[0].axis('off')
axes[0].set_title('Original Image')

axes[1].imshow(convolved_image)
axes[1].axis('off')
axes[1].set_title('Convolved Image')

axes[2].imshow(correlated_image)
axes[2].axis('off')
axes[2].set_title('Correlated Image')

plt.tight_layout()
plt.show()
"""
    print(code)

def dft():
    code=r""" import matplotlib.pyplot as plt
from image_func import perform_fourier_transform

# Specify the image path
image_path = r"C:\Users\arman\Pictures\floweer.jpg"

# Perform Fourier transform
optimalImg, DFT, result = perform_fourier_transform(image_path)

# Display the results
images = [optimalImg, DFT, result]
imageTitles = ['Input image', 'DFT', 'Reconstructed image']

for i in range(len(images)):
    plt.subplot(1, 3, i + 1)
    plt.imshow(images[i], cmap='gray')
    plt.title(imageTitles[i])
    plt.xticks([])
    plt.yticks([])

plt.show()
"""
    print(code)

def log():
    code=r"""import cv2
import numpy as np
import matplotlib.pyplot as plt
from image_func import apply_log_transform

# Specify the image paths
input_image_path = r"C:\IP practicals\floweer.jpg"
output_image_path = r"C:\IP practicals\floweer1.jpg"

# Apply log transform
apply_log_transform(input_image_path, output_image_path)

# Display the original and log-transformed images
img = cv2.imread(input_image_path)
log_transformed = cv2.imread(output_image_path)

plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original Image')

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(log_transformed, cv2.COLOR_BGR2RGB))
plt.title('Log-Transformed Image')

plt.show()
"""
    print(code)

def power():
    code=r"""import cv2
import numpy as np
from image_func import apply_gamma_correction

# Specify the image path
image_path = r"C:\IP practicals\floweer.jpg"

# Specify the gamma values
gamma_values = [0.1, 0.5, 1.2, 2.2, 5]

# Read the image
img = cv2.imread(image_path)

# Apply gamma correction
gamma_corrected_images = apply_gamma_correction(img, gamma_values)

# Display the original image
cv2.imshow('Original Image', img)
cv2.waitKey(0)

# Display the gamma-corrected images
for gamma_corrected in gamma_corrected_images:
    cv2.imshow('Gamma Corrected Image', gamma_corrected)
    cv2.waitKey(0)

cv2.destroyAllWindows()
"""
    print(code)

def contrast():
    code=r"""
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from image_func import plot_original, plot_stretched, contrast

image_path = r"C:\IP practicals\floweer.jpg"
im = Image.open(image_path)

plot_original(im)

imc = im.point(contrast)

plot_stretched(imc)
"""
    print(code)

def histogram():
    code=r"""
import cv2
import matplotlib.pyplot as plt

from image_func import histogram_equalization

# Read the image
image_path = r"C:\IP practicals\floweer.jpg"
img = cv2.imread(image_path, 0)

# Perform histogram equalization
equalized_image, original_hist, original_cdf_hist, equalized_hist, equalized_cdf_hist = histogram_equalization(img)

# Plot the images and histograms
plt.subplot(221), plt.imshow(img, 'gray')
plt.subplot(222), plt.plot(original_hist), plt.plot(original_cdf_hist)
plt.subplot(223), plt.imshow(equalized_image, 'gray')
plt.subplot(224), plt.plot(equalized_hist), plt.plot(equalized_cdf_hist)
plt.xlim([0, 256])
plt.show()
"""
    print(code)

def threshold():
    code=r"""
import cv2
import numpy as np
from matplotlib import pyplot as plt
from image_func import threshold_image

# Load the image
img = cv2.imread(r"C:\IP practicals\floweer.jpg")
# Set the threshold value
threshold_value = 127

# Perform thresholding using the threshold_image function
thresh = threshold_image(img, threshold_value)

# Plot the images manually
titles = ['Original Image', 'Thresholded']
images = [img, thresh]
for i in range(2):
    plt.subplot(1, 2, i + 1)
    plt.imshow(images[i], 'gray', vmin=0, vmax=255)
    plt.title(titles[i])
    plt.xticks([])
    plt.yticks([])
plt.show()
"""
    print(code)

def gradient():
    code=r"""
from skimage.io import imread
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from image_func import plot_image, apply_gradient, apply_laplacian

im = rgb2gray(imread(r"C:\IP practicals\floweer.jpg"))

# Apply gradient
im_x, im_y, im_mag, im_dir = apply_gradient(im)

# Plot the gradient results
plt.gray()
plt.figure(figsize=(20, 15))
plt.subplot(231)
plot_image(im, 'Original')
plt.subplot(232)
plot_image(im_x, 'Gradient x')
plt.subplot(233)
plot_image(im_y, 'Gradient y')
plt.subplot(234)
plot_image(im_mag, '||Gradient||')
plt.legend(prop={'size': 20})
plt.show()

# Apply Laplacian
im1 = apply_laplacian(im)

# Plot the Laplacian result
plt.gray()
plt.figure(figsize=(10, 5))
plt.subplot(121)
plot_image(im, 'Original')
plt.subplot(122)
plot_image(im1, 'Laplacian Convolved')
plt.show()
"""
    print(code)

def sharpening():
    code=r"""
import numpy as np
from skimage import filters, img_as_float, color
from skimage.io import imread
import matplotlib.pyplot as plt

def plot_image(image, title=""):
    plt.title(title, size=10)
    plt.imshow(image, cmap='gray')
    plt.axis('off')

def sharpen_image(image):
    blurred = filters.gaussian(image, sigma=3)
    detail = np.clip(image - blurred, 0, 1)
    alpha_values = [1, 5, 10]

    fig, axes = plt.subplots(nrows=2, ncols=3, sharex=True, sharey=True, figsize=(15, 15))
    axes = axes.ravel()
    axes[0].set_title('Original Image', size=15)
    axes[0].imshow(image, cmap='gray')
    
    axes[1].set_title('Blurred Image (sigma=3)', size=15)
    axes[1].imshow(blurred, cmap='gray')
    
    axes[2].set_title('Detail Image', size=15)
    axes[2].imshow(detail, cmap='gray')
    for i, alpha in enumerate(alpha_values):
        sharpened = np.clip(image + alpha * detail, 0, 1)
        axes[3+i].imshow(sharpened, cmap='gray')
        axes[3+i].set_title(f'Sharpened Image (alpha={alpha})', size=15)
    for ax in axes:
        ax.axis('off')
    fig.tight_layout()
    plt.show()

# Load the grayscale image
image = color.rgb2gray(imread(r"C:\Users\Aditi\OneDrive\Pictures\IP\flower.jpg"))

# Perform sharpening and display the results
sharpen_image(image)
"""
    print(code)

def edge():
    code=r"""
import numpy as np
from skimage import filters, img_as_float, color
from skimage.io import imread
import matplotlib.pyplot as plt

def plot_image(image, title=""):
    plt.title(title, size=10)
    plt.imshow(image, cmap='gray')
    plt.axis('off')

def sharpen_image(image):
    blurred = filters.gaussian(image, sigma=3)
    detail = np.clip(image - blurred, 0, 1)
    alpha_values = [1, 5, 10]

    fig, axes = plt.subplots(nrows=2, ncols=3, sharex=True, sharey=True, figsize=(15, 15))
    axes = axes.ravel()
    axes[0].set_title('Original Image', size=15)
    axes[0].imshow(image, cmap='gray')
    
    axes[1].set_title('Blurred Image (sigma=3)', size=15)
    axes[1].imshow(blurred, cmap='gray')
    
    axes[2].set_title('Detail Image', size=15)
    axes[2].imshow(detail, cmap='gray')
    for i, alpha in enumerate(alpha_values):
        sharpened = np.clip(image + alpha * detail, 0, 1)
        axes[3+i].imshow(sharpened, cmap='gray')
        axes[3+i].set_title(f'Sharpened Image (alpha={alpha})', size=15)
    for ax in axes:
        ax.axis('off')
    fig.tight_layout()
    plt.show()

# Load the grayscale image
image = color.rgb2gray(imread(r"C:\Users\Aditi\OneDrive\Pictures\IP\flower.jpg"))

# Perform sharpening and display the results
sharpen_image(image)
"""
    print(code)

def canny():
    code=r"""
import matplotlib.pylab as pylab
from skimage import feature
from image_func import plot_canny, generate_noisy_square, canny_edge_detection

# Generate noisy image of a square
image = generate_noisy_square()

# Perform Canny edge detection
edges1, edges2 = canny_edge_detection(image)

# Display results
# Display results
fig, ax = pylab.subplots(nrows=1, ncols=3, figsize=(8, 3))

plot_canny(image, 'noisy image', ax=ax[0])

plot_canny(edges1, r'Canny filter, $\sigma=1$', ax=ax[1])

plot_canny(edges2, r'Canny filter, $\sigma=3$', ax=ax[2])

pylab.show()


"""
    print(code)

def sobel():
    code=r"""
from skimage.io import imread
from PIL import Image
import matplotlib.pylab as pylab
import numpy as np
from skimage import filters
from image_func import plot_image ,sobel_edge_detection

image_path = r"C:\IP practicals\floweer.jpg"

# Open and convert the image to grayscale
im = Image.open(image_path).convert('L')
im_array = np.array(im)
# Perform Sobel edge detection
edges_x, edges_y = sobel_edge_detection(im_array)

# Display the images
pylab.gray()
pylab.figure(figsize=(15, 15))
pylab.subplot(2, 2, 1)
plot_image(im, 'Original')
pylab.subplot(2, 2, 2)
plot_image(edges_x, 'Sobel X')
pylab.subplot(2, 2, 3)
plot_image(edges_y, 'Sobel Y')
pylab.subplot(2, 2, 4)
plot_image(edges_x + edges_y, 'Sobel X + Y')
pylab.subplots_adjust(wspace=0.1, hspace=0.1)
pylab.show()
"""
    print(code)

def erosion():
    code=r"""
import cv2
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.io import imread
import matplotlib.pylab as pylab
from image_func import threshold_image, erosion, dilation, opening, closing, plot_image


# Erosion and Dilation
img = cv2.imread(r"C:\IP practicals\floweer.jpg", 0)
bw_img = threshold_image(img, 127)

kernel_size = 5
img_erosion = erosion(img, kernel_size)
img_dilation = dilation(img, kernel_size)

plt.figure(figsize=(5, 5))
plot_image(img, "ORIGINAL IMAGE")
plt.show()
plot_image(img_erosion, "EROSION")
plt.show()
plot_image(img_dilation, "DILATION")
plt.show()

# Image opening and closing
im = rgb2gray(imread(r"C:\IP practicals\floweer.jpg"))
im[im <= 0.5] = 0
im[im > 0.5] = 1

disk_size = 6
im_opening = opening(im, disk_size)
im_closing = closing(im, disk_size)

pylab.gray()
pylab.figure(figsize=(20, 10))
plot_image(im, "original")
plot_image(im_opening, "opening with disk size 6")
plt.show()
plot_image(im_closing, "closing with disk size 6")
pylab.show()
"""
    print(code)

def segmentation():
    code=r"""
from image_func import load_image, convert_to_gray, threshold_image, segment_image,plot_images
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Loading original image
img = load_image(r'C:\IP practicals\floweer.jpg')

# Converting to grayscale
gray = convert_to_gray(img)

# Thresholding image
thresh = threshold_image(gray)

# Segmenting the image
segmented = segment_image(thresh)


# Displaying final output
plt.figure(figsize=(10, 10))
plt.subplot(2, 2, 1)
plot_images(img, "Original Image")
plt.subplot(2, 2, 2)
plot_images(gray, "Grayscale Image")
plt.subplot(2, 2, 3)
plot_images(thresh, "Threshold Image")
plt.subplot(2, 2, 4)
plot_images(segmented, "Segmented Image")
plt.tight_layout()
plt.show()
"""
    print(code)

def all():
    code="""
fft()
convolution()
dft()
log()
power()
contrast()
histogram()
threshold()
gradient()
sharpening()
edge()
canny()
sobel()
erosion()
segmentation()
"""
    print(code)



def onlySegmentation():
    code=r"""
import numpy as np
import cv2
from matplotlib import pyplot as plt

# Loading original image
img = cv2.imread(r'bird.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Converting to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Converting to binary inverted image
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Segmenting the images
kernel = np.ones((3, 3), np.uint8)
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=15)
bg = cv2.dilate(closing, kernel, iterations=1)
dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 0)
ret, fg = cv2.threshold(dist_transform, 0.02 * dist_transform.max(), 255, 0)

# Plotting the images
plt.figure(figsize=(10, 10))

plt.subplot(2, 2, 1)
plt.imshow(img, cmap="gray")
plt.axis('off')
plt.title("Original Image")

plt.subplot(2, 2, 2)
plt.imshow(gray, cmap="gray")
plt.axis('off')
plt.title("GrayScale Image")

plt.subplot(2, 2, 3)
plt.imshow(thresh, cmap="gray")
plt.axis('off')
plt.title("Threshold Image")

plt.subplot(2, 2, 4)
plt.imshow(fg, cmap="gray")
plt.axis('off')
plt.title("Segmented Image")

plt.show()
"""
    print(code)


def onlyErosionDilation():
    code=r"""
import cv2
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.io import imread
import matplotlib.pylab as pylab
from image_func import threshold_image, erosion, dilation, opening, closing, plot_image


# Erosion and Dilation
img = cv2.imread(r"bird.jpg", 0)
bw_img = threshold_image(img)

kernel_size = 5
img_erosion = erosion(img, kernel_size)
img_dilation = dilation(img, kernel_size)

plt.figure(figsize=(5, 5))
plot_image(img, "ORIGINAL IMAGE")
plt.show()
plot_image(img_erosion, "EROSION")
plt.show()
plot_image(img_dilation, "DILATION")
plt.show()

# Image opening and closing
im = rgb2gray(imread(r"bird.jpg"))
im[im <= 0.5] = 0
im[im > 0.5] = 1

disk_size = 6
im_opening = opening(im, disk_size)
im_closing = closing(im, disk_size)

pylab.gray()
pylab.figure(figsize=(20, 10))
plot_image(im, "original")
plot_image(im_opening, "opening with disk size 6")
plt.show()
plot_image(im_closing, "closing with disk size 6")
pylab.show()
"""
    print(code)


def onlyRobertPrewitt():
    code=r"""
import numpy as np
from skimage import filters
from PIL import Image
import matplotlib.pylab as pylab
from image_func import plot_img

def edge_detection(image_path):
    im = Image.open(image_path).convert('L')
    im_arr = np.asarray(im)
    pylab.gray()
    pylab.figure(figsize=(15, 15))
    pylab.subplot(3, 2, 1), plot_img(im, 'Original Image')
    edges = filters.roberts(im_arr)
    pylab.subplot(3, 2, 2), plot_img(edges, 'Roberts')
    edges = filters.scharr(im_arr)
    pylab.subplot(3, 2, 3), plot_img(edges, 'Scharr')
    edges = filters.sobel(im_arr)
    pylab.subplot(3, 2, 4), plot_img(edges, 'Sobel')
    edges = filters.prewitt(im_arr)
    pylab.subplot(3, 2, 5), plot_img(edges, 'Prewitt')
    edges = np.clip(filters.laplace(im_arr), 0, 1)
    pylab.subplot(3, 2, 6), plot_img(edges, 'Laplace')
    pylab.subplots_adjust(wspace=0.1, hspace=0.1)
    pylab.show()

# Set the path to the image
image_path = r"bird.jpg"

# Call the edge_detection function
edge_detection(image_path)
"""
    print(code)


def onlySobel():
    code=r"""
import numpy as np
from skimage import filters
from skimage.io import imread
import matplotlib.pyplot as plt

im = imread(r"bird.jpg", as_gray=True)

plt.gray()
fig, axes = plt.subplots(2, 2, figsize=(15, 15))

titles = ['Original', 'Sobel x', 'Sobel y', 'Sobel']
images = [im, filters.sobel_h(im), filters.sobel_v(im), filters.sobel(im)]

for ax, title, image in zip(axes.ravel(), titles, images):
    ax.imshow(np.clip(image, 0, 1), cmap='gray')
    ax.set_title(title)
    ax.axis('off')

plt.tight_layout()
plt.show()
"""
    print(code)


def onlyCanny():
    code=r"""
import matplotlib.pyplot as plt
from skimage.util import random_noise
from skimage import feature

# Generate noisy image of a square
image = random_noise(feature.square(128), mode='speckle', mean=0.05)

# Compute the Canny filter for two values of sigma
edges1 = feature.canny(image)
edges2 = feature.canny(image, sigma=3)

# Display results
fig, ax = plt.subplots(1, 3, figsize=(8, 3))

ax[0].imshow(image, cmap='gray')
ax[0].set_title('noisy image', fontsize=10)

ax[1].imshow(edges1, cmap='gray')
ax[1].set_title(r'Canny filter, $\sigma=1$', fontsize=10)

ax[2].imshow(edges2, cmap='gray')
ax[2].set_title(r'Canny filter, $\sigma=3$', fontsize=10)

for a in ax:
    a.axis('off')

plt.tight_layout()
plt.show()
"""
    print(code)


def onlySharpening():
    code=r"""
import numpy as np
from skimage import filters, img_as_float, color
from skimage.io import imread
import matplotlib.pyplot as plt

def plot_image(image, title=""):
    plt.title(title, size=10)
    plt.imshow(image, cmap='gray')
    plt.axis('off')

def sharpen_image(image):
    blurred = filters.gaussian(image, sigma=3)
    detail = np.clip(image - blurred, 0, 1)
    alpha_values = [1, 5, 10]

    fig, axes = plt.subplots(nrows=2, ncols=3, sharex=True, sharey=True, figsize=(15, 15))
    axes = axes.ravel()
    axes[0].set_title('Original Image', size=15)
    axes[0].imshow(image, cmap='gray')
    
    axes[1].set_title('Blurred Image (sigma=3)', size=15)
    axes[1].imshow(blurred, cmap='gray')
    
    axes[2].set_title('Detail Image', size=15)
    axes[2].imshow(detail, cmap='gray')
    for i, alpha in enumerate(alpha_values):
        sharpened = np.clip(image + alpha * detail, 0, 1)
        axes[3+i].imshow(sharpened, cmap='gray')
        axes[3+i].set_title(f'Sharpened Image (alpha={alpha})', size=15)
    for ax in axes:
        ax.axis('off')
    fig.tight_layout()
    plt.show()

# Load the grayscale image
image = color.rgb2gray(imread(r"flower.jpg"))

# Perform sharpening and display the results
sharpen_image(image)
"""
    print(code)


def onlyGradientLaplacian():
    code=r"""
from skimage.io import imread
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from image_func import plot_image, apply_gradient, apply_laplacian

im = rgb2gray(imread(r"C:\IP practicals\floweer.jpg"))

# Apply gradient
im_x, im_y, im_mag, im_dir = apply_gradient(im)

# Plot the gradient results
plt.gray()
plt.figure(figsize=(20, 15))
plt.subplot(231)
plot_image(im, 'Original')
plt.subplot(232)
plot_image(im_x, 'Gradient x')
plt.subplot(233)
plot_image(im_y, 'Gradient y')
plt.subplot(234)
plot_image(im_mag, '||Gradient||')
plt.legend(prop={'size': 20})
plt.show()

# Apply Laplacian
im1 = apply_laplacian(im)

# Plot the Laplacian result
plt.gray()
plt.figure(figsize=(10, 5))
plt.subplot(121)
plot_image(im, 'Original')
plt.subplot(122)
plot_image(im1, 'Laplacian Convolved')
plt.show()
"""
    print(code)


def onlyContrasting():
    code=r"""
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
def plot_image(image, title=""):
    plt.title(title, size=10)
    plt.imshow(image)
    plt.axis('off')
def plot_hist(channel, title=""):
    plt.hist(np.array(channel).ravel(), bins=256, range=(0, 256), color='r', alpha=0.3)
    plt.xlabel('Pixel Values', size=20)
    plt.ylabel('Frequency', size=20)
    plt.title(title, size=10)
image_path = r"flower.jpg"
im = Image.open(image_path)
im_r, im_g, im_b = im.split()
plt.style.use('ggplot')
plt.figure(figsize=(15, 5))
plt.subplot(121)
plot_image(im)
plt.subplot(122)
plot_hist(im_r, "Red Channel")
plot_hist(im_g, "Green Channel")
plot_hist(im_b, "Blue Channel")
plt.yscale('log')
plt.show()

def contrast(c):
    return 0 if c < 50 else (255 if c > 150 else int((255 * c - 22950) / 48))

imc = im.point(contrast)
im_rc, im_gc, im_bc = imc.split()

plt.style.use('ggplot')
plt.figure(figsize=(15, 5))

plt.subplot(121)
plot_image(imc)
plt.subplot(122)
plot_hist(im_rc, "Contrast-Adjusted Red Channel")
plot_hist(im_gc, "Contrast-Adjusted Green Channel")
plot_hist(im_bc, "Contrast-Adjusted Blue Channel")
plt.yscale('log')
plt.show()
"""
    print(code)


def onlyThresholding():
    code=r"""
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
img = cv.imread(r"C:\Users\Aditi\Pictures\IP\flower.jpg", 0)
ret, thresh1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
ret, thresh2 = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)
ret, thresh3 = cv.threshold(img, 127, 255, cv.THRESH_TRUNC)
ret, thresh4 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO)
ret, thresh5 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO_INV)
titles = ['Original Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
for i in range(6):
    plt.subplot(2, 3, i + 1)
    plt.imshow(images[i], 'gray', vmin=0, vmax=255)
    plt.title(titles[i])
    plt.xticks([])
    plt.yticks([])
plt.show()
"""
    print(code)


def onlyDFT():
    code=r"""
import numpy as np
import cv2
import matplotlib.pyplot as plt

img=cv2.imread(r"flower.jpg",0)

optimalImg=cv2.copyMakeBorder(img, 0, cv2.getOptimalDFTSize(img.shape[0])
                              -img.shape[0], 0, cv2.getOptimalDFTSize(img.shape[1])
                              -img.shape[1], cv2.BORDER_CONSTANT, value=0)
dft_shift=np.fft.fftshift(cv2.dft(np.float32(optimalImg), flags=cv2.DFT_COMPLEX_OUTPUT))
magnitude_spectrum=20*np.log(cv2.magnitude(dft_shift[:,:,0],
                                           dft_shift[:,:,1])+1)
result=cv2.magnitude(cv2.idft(np.fft.ifftshift(dft_shift))[:,:,0],
                     cv2.idft(np.fft.ifftshift(dft_shift))[:,:,1])

images=[optimalImg, magnitude_spectrum, result]
imagesTitles=["Input", "DFT", "Output"]

for i in range(len(images)):
    plt.subplot(1, 3, i+1)
    plt.imshow(images[i], cmap="gray")
    plt.title(imagesTitles[i])
    plt.xticks([])
    plt.yticks([])
plt.show()
"""
    print(code)


def onlyConvCorr():
    code=r"""
import cv2
import matplotlib.pyplot as plt
import numpy as np
from image_func import apply_convolution, apply_correlation
img=cv2.imread(r"flower.jpg")
#img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

k1=np.ones((3,3), np.float32)/9
c1=apply_convolution(img, k1)

k2=np.array([[0, -1, 0],
             [-1, 5, -1],
             [0, -1, 0]])
c2=apply_correlation(img, k2)

fig, axes=plt.subplots(1, 3, figsize=(12, 4))
axes[0].imshow(img)
axes[0].axis("off")
axes[0].set_title("Original")

axes[1].imshow(c1)
axes[1].axis("off")
axes[1].set_title("Convolution")
 
axes[2].imshow(c2)
axes[2].axis("off")
axes[2].set_title("Correlation")

plt.tight_layout()
plt.show()
"""
    print(code)


def onlyHaar():
    code=r"""
import cv2
import numpy as np

# Load the image
image = cv2.imread(r"bird.jpg", 0)

# Convert the image to floating-point data type
image_float = np.float32(image)

# Apply the DCT
transformed = cv2.dct(image_float)

# Display the transformed image
cv2.imshow("Transformed Image", transformed)
"""
    print(code)


def onlyColorModel():
    code=r"""
import cv2

# Load the image
image = cv2.imread(r"bird.jpg")

# Convert the image to a different color model
converted_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Display the transformed image
cv2.imshow("Converted Image", converted_image)
"""
    print(code)


def onlyHistogram():
    code=r"""
import cv2
from matplotlib import pyplot as plt
img = cv2.imread(r"flower.jpg",0)
hist = cv2.calcHist([img],[0],None,[256],[0,256])
eq = cv2.equalizeHist(img)
cdf = hist.cumsum()
cdfnmhist = cdf * hist.max()/ cdf.max()
histeq = cv2.calcHist([eq],[0],None,[256],[0,256])
cdfeq = histeq.cumsum()
cdfnmhisteq = cdfeq * histeq.max()/ cdf.max()
plt.subplot(221), plt.imshow(img,'gray')
plt.subplot(222), plt.plot(hist), plt.plot(cdfnmhist)
plt.subplot(223), plt.imshow(eq,'gray')
plt.subplot(224), plt.plot(histeq), plt.plot(cdfnmhisteq)
plt.xlim([0,256])
plt.show()
"""
    print(code)


def onlyPowerLaw():
    code=r"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
# Read the image
img = cv2.imread(r"flower.jpg")
# Display the original image
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()
# Define gamma values
gamma_values = [0.1, 0.5, 1.2, 2.2, 5]
# Apply gamma correction and save edited images
for gamma in gamma_values:
    gamma_corrected = np.array(255 * (img / 255) ** gamma, dtype='uint8')
    cv2.imwrite('gamma_transformed' + str(gamma) + '.jpg', gamma_corrected)
    plt.imshow(cv2.cvtColor(gamma_corrected, cv2.COLOR_BGR2RGB))
    plt.show()
"""
    print(code)


def onlyLog():
    code=r"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
# Read the image
img = cv2.imread(r"C:\Users\Aditi\OneDrive\Pictures\IP\flower.jpg")
# Apply log transform
log_transformed = 255 * np.log(1 + img.astype(np.float32)) / np.log(1 + np.max(img))
# Convert the data type
log_transformed = log_transformed.astype(np.uint8)
# Save the output image
cv2.imwrite(r"C:\Users\Aditi\Pictures\IP\flower1.jpg", log_transformed)
# Display the original and log-transformed images
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original Image')
plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(log_transformed, cv2.COLOR_BGR2RGB))
plt.title('Log-Transformed Image')
plt.show()
"""
    print(code)
    
def onlyall():
    code=r"""
onlySegmentation()
onlyErosionDilation()
onlyRobertPrewitt()
onlySobel()
onlyCanny()
onlySharpening()
onlyGradientLaplacian()
onlyContrasting()
onlyThresholding()
onlyDFT()
onlyConvCorr()
onlyHaar()
onlyColorModel()
onlyHistogram()
onlyPowerLaw()
onlyLog()
"""
    print(code)

def awp():
    code=r"""
Topic Working with basic C#
1. Working with basic C#
a) Create an application that obtains four int values from the user and displays the product.
CODE:
using System;
namespace qwefgh
{
 class Program
 {
 static void Main(string[] args)
 {
 int num1, num2, num3, num4, prod;
 Console.Write("Enter number 1: ");
 num1 = Convert.ToInt32(Console.ReadLine());
 Console.Write("Enter number 2: ");
 num2 = Convert.ToInt32(Console.ReadLine());
 Console.Write("Enter number 3: ");
 num3 = Convert.ToInt32(Console.ReadLine());
 Console.Write("Enter number 4: ");
 num4 = Convert.ToInt32(Console.ReadLine());
 prod = num1 * num2 * num3 * num4;
 Console.WriteLine(num1 + "*" + num2 + "*" + num3 + "*" + num4 + "=" + prod);
 Console.ReadKey();
 }
 }
}
Output:
Vidyalankar School of Information Technology
b) Create an application to demonstrate string operations
 Code:
using System;
namespace qwefgh
{
 class Program
 {
 static void Main(string[] args)
 {
 string str = " Life is Best at VSIT ";
 Console.WriteLine("Trim:" + str.Trim());
 Console.WriteLine("String is:" + str);
 Console.WriteLine("ToUpper:" + str.ToUpper());
 Console.WriteLine("ToLower:" + str.ToLower());
 Console.WriteLine("Contains good:" + str.Contains("good"));
 Console.WriteLine("Startswith Life:" + str.StartsWith(" Life"));
 Console.WriteLine("Startswith vsit: " + str.StartsWith("vsit"));
 Console.WriteLine("IndexOf i:" + str.IndexOf("i"));
 Console.WriteLine("LastIndexOf i:" + str.LastIndexOf("i"));
 Console.WriteLine("Lenght:" + str.Length);
 Console.WriteLine("Remove 4:" + str.Remove(4));
 Console.WriteLine("Replace i with e : " + str.Replace('i', 'e'));
 Console.WriteLine("Insert Hey:" + str.Insert(0, "Hey "));
 Console.WriteLine("Substring 0,8:" + str.Substring(0, 8));
 Console.WriteLine("ToCharArray():");
 char[] charArray = str.ToCharArray();
 foreach (char c in charArray)
 {
 Console.WriteLine(c);
 }
 Console.ReadKey();
 }
 }
}
Output:
Vidyalankar School of Information Technology
c) Create an application that receives the (Student Id, Student Name, Course Name, Date of Birth) information
from a set of students. The application should also display the information of all the students once the data
entered.
Code:
using System;
namespace qwefgh
{
 class structure
 {
 struct Student
 {
 public string studId, name, cname;
 public int day, month, year;
 }
 static void Main(string[] args)
 {
 Student[] s = new Student[5];
 int i;
 for (i = 0; i < 5; i++)
 {
 Console.Write("Enter Student ID: ");
 s[i].studId = Console.ReadLine();
 Console.Write("Enter Student name: ");
 s[i].name = Console.ReadLine();
 Console.Write("Enter course name: ");
Vidyalankar School of Information Technology
 s[i].cname = Console.ReadLine();
 Console.Write("Enter date of birth\nEnter day(1-31): ");
 s[i].day = Convert.ToInt32(Console.ReadLine());
 Console.Write("Enter month(1-12): ");
 s[i].month = Convert.ToInt32(Console.ReadLine());
 Console.Write("Enter year: ");
 s[i].year = Convert.ToInt32(Console.ReadLine());
 }
 Console.WriteLine("\n\nStudent's List\n");
 for (i = 0; i < 5; i++)
 {
 Console.Write("\n\nStudent ID: " + s[i].studId);
 Console.Write("\tStudent name: " + s[i].name);
 Console.Write("\nCourse name: " + s[i].cname);
 Console.Write("\nDate of birth(dd-mm-yy): " + s[i].day + "-" +
 s[i].month + "-" + s[i].year);
 }
 Console.ReadKey();
 }
 }
}
Output:
d) Create an application to demonstrate following operations:
i. Generate Fibonacci series.
Vidyalankar School of Information Technology
ii. Test for prime numbers.
iii. Test for vowels.
iv. Use of foreach loop with arrays
1.Code:
using System;
namespace qwefgh
{
 class structure
 {
 static void Main(string[] args)
 {
 int n1 = 0, n2 = 1, n3, n;
 Console.Write("Enter a number: ");
 n = Convert.ToInt32(Console.ReadLine());
 Console.Write("\nFibonacci Series\n");
 Console.Write(n1 + "\t" + n2);
 for (int i = 3; i <= n; i++)
 {
 n3 = n1 + n2;
 Console.Write("\t" + n3);
 n1 = n2;
 n2 = n3;
 }
 Console.ReadKey();
 }
 }
}
Output:
2.Code:
using System;
namespace qwefgh
{
 class structure
 {
 static void Main(string[] args)
 {
 int num, counter;
 Console.Write("Enter number:");
Vidyalankar School of Information Technology
 num = int.Parse(Console.ReadLine());
 for (counter = 2; counter <= num / 2; counter++)
 {
 if ((num % counter) == 0)
 break;
 }
 if (num == 1)
 Console.WriteLine(num + " is neither prime nor composite");
 else if (counter <= (num / 2))
 Console.WriteLine(num + " is not prime number");
 else
 Console.WriteLine(num + " is prime number");
 Console.ReadKey();
 }
 }
}
Output:
3.Code:
using System;
namespace qwefgh
{
 class Vowels
 {
 static void Main(string[] args)
 {
 char ch;
 Console.Write("Enter a character: ");
 ch = (char)Console.Read();
 switch (ch)
 {
 case 'a':
 case 'A':
 case 'E':
Vidyalankar School of Information Technology
 case 'e':
 case 'I':
 case 'i':
 case 'O':
 case 'o':
 case 'U':
 case 'u':
 Console.WriteLine(ch + " is Vowel");
 break;
 default:
 Console.WriteLine(ch + " is not a vowel");
 break;
 }
 Console.ReadKey();
 }
 }
}
Output:
4.Code
using System;
namespace qwefgh
{
 class Vowels
 {
 static void Main(string[] args)
 {
 string[] str = { "Advanced", "Web", "Programming" };
 foreach (string s in str)
 {
 Console.WriteLine(s);
 }
 Console.ReadKey();
 }
 }
}
Vidyalankar School of Information Technology
Vidyalankar School of Information Technology
Advanced Web Programming
Practical #2
1. Working with Object Oriented C#
a. Create simple application to perform following operations i. Finding factorial Value ii. Money Conversion iii.
Quadratic Equation iv. Temperature Conversion
i. Finding factorial Value
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
namespace ConsoleApp4
{
 class Program
 {
 static void Main(string[] args)
 {
 Console.WriteLine("Enter the number: ");
 int a = Convert.ToInt32(Console.ReadLine());
 int fact = 1;
 for (int x = 1; x <= a; x++)
 {
 fact *= x;
 }
 Console.WriteLine(fact);
 Console.ReadLine();
 }
 }
}
ii. Money Conversion
using System;
namespace ConsoleApplication1
{
Vidyalankar School of Information Technology
class MoneyConversion
{
static void Main(string[] args)
{
int choice;
Console.WriteLine("Enter your Choice:\n 1- Dollar to Rupee\n 2- Euro to Rupee \n 3 Malaysian Ringgit to
Rupee ");
choice = int.Parse(Console.ReadLine());
switch (choice)
{
case 1:
Double dollar, rupee,val; Console.WriteLine("Enter the Dollar Amount :");
dollar = Double.Parse(Console.ReadLine());
Console.WriteLine("Enter the Dollar Value :"); val = double.Parse(Console.ReadLine());
rupee = dollar * val;
Console.WriteLine("{0} Dollar Equals {1} Rupees", dollar, rupee);
break;
case 2:
Double Euro, rupe,valu; Console.WriteLine("Enter the Euro Amount :");
Euro = Double.Parse(Console.ReadLine());
Console.WriteLine("Enter the Euro Value :");
valu = double.Parse(Console.ReadLine());
rupe = Euro *valu;
Console.WriteLine("{0} Euro Equals {1} Rupees", Euro, rupe);
break;
case 3:
Double ringit, rup,value; Console.WriteLine("Enter the Ringgit Amount :");
ringit = Double.Parse(Console.ReadLine());
Console.WriteLine("Enter the Ringgit Value :");
value = double.Parse(Console.ReadLine());
rup = ringit * value;
Console.WriteLine("{0} Malaysian Ringgit Equals {1} Rupees", ringit, rup);
break;
}
Console.ReadLine();
}
}
}
Vidyalankar School of Information Technology
iii. Quadratic Equation
Code
using System;
namespace Practical2a1
{
class Quadraticroots
{
double a, b, c;
public void read()
{
Console.WriteLine(" \n To find the roots of a quadratic equation of the form a*x*x + b*x + c = 0");
Console.Write("\n Enter value for a : ");
a = double.Parse(Console.ReadLine());
Console.Write("\n Enter value for b : ");
b = double.Parse(Console.ReadLine());
Console.Write("\n Enter value for c : ");
c = double.Parse(Console.ReadLine());
Vidyalankar School of Information Technology
}
public void compute()
{
int m;
double r1, r2, d1;
d1 = b * b - 4 * a * c;
if (a == 0)
m = 1;
else if (d1 > 0)
m = 2;
else if (d1 == 0)
m = 3;
else
m = 4;
switch (m)
{
case 1: Console.WriteLine("\n Not a Quadratic equation, Linear equation");
Console.ReadLine();
break;
case 2: Console.WriteLine("\n Roots are Real and Distinct");
r1 = (-b + Math.Sqrt(d1)) / (2 * a);
r2 = (-b - Math.Sqrt(d1)) / (2 * a);
Console.WriteLine("\n First root is {0:#.##}", r1);
Console.WriteLine("\n Second root is {0:#.##}", r2);
Console.ReadLine();
break;
case 3: Console.WriteLine("\n Roots are Real and Equal");
r1 = r2 = (-b) / (2 * a);
Vidyalankar School of Information Technology
Console.WriteLine("\n First root is {0:#.##}", r1);
Console.WriteLine("\n Second root is {0:#.##}", r2);
Console.ReadLine();
break;
case 4: Console.WriteLine("\n Roots are Imaginary");
r1 = (-b) / (2 * a);
r2 = Math.Sqrt(-d1) / (2 * a);
Console.WriteLine("\n First root is {0:#.##} + i {1:#.##}", r1, r2);
Console.WriteLine("\n Second root is {0:#.##} - i {1:#.##}", r1, r2);
Console.ReadLine();
break;
}
}
}
class QuadraticEquation
{
public static void Main()
{
Quadraticroots qr = new Quadraticroots();
qr.read();
qr.compute();
}
}
}
Output
Vidyalankar School of Information Technology
iv. Temperature Conversion
Code
using System;
namespace Temperature_Conversion
{
class TempConversion
{
public static float temp;
public static char tempUnit;
static void Main(string[] args)
{
//Getting user input
Console.WriteLine("Enter Temperature in to convert it into other i.e 30 k, 45 f, 50 c *Put space between value and unit*
");
string[] tempInput = Console.ReadLine().Split();
//parse element 0
temp = float.Parse(tempInput[0]);
//assinging tempUnit
tempUnit = char.Parse(tempInput[1]);
switch (tempUnit)
{
//Converting temp to F and K if tempUnit == c
case 'c':
Console.WriteLine("Celsius To Fahrenheit and Kelvin");
Vidyalankar School of Information Technology
convertCelsiusToFahrenheit();
convertCelsiusToKelvin();
break;
//Converting temp to C and F if tempUnit == K
case 'k':
Console.WriteLine("Kelvin To Fahrenheit and Celsius");
convertKelvinToCelsius();
convertKelvinToFahrenheit();
break;
//Converting temp to C and K if tempUnit == F
case 'f':
Console.WriteLine("Fahrenheit to Celsius and kelvin");
convertFahrenheitToCelsius();
convertFahrenheitToKelvin();
break;
}
Console.ReadKey();
}
static void convertFahrenheitToCelsius()
{
Console.WriteLine((temp - 32) * 0.5556 + "C");
}
static void convertFahrenheitToKelvin()
{
Console.WriteLine((temp + 459.67) * 5 / 9 + "K");
}
static void convertCelsiusToFahrenheit()
Vidyalankar School of Information Technology
{
Console.WriteLine((temp * 1.8) + 32 + "F");
}
static void convertCelsiusToKelvin()
{
Console.WriteLine(temp + 273.15 + "K");
}
static void convertKelvinToCelsius()
{
Console.WriteLine(temp - 273.15 + "C");
}
static void convertKelvinToFahrenheit()
{
Console.WriteLine(temp - 459.67 + "F");
}
}
}
Output
b. Create simple application to demonstrate use of following concepts
i. Function Overloading ii. Inheritance (all types)
iii. Constructor overloading iv. Interfaces
i. Function Overloading
Code
using System;
namespace Practical2b1
Vidyalankar School of Information Technology
{
class shape
{
public void Area(int side)
{
int squarearea = side * side;
Console.WriteLine("The Area of Square is :" + squarearea);
}
public void Area(int length, int breadth)
{
int rectarea = length * breadth;
Console.WriteLine("The Area of Rectangle is :" + rectarea);
}
public void Area(double radius)
{
double circlearea = 3.14 * radius * radius;
Console.WriteLine("The Area of Circle is :" + circlearea);
}
}
class FunctionOverloading
{
static void Main(string[] args)
{
shape s = new shape();
s.Area(10);
s.Area(10, 20);
Vidyalankar School of Information Technology
s.Area(10.8);
Console.ReadKey();
}
}
}
Output
ii. Inheritance (all types)
(a) Single Inheritance
Code
using System;
namespace Practical2b2a
{
class Shape
{
public void setWidth(int w)
{
width = w;
}
public void setHeight(int h)
Vidyalankar School of Information Technology
{
height = h;
}
protected int width;
protected int height;
}
// Derived class
class Rectangle : Shape
{
public int getArea()
{
return (width * height);
}
}
class SingleInheritance
{
static void Main(string[] args)
{
Rectangle Rect = new Rectangle();
Rect.setWidth(5);
Rect.setHeight(7);
// Print the area of the object.
Console.WriteLine("Total area: {0}", Rect.getArea());
Console.ReadKey();
}
}
}
Vidyalankar School of Information Technology
Output
(b) Multilevel Inheritance
Code
using System;
namespace Practical2b2b
{
class Student
{
int roll_no;
string name;
public Student(int roll_no, string name)
{
this.roll_no = roll_no;
this.name = name;
}
public void display()
{
Console.WriteLine("Roll No: " + roll_no);
Console.WriteLine("Name: " + name);
}
}
class Test : Student
{
int marks1, marks2;
public Test(int roll_no, string name, int marks1, int marks2)
: base(roll_no, name)
{
this.marks1 = marks1;
this.marks2 = marks2;
}
public int getMarks1()
{
return marks1;
}
public int getMarks2()
{
return marks2;
}
public void display()
{
Vidyalankar School of Information Technology
base.display();
Console.WriteLine("Marks1: " + marks1);
Console.WriteLine("Marks2: " + marks2);
}
}
class Result : Test
{
int total;
public Result(int roll_no, string name, int marks1, int marks2)
: base(roll_no, name, marks1, marks2)
{
total = getMarks1() + getMarks2();
}
public void display()
{
base.display();
Console.WriteLine("Total: " + total);
}
}
class MultilevelInheritance
{
static void Main(string[] args)
{
Result objResult = new Result(22, "Sahil ", 98,99);
objResult.display();
Console.ReadKey();
}
}
}
iii. Constructor overloading
Code
using System;
namespace Practical2b3
{
public class StudentData
{
private int stuID;
private string stuName;
private int stuAge;
Vidyalankar School of Information Technology
public StudentData() //Default Constructor
{
stuID = 22;
stuName = "Sahil";
stuAge = 21;
}
public StudentData(int num1, string str, int num2) //Parameterized Constructor
{
stuID = num1;
stuName = str;
stuAge = num2;
}
public StudentData(StudentData s) //Copy Constructor
{
stuID = s.stuID;
stuName = s.stuName;
stuAge = s.stuAge;
}
//Getter & Setter Methods
public int getStuID()
{
return stuID;
}
public void setStuID(int stuID)
{
this.stuID = stuID;
}
public string getStuName()
{
return stuName;
}
public void setStuID(string stuName)
{
this.stuName = stuName;
}
public int getStuAge()
{
return stuAge;
}
public void setStuAge(int stuAge)
{
this.stuAge = stuAge;
}
}
class OverloadConstructor
{
static void Main(string[] args)
{
StudentData myobj = new StudentData();//call to Default Constructor
Console.WriteLine("\nConstructor 1:Default Constructor");
Console.WriteLine("Student Name:" + myobj.getStuName());
Console.WriteLine("Student Age:" + myobj.getStuAge());
Vidyalankar School of Information Technology
Console.WriteLine("Student ID:" + myobj.getStuID());
Console.WriteLine("\nConstructor 2:Parameterized Constructor");
//call to Parameterized Constructor
StudentData myobj2 = new StudentData(22, "Sahil shah", 20);
Console.WriteLine("Student Name:" + myobj2.getStuName());
Console.WriteLine("Student Age:" + myobj2.getStuAge());
Console.WriteLine("Student ID:" + myobj2.getStuID());
Console.WriteLine("\nConstructor 3:Copy Constructor");
//call to Copy Constructor
StudentData myobj3 = new StudentData(myobj2);
Console.WriteLine("Student Name:" + myobj3.getStuName());
Console.WriteLine("Student Age:" + myobj3.getStuAge());
Console.WriteLine("Student ID :" + myobj3.getStuID());
Console.ReadKey();
}
}
}
iv. Interfaces (Multiple Inheritance using Interfaces)
Code
using System;
namespace Practical2b4
{
interface calc1
Vidyalankar School of Information Technology
{
int add(int a, int b);
}
interface calc2
{
int sub(int x, int y);
}
interface calc3
{
int mul(int r, int s);
}
interface calc4
{
int div(int c, int d);
}
class Calculation : calc1, calc2, calc3, calc4
{
public int result1;
public int add(int a, int b)
{
return result1 = a + b;
}
public int result2;
public int sub(int x, int y)
{
return result2 = x - y;
}
public int result3;
Vidyalankar School of Information Technology
public int mul(int r, int s)
{
return result3 = r * s;
}
public int result4;
public int div(int c, int d)
{
return result4 = c / d;
}
}
class MultipleInheritance
{
static void Main(string[] args)
{
Calculation c = new Calculation();
c.add(8, 2);
c.sub(20, 10);
c.mul(5, 2);
c.div(20, 10);
Console.WriteLine("Multiple Inheritance concept Using Interfaces :\n ");
Console.WriteLine("Addition: " + c.result1);
Console.WriteLine("Subtraction: " + c.result2);
Console.WriteLine("Multiplication:" + c.result3);
Console.WriteLine("Division: " + c.result4);
Console.ReadKey();
}
}
Vidyalankar School of Information Technology
}
Output

c. Create simple application to demonstrate use of Delegates and events
using System;
namespace Delegate
{
public delegate void EventDelegate(string str);//delegate declaration
public class EventClass
{
public event EventDelegate Status;//declaration of Event
public void TriggerEvent()
{
if (Status != null)
{
Status("Event Triggered");
}
else
{
Console.WriteLine("Not Registered");
}
}
}
Vidyalankar School of Information Technology
class DelegateEvent
{
public static void CatchEvent(string str)//Delegate Method definition
{
Console.WriteLine(str);
}
static void Main(string[] args)
{
EventClass ec = new EventClass();
DelegateEvent et = new DelegateEvent();
ec.Status += new EventDelegate(CatchEvent);
ec.TriggerEvent();
Console.ReadLine();
}
}
}
Output
ii. Exception handling
Create user defined exception “bankexception” which will throw the exception when the
balance amount is less than 500 into the account. Then write a program to show the use of
“bank exception”.
Vidyalankar School of Information Technology
Code:
using System;
namespace Exception_handling
{
class BankException : Exception
{
public BankException(string msg)
: base(msg)
{
}
}
class BankAccount
{
public int AccountNo;
public double Balance;
public BankAccount(int AcctNo, double Balance)
{
try
{
AccountNo = AcctNo;
if (Balance < 500) throw new BankException("Oops!!!Lower Limit reached for Balance");
else
this.Balance= Balance;
}
catch (BankException e)
{
Console.WriteLine(e.Message);
}
Vidyalankar School of Information Technology
finally
{
Console.WriteLine("Account no:{0} and Balance {1}", AccountNo, Balance);
Console.ReadKey();
}
}
}
class ExceptionHandling
{
static void Main(string[] args)
{
int a;
double b;
Console.Write("Enter Account Number:");
a = int.Parse(Console.ReadLine());
Console.Write("Enter Account Balance:");
b = double.Parse(Console.ReadLine());
BankAccount obj = new BankAccount(a, b);
}
}
}
OutPut
Vidyalankar School of Information Technology
Vidyalankar School of Information Technology
Advanced Web Programming
Practical #3

Subject/Course: Advanced Web Programming
Topic Working with Web Forms and Controls
1. Working with Web Forms and Controls
a. Create a simple web page with various sever controls to demonstrate setting and use of their
properties. (Example : AutoPostBack)
Main Code:
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
namespace WebApplication1
{
 public partial class Loremum : System.Web.UI.Page
 {
 protected void Page_Load(object sender, EventArgs e)
 {
 if (!this.IsPostBack)
 {
 // Set Backcolor options in DropDownList
 lstbg.Items.Add("White");
 lstbg.Items.Add("Yellow");
 lstbg.Items.Add("Black");
 }
 }
 protected void RadioButton1_CheckedChanged(object sender, EventArgs e)
 {
 }
 protected void CheckBox1_CheckedChanged(object sender, EventArgs e)
 {
 }
Vidyalankar School of Information Technology
 protected void RadioButton3_CheckedChanged(object sender, EventArgs e)
 {
 }
 protected void Button1_Click(object sender, EventArgs e)
 {
 }
 protected void Button1_Click1(object sender, EventArgs e)
 {
 if (ChkBold.Checked == true)
 lblmsg.Font.Bold = true;
 else
 lblmsg.Font.Bold = false;
 if (ChkItalic.Checked == true)
 lblmsg.Font.Italic = true;
 else
 lblmsg.Font.Italic = false;
 if (ChkUnderline.Checked == true)
 lblmsg.Font.Underline = true;
 else
 lblmsg.Font.Underline = false;
 //update Font color
 if (RdbRed.Checked == true)
 lblmsg.ForeColor = System.Drawing.Color.Red;
 else if (RdbGreen.Checked == true)
 lblmsg.ForeColor = System.Drawing.Color.Green;
 else if (RdbBlue.Checked == true)
 lblmsg.ForeColor = System.Drawing.Color.Blue;
Vidyalankar School of Information Technology
 // Update font.
 lblmsg.Font.Name = LstFont.SelectedItem.Text;
 //Update Font Size
 if (Int32.Parse(TxtFontSize.Text) > 0)
 {
 lblmsg.Font.Size = FontUnit.Point(Int32.Parse(TxtFontSize.Text));
 }
 //Update Back Color
 lblmsg.BackColor = System.Drawing.Color.FromName(lstbg.SelectedItem.Text);
 //display Image
 if (ChkPic.Checked)
 {
 Image1.Visible = true;
 }
 else
 {
 Image1.Visible = false;
 }
 //Display Name & Message in Lable
 lblmsg.Text = TxtName.Text + " " + TxtMsg.Text;
 }
 }
 }
XML CODE:
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Loremum.aspx.cs"
Inherits="WebApplication1.Loremum" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
 <title></title>
</head>
Vidyalankar School of Information Technology
<body>
 <form id="form1" runat="server">
 <p>
 <bold>SAHIL SHAH</p>
 <p>
 Enter Your Name:
 <asp:TextBox ID="TxtName" runat="server">sahil shah</asp:TextBox>
 </p>
 <p>
 Enter ur message:
 <asp:TextBox ID="TxtMsg" runat="server" Height="45px" Width="304px"
TextMode="MultiLine">hello!!!</asp:TextBox>
 </p>
 <p>
 choose :
 <asp:CheckBox ID="ChkBold" runat="server" OnCheckedChanged="CheckBox1_CheckedChanged" Text="Bold"
/>
 <asp:CheckBox ID="ChkItalic" runat="server" Text="Italic" />
 <asp:CheckBox ID="ChkUnderline" runat="server" Text="UnderLine" />
 </p>
 <p>
 choose color:
 <asp:RadioButton ID="RdbRed" runat="server" Text="Red" />
 <asp:RadioButton ID="RdbBlue" runat="server" Text="Blue" />
 <asp:RadioButton ID="RdbGreen" runat="server" OnCheckedChanged="RadioButton3_CheckedChanged"
Text="Green" />
 </p>
 <p>
 Choose Font name:
 <asp:DropDownList ID="LstFont" runat="server" AutoPostBack="True">
 <asp:ListItem>Time sans sarif</asp:ListItem>
 <asp:ListItem>Latina san sarif</asp:ListItem>
 <asp:ListItem>Urdu</asp:ListItem>
 <asp:ListItem>Arabic</asp:ListItem>
 <asp:ListItem>Time New Roman</asp:ListItem>
 </asp:DropDownList>
 </p>
 <p>
 Font size:
 <asp:TextBox ID="TxtFontSize" runat="server">12</asp:TextBox>
 </p>
 <p>
 Select Back Color :
 <asp:DropDownList ID="lstbg" runat="server" AutoPostBack="True">
 <asp:ListItem>Black</asp:ListItem>
 <asp:ListItem>Yellow</asp:ListItem>
 <asp:ListItem>White</asp:ListItem>
 </asp:DropDownList>
 </p>
 <p>
 <asp:CheckBox ID="ChkPic" runat="server" Text="Add Default picture" />
 </p>
 <asp:Image src="qw.jpg" ID="Image1" runat="server" Height="176px" Width="177px" Visible="False" />
Vidyalankar School of Information Technology
 <p>
 <asp:Button ID="Button1" runat="server" OnClick="Button1_Click1" Text="Display" />
 </p>
 <p>
 <asp:Label ID="lblmsg" runat="server" Text="Label"></asp:Label>
 </p>
 </form>
</body>
</html>
b. Demonstrate the use of Calendar control to perform following operations.
 a) Display messages in a calendar control
 b) Display vacation in a calendar control
 c) Selected day in a calendar control using style d) Difference between two calendar dates
MAIN Function:
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
namespace WebApplication9
{
 public partial class WebForm1 : System.Web.UI.Page
 {
 protected void Page_Load(object sender, EventArgs e)
Vidyalankar School of Information Technology
 {
 }
 protected void Calendar1_SelectionChanged(object sender, EventArgs e)
 {
 Label1.Text = "Your are selected date:" + Calendar1.SelectedDate.Date.ToShortDateString();
 }
 protected void Button1_Click(object sender, EventArgs e)
 {
 Calendar1.Caption = "VSIT Academic calender";
 Calendar1.FirstDayOfWeek = FirstDayOfWeek.Monday;
 Calendar1.NextPrevFormat = NextPrevFormat.FullMonth;
 Calendar1.TitleFormat = TitleFormat.Month;
 Label2.Text = Calendar1.TodaysDate.ToShortDateString();
 Label3.Text = "Ganpati vacation start : 19-09-2023";
 TimeSpan d1 = new DateTime(2023, 09, 19) - DateTime.Now;
 Label4.Text = "Day of remainig for ganpati vacation : " + d1.Days.ToString();
 TimeSpan d2 = new DateTime(2023, 12, 31) - DateTime.Now;
 Label5.Text = "Dates remainig for NewYear : 31-12-2023" + d2.Days.ToString();

 }
 protected void Button2_Click(object sender, EventArgs e)
 {
 Label1.Text = "";
 Label2.Text = "";
 Label3.Text = "";
 Label4.Text = "";
 Label5.Text = "";
 Calendar1.SelectedDates.Clear();
 }
 protected void Calendar1_DayRender(object sender, DayRenderEventArgs e)
 {
 if (e.Day.Date.Day == 19 && e.Day.Date.Month == 9)
 {
 Calendar1.SelectedDate = new DateTime(2023, 9, 19);
 Calendar1.SelectedDates.SelectRange(Calendar1.SelectedDate, Calendar1.SelectedDate.AddDays(5));
 Label l1 = new Label();
 l1.Text = "Ganpati!!";
 e.Cell.Controls.Add(l1);
 }
 if (e.Day.Date.Day == 5 && e.Day.Date.Month == 9)
 {
 e.Cell.BackColor = System.Drawing.Color.Yellow;
 Label l2 = new Label();
 l2.Text = "Teachers days";
 e.Cell.Controls.Add(l2);
 Image img = new Image();
 img.ImageUrl = "189.jpg";
Vidyalankar School of Information Technology
 img.Width = 20;
 img.Height = 20;
 e.Cell.Controls.Add(img);
 }
 }
 }
}
XML FILE:
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="WebForm1.aspx.cs"
Inherits="WebApplication9.WebForm1" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
 <title></title>
</head>
<body>
 <form id="form1" runat="server">
 <div>
 </div>
 <asp:Calendar ID="Calendar1" runat="server" BackColor="#99FF66" BorderColor="#990000"
OnDayRender="Calendar1_DayRender" OnSelectionChanged="Calendar1_SelectionChanged">
 <TitleStyle BackColor="#339966" />
 </asp:Calendar>
 <br />
 <asp:Label ID="Label1" runat="server" Text="Label"></asp:Label>
 <br />
 <br />
 <asp:Label ID="Label2" runat="server" Text="Label"></asp:Label>
 <br />
 <br />
 <asp:Label ID="Label3" runat="server" Text="Label"></asp:Label>
 <br />
 <br />
 <asp:Label ID="Label4" runat="server" Text="Label"></asp:Label>
 <br />
 <br />
 <asp:Label ID="Label5" runat="server" Text="Label"></asp:Label>
 <br />
 <br />
&nbsp;
 <asp:Button ID="Button1" runat="server" OnClick="Button1_Click" Text="Display" />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
 <asp:Button ID="Button2" runat="server" OnClick="Button2_Click" Text="Reset" />
 <p>
 &nbsp;</p>
 </form>
Vidyalankar School of Information Technology
</body>
</html>
Sample o/p:
Output:

Vidyalankar School of Information Technology
c. Demonstrate the use of Treeview control perform following operations.
 a) Treeview control and datalist b) Treeview operations
Main Function:
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
namespace WebApplication10
{
 public partial class WebForm1 : System.Web.UI.Page
 {
 protected void Page_Load(object sender, EventArgs e)
 {
 }
 protected void TreeView1_SelectedNodeChanged(object sender, EventArgs e)
 {
 Response.Write("You are selected" + TreeView1.SelectedValue);
 }
 protected void TreeView1_TreeNodeCollapsed(object sender, TreeNodeEventArgs e)
 {
 Response.Write("The value collapsed is" + e.Node.Value);
 }
 protected void Button1_Click(object sender, EventArgs e)
 {
 TreeNodeCollection t1;
 t1 = TreeView1.CheckedNodes;
 DataList1.DataSource = t1;
 DataList1.DataBind();
 DataList1.Visible = true;
 }
 }
}
Xml File:
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="WebForm1.aspx.cs"
Inherits="WebApplication10.WebForm1" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
 <title></title>
</head>
<body>
Vidyalankar School of Information Technology
 <form id="form1" runat="server">
 <div>
 </div>
 <asp:TreeView ID="TreeView1" runat="server" OnSelectedNodeChanged="TreeView1_SelectedNodeChanged"
OnTreeNodeCollapsed="TreeView1_TreeNodeCollapsed" Width="214px">
 <Nodes>
 <asp:TreeNode ShowCheckBox="True" Text="BSC IT" Value="BSC IT">
 <asp:TreeNode Text="FY" Value="FY"></asp:TreeNode>
 <asp:TreeNode Text="SY" Value="SY"></asp:TreeNode>
 <asp:TreeNode Text="TY" Value="TY"></asp:TreeNode>
 </asp:TreeNode>
 <asp:TreeNode ShowCheckBox="True" Text="BMS" Value="BMS">
 <asp:TreeNode Text="FY" Value="FY"></asp:TreeNode>
 <asp:TreeNode Text="SY" Value="SY"></asp:TreeNode>
 <asp:TreeNode Text="TY" Value="TY"></asp:TreeNode>
 </asp:TreeNode>
 </Nodes>
 </asp:TreeView>
 <p>
 <asp:Button ID="Button1" runat="server" Height="53px" OnClick="Button1_Click" Text="Button"
Width="243px" />
 </p>
 <asp:DataList ID="DataList1" runat="server">
 <ItemTemplate><%#Eval("text") %></ItemTemplate>
 </asp:DataList>
 <asp:DataList ID="DataList2" runat="server">
 </asp:DataList>
 </form>
</body>
</html>
Sample o/p:
Vidyalankar School of Information Technology
Vidyalankar School of Information Technology
Vidyalankar School of Information Technology
Advanced Web Programming
Practical #4
1122
Subject/Course: Advanced Web Programming
Topic Working with Web Forms and Controls
Working with Form Controls
a. Create a Registration form to demonstrate use of various Validation controls.
WebForm1.aspx
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="WebForm1.aspx.cs"
Inherits="Validation.WebForm1" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
 <title></title>
</head>
<body>
 <form id="form1" runat="server">
 <div>
 <asp:Label ID="Label1" runat="server" Style="font-weight: 700"
Text="Name:"></asp:Label>&nbsp;&nbsp;
 <asp:TextBox ID="TextName" runat="server"></asp:TextBox>
 &nbsp;<asp:RequiredFieldValidator ID="RequiredFieldValidator1"
runat="server" ControlToValidate="TextName" ErrorMessage="*Enter your name"
ForeColor="Red"></asp:RequiredFieldValidator>
 <br />
 <asp:Label ID="Label2" runat="server" Style="font-weight: 700"
Text="Password:"></asp:Label>&nbsp;&nbsp;
 <asp:TextBox ID="TextPassword" runat="server"></asp:TextBox>
 &nbsp;<asp:RequiredFieldValidator ID="RequiredFieldValidator2"
runat="server" ControlToValidate="TextPassword" ErrorMessage="*Enter your
password" ForeColor="Red"></asp:RequiredFieldValidator>
 <br />
 <asp:Label ID="Label3" runat="server" Style="font-weight: 700"
Text="Confirm Password:"></asp:Label>&nbsp;&nbsp;
 <asp:TextBox ID="TextConfirmPassword" runat="server"></asp:TextBox>
 &nbsp;<asp:CompareValidator ID="CompareValidator1" runat="server"
ControlToCompare="TextPassword" ControlToValidate="TextConfirmPassword"
ErrorMessage="*Enter same password here too"
ForeColor="Red"></asp:CompareValidator>
Vidyalankar School of Information Technology
 <br />
 <asp:Label ID="Label4" runat="server" Style="font-weight: 700"
Text="Email ID:"></asp:Label>&nbsp;&nbsp;
 <asp:TextBox ID="TextEmail" runat="server"></asp:TextBox>
 &nbsp;<asp:RegularExpressionValidator
ID="RegularExpressionValidator1" runat="server" ControlToValidate="TextEmail"
ErrorMessage="*Enter vaild Email ID" ForeColor="Red" ValidationExpression="\w+([-
+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*"></asp:RegularExpressionValidator>
 <br />

 <asp:Label ID="Label5" runat="server" Style="font-weight: 700"
Text="Age:"></asp:Label>&nbsp;&nbsp;
 <asp:TextBox ID="TextAge" runat="server"></asp:TextBox>
 &nbsp;<asp:RangeValidator ID="RangeValidator" runat="server"
ControlToValidate="TextAge" ErrorMessage="*Enter Age between 18 - 100"
ForeColor="Red" MaximumValue="18" MinimumValue="100"></asp:RangeValidator>
 <br />

 <asp:Label ID="Label6" runat="server" Style="font-weight: 700"
Text="User ID:"></asp:Label>&nbsp;&nbsp;
 <asp:TextBox ID="TextUserID" runat="server"></asp:TextBox>
 &nbsp;<asp:CustomValidator ID="CustomValidator1" runat="server"
ErrorMessage="*Enter atleast single capital, lower case letter &amp; a digit"
ForeColor="Red" OnServerValidate="CustomValidator1_ServerValidate"
ControlToValidate="TextUserID"></asp:CustomValidator>
 <br />

 <br />
 <asp:Label ID="Label7" runat="server" Style="font-weight: 700"
Text="Validation summary"></asp:Label>
 <asp:ValidationSummary ID="ValidationSummary1" runat="server" />
 <asp:Button ID="Btn1" runat="server" OnClick="Btn1_Click" Text="VALID"
/>
 &nbsp;&nbsp;&nbsp;
 <asp:Button ID="Btn2" runat="server" OnClick="Btn2_Click"
Text="CANCEL" />
 <br />
 <br />
 <asp:Label ID="LabelMsg" runat="server" Text="[Label]"></asp:Label>
 </div>
 </form>
</body>
</html>
WebForm1.aspx.cs
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
Vidyalankar School of Information Technology
using System.Web.UI;
using System.Web.UI.WebControls;
namespace Validation {
 public partial class WebForm1 : System.Web.UI.Page {
 protected void Page_Load(object sender, EventArgs e) {
 }
 protected void Btn1_Click(object sender, EventArgs e) {
 if (Page.IsValid) {
 LabelMsg.Text = "This is a valid form.";
 }
 }
 protected void Btn2_Click(object sender, EventArgs e) {
 LabelMsg.Text = "No attempt was made to validate this form.";
 }
 protected void CustomValidator1_ServerValidate(object source,
ServerValidateEventArgs args) {
 string str = args.Value;
 args.IsValid = false;
 if (str.Length < 6 || str.Length > 25) {
 return;
 }
 bool capital = false;
 foreach (char ch in str) {
 if (ch >= 'A' && ch <= 'Z') {
 capital = true;
break;
 }
 }
 if (capital) {
 return;
 }
 bool lower = false;
 foreach (char ch in str) {
 if (ch >= 'a' && ch <= 'z') {
 lower = true;
break;
 }
 }
 if (!lower) {
 return;
 }
Vidyalankar School of Information Technology
 bool digit = false;
 foreach (char ch in str) {
 if (ch >= '0' && ch <= '9') {
 digit = true;
 break;
 }
 }
 if (!digit) {
 return;
 }
 args.IsValid = true;
 }
 }
}
Output
b. Create Web Form to demonstrate use of Adrotator Control
-------------XML---------------
<?xml version="1.0" encoding="utf-8" ?>
<Advertisements>
<Ad>
<ImageUrl>luffy.jpg</ImageUrl>
<NavigateUrl>https://vsit.edu.in/</NavigateUrl>
<AlternateText>Image1</AlternateText>
<Impressions>4</Impressions>
<Keyword>data</Keyword>
</Ad>
<Ad>
Vidyalankar School of Information Technology
<ImageUrl>luffy2.jpg</ImageUrl>
<NavigateUrl>https://vsit.edu.in/</NavigateUrl>
<AlternateText>Image2</AlternateText>
<Impressions>5</Impressions>
<Keyword>data</Keyword>
</Ad>
<Ad>
<ImageUrl>luffy3.jpg</ImageUrl>
<NavigateUrl>https://vsit.edu.in/</NavigateUrl>
<AlternateText>Image4</AlternateText>
<Impressions>4</Impressions>
<Keyword>data</Keyword>
</Ad>
<Ad>
<ImageUrl>luffy4.jpg</ImageUrl>
<NavigateUrl>https://vsit.edu.in/</NavigateUrl>
<AlternateText>Image4</AlternateText>
<Impressions>4</Impressions>
<Keyword>data</Keyword>
</Ad>
</Advertisements>
-----------WEBFORM----------------
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="WebForm1.aspx.cs"
Inherits="WebApplication4.WebForm1" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
<title></title>
</head>
<body>
<form id="form1" runat="server">
<div>
</div>
<asp:AdRotator ID="AdRotator1" runat="server" AdvertisementFile="~/XMLFile1.xml" />
</form>
</body>
</html>
Vidyalankar School of Information Technology

c. Create Web Form to demonstrate use User Controls.
Web user control ascx
<%@ Control Language="C#" AutoEventWireup="true" CodeBehind="WebUserControl1.ascx.cs"
Inherits="WebApplication3.WebUserControl1" %>
<p>
 This is User Control</p>
<p>
<asp:Label ID="Label1" runat="server" Text="Name"></asp:Label>
<asp:TextBox ID="TextBoxName" runat="server"></asp:TextBox>
</p>
<p>
<asp:Label ID="Label2" runat="server" Text="City"></asp:Label>
<asp:TextBox ID="TextBoxCity" runat="server"></asp:TextBox>
</p>
<p>
<asp:Button ID="Button1" runat="server" OnClick="Button1_Click" Text="Save" />
Vidyalankar School of Information Technology
</p>
<asp:Label ID="Label3" runat="server" Text="Label"></asp:Label>
Web user control ascx.cs
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace WebApplication3
{
 public partial class WebUserControl1 : System.Web.UI.UserControl
 {
 protected void Page_Load(object sender, EventArgs e)
 {

 }

 protected void Button1_Click(object sender, EventArgs e)
 {
 Label3.Text = "Name :" + TextBoxName.Text + ",City: " + TextBoxCity.Text;
 }
 }
}
Using user control aspx
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="WebForm1.aspx.cs"
Inherits="WebApplication3.WebForm1" %>
<<%@ Register Src="~/WebUserControl1.ascx" TagName="MyControl" TagPrefix="MyUser" %>
<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
<title></title>
</head>
<body>
<form id="form1" runat="server">
<div>
<MyUser:MyControl ID="user1" runat="server" />
</div>
</form>
</body>
</html>
Output
Vidyalankar School of Information Technology
Vidyalankar School of Information Technology
Advanced Web Programming
Practical #5
1122
Subject/Course: Advanced Web Programming
Topic Working with Navigation, Beautification and Master page.
5. Working with Navigation, Beautification and Master page.
a) Create Web Form to demonstrate use of Website Navigation controls and Site Map.
--> Home page
 <%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Home.aspx.cs"
Inherits="WebApplication14.Home" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
 <title></title>
</head>
<body>
 <form id="form1" runat="server">
 <div>
 Home Page</div>
 <asp:Menu ID="Menu1" runat="server">
 </asp:Menu>
 <asp:TreeView ID="TreeView1" runat="server" DataSourceID="SiteMapDataSource1">
 </asp:TreeView>
 <asp:SiteMapDataSource ID="SiteMapDataSource1" runat="server" />
 </form>
</body>
</html>
--> Order Page
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="order.aspx.cs"
Inherits="WebApplication14.order" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
 <title></title>
</head>
<body>
 <form id="form1" runat="server">
 <div>
 </div>
Vidyalankar School of Information Technology
 </form>
</body>
</html>
--> Product Page
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="product.aspx.cs"
Inherits="WebApplication14.product" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
 <title></title>
</head>
<body>
 <form id="form1" runat="server">
 <div>
 This is product page</div>
 <asp:SiteMapPath ID="SiteMapPath1" runat="server">
 </asp:SiteMapPath>
 </form>
</body>
</html>
--> Cart Page
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="cart.aspx.cs" Inherits="WebApplication14.cart"
%>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
 <title></title>
</head>
<body>
 <form id="form1" runat="server">
 <div>
 this is cart page</div>
 <asp:SiteMapPath ID="SiteMapPath1" runat="server">
 </asp:SiteMapPath>
 </form>
</body>
</html>
Vidyalankar School of Information Technology
b) Create a web application to demonstrate use of Master Page with applying Styles and Themes for page
beautification.
----Content Page-------
<%@ Page Title="" Language="C#" MasterPageFile="~/masterpage.Master" AutoEventWireup="true"
CodeBehind="contentpage.aspx.cs" Inherits="WebApplication15.contentpage" Theme="Skin1"%>
<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="server">
</asp:Content>
<asp:Content ID="Content2" ContentPlaceHolderID="ContentPlaceHolder1" runat="server">
 <asp:Label ID="Label1" runat="server" Text="Label"></asp:Label>
 <br />
 <asp:Label ID="Label2" runat="server" Text="SPM"></asp:Label>
 <br />
 <asp:Label ID="Label3" runat="server" Text="IOT"></asp:Label>
 <br />
 <asp:Label ID="Label4" runat="server" Text="AI" SkinID="LabelSkin"></asp:Label>
 <br />
 <asp:Label ID="Label5" runat="server" Text="AWP"></asp:Label>
 <br />
 <br />
 <asp:Button ID="Button1" runat="server" Text="show" />
</asp:Content>
----------Master Page----------
<%@ Master Language="C#" AutoEventWireup="true" CodeBehind="masterpage.Master.cs"
Inherits="WebApplication15.Site1" %>
<!DOCTYPE html>
Vidyalankar School of Information Technology
<html>
<head runat="server">
 <title></title>
 <asp:ContentPlaceHolder ID="head" runat="server">
 </asp:ContentPlaceHolder>
 <link href="StyleSheet1.css" rel="stylesheet" type="text/css" />
</head>
<body>
 <form id="form1" runat="server">
 <div>
 <h1>This is a master page!</h1>
 <asp:ContentPlaceHolder ID="ContentPlaceHolder1" runat="server">
 </asp:ContentPlaceHolder>
 </div>
 </form>
</body>
</html>
--------CSS-----------
body {
 border-style: dashed;
 background-color: cornflowerblue;
 font-family:Cambria, Cochin, Georgia, Times, Times New Roman, serif;
 font-size: 23px;
}
-----------SKIN---------------
<asp:Label runat="server" ForeColor="red" FontSize="14pt" Font-Names="Verdana" SkinID="LabelSkin" />
<asp:Label runat="server" ForeColor="Blue" FontSize="25pt" Font-Names="Verdana"/>
<asp:button runat="server" Borderstyle="solid" BorderWidth="2px" Bordercolor="Blue" Backcolor="blue"/>
c) Create a web application to demonstrate various states of ASP.NET Pages.
Vidyalankar School of Information Technology
Webform
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="WebForm1.aspx.cs"
Inherits="WebApplication11.WebForm1" Trace="true" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
<title></title>
</head>
<body>
<form id="form1" runat="server">
<div>
<asp:Label ID="Label1" runat="server" Text="User Name : "></asp:Label>
<asp:TextBox ID="TextBox1" runat="server"></asp:TextBox>
<asp:Label ID="Label3" runat="server" Text="Labelname"></asp:Label>
<br />
<br />
<br />
<asp:Label ID="Label2" runat="server" Text="User ID : "></asp:Label>
&nbsp;
<asp:TextBox ID="TextBox2" runat="server"></asp:TextBox>
<asp:Label ID="Label4" runat="server" Text="LabelID"></asp:Label>
</div>
<asp:Button ID="Button1" runat="server" OnClick="Button1_Click" Text="Get View state Data" />
<br />
<br />
<asp:Button ID="Button2" runat="server" Text="Query string Send value" OnClick="Button2_Click" />
<br />
<br />
<asp:Button ID="Button3" runat="server" Text="Create Cookie and Send Value" OnClick="Button3_Click" />
<br />
<br />
<asp:Button ID="Button4" runat="server" Text="Save in Session" OnClick="Button4_Click" />
<br />
<br />
<asp:Button ID="Button5" runat="server" OnClick="Button5_Click" Text="Application state:Visitor count" />
<asp:Label ID="Label5" runat="server" Text="LabelCount"></asp:Label>
</form>
</body>
</html>
Vidyalankar School of Information Technology
Webform1promain
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
namespace WebApplication11
{
 public partial class WebForm1 : System.Web.UI.Page
 {
 protected void Page_Load(object sender, EventArgs e)
 {
 }
 protected void Button5_Click(object sender, EventArgs e)
 {
 Label5.Text = Application["CountUser"].ToString();
 }
 protected void Button1_Click(object sender, EventArgs e)
 {
 ViewState["name"] = TextBox1.Text;
 Label3.Text = ViewState["name"].ToString();
 ViewState["ID"] = TextBox2.Text;
 Label4.Text = ViewState["ID"].ToString();
 }
 protected void Button2_Click(object sender, EventArgs e)
 {
 Response.Redirect("ReadQueryString.aspx?name=" + TextBox1.Text + "&ID=" + TextBox2.Text);
 }
 protected void Button4_Click(object sender, EventArgs e)
 {
 Session["Name"] = TextBox1.Text;
Vidyalankar School of Information Technology
 Session["ID"] = TextBox2.Text;
 Response.Redirect("ReadFromSession.aspx");
 }
 protected void Button3_Click(object sender, EventArgs e)
 {
 HttpCookie ck = new HttpCookie("ck");
 ck.Values.Add("Name", TextBox1.Text);
 ck.Values.Add("ID", TextBox2.Text);
 Response.Cookies.Add(ck);
 Response.Redirect("Cookies2.aspx");
 }
 }
}
ReadQuery
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
namespace WebApplication11
{
 public partial class ReadQueryString : System.Web.UI.Page
 {
 protected void Page_Load(object sender, EventArgs e)
 {
 }
 protected void Button1_Click(object sender, EventArgs e)
 {
 TextBox1.Text = Request.QueryString["name"].ToString();
 TextBox2.Text = Request.QueryString["ID"].ToString();
 }
 }
}
ReadFromsession
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
Vidyalankar School of Information Technology
using System.Web.UI;
using System.Web.UI.WebControls;
namespace WebApplication11
{
 public partial class ReadFromSession : System.Web.UI.Page
 {
 protected void Page_Load(object sender, EventArgs e)
 {
 }
 protected void Button1_Click(object sender, EventArgs e)
 {
 TextBox1.Text=Session["Name"].ToString();
 TextBox2.Text=Session["ID"].ToString();
 }
 }
}
readfromsessionmain
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
namespace WebApplication11
{
 public partial class ReadFromSession : System.Web.UI.Page
 {
 protected void Page_Load(object sender, EventArgs e)
 {
 }
 protected void Button1_Click(object sender, EventArgs e)
 {
 TextBox1.Text=Session["Name"].ToString();
 TextBox2.Text=Session["ID"].ToString();
 }
 }
}
ReadQueryMain
Vidyalankar School of Information Technology
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
namespace WebApplication11
{
 public partial class ReadQueryString : System.Web.UI.Page
 {
 protected void Page_Load(object sender, EventArgs e)
 {
 }
 protected void Button1_Click(object sender, EventArgs e)
 {
 TextBox1.Text = Request.QueryString["name"].ToString();
 TextBox2.Text = Request.QueryString["ID"].ToString();
 }
 }
}
Vidyalankar School of Information Technology
Vidyalankar School of Information Technology
Advanced Web Programming
Practical #6
1122
Subject/Course: Advanced Web Programming
Topic Working with Database
6. Working with Database
a) Create a web application bind data in a multiline textbox by querying in another textbox.
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Data.SqlClient;
using System.Data;
namespace WebApplication23
{
 public partial class WebForm3 : System.Web.UI.Page
 {
 protected void Page_Load(object sender, EventArgs e)
 {
 }
 protected void Button1_Click(object sender, EventArgs e)
 {
 SqlConnection con = new SqlConnection(@"Data
Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=C:\Users\exam\source\repos\WebApplication23\WebApplication
23\App_Data\Database1.mdf;Integrated Security=True");
 con.Open();
Vidyalankar School of Information Technology
 SqlCommand cmd = new SqlCommand(TextBox1.Text, con);
 SqlDataReader reader = cmd.ExecuteReader();
 TextBox2.Text = "";
 while (reader.Read())
 {
 TextBox2.Text += Environment.NewLine;
 for (int i = 0; i < reader.FieldCount - 1; i++)
 {
 TextBox2.Text += reader[i].ToString().PadLeft(15);
 }
 }
 reader.Close();
 con.Close();
 }
 }
}
b) Create a web application to display records in Label by using database.
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Data.SqlClient;
using System.Data;
namespace WebApplication23
{
 public partial class web22 : System.Web.UI.Page
 {
 protected void Page_Load(object sender, EventArgs e)
 {
 }
Vidyalankar School of Information Technology
 protected void Button1_Click(object sender, EventArgs e)
 {
 SqlConnection con = new SqlConnection(@"Data
Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=C:\Users\exam\source\repos\WebApplication23\WebApplication
23\App_Data\Database1.mdf;Integrated Security=True");
 SqlCommand cmd = new SqlCommand("Select Id,Name,Address from Customer", con);
 con.Open();
 SqlDataReader reader = cmd.ExecuteReader();
 while(reader.Read())
 {
 Label1.Text+=reader["Id"].ToString()+""+reader["Name"].ToString() + " " + reader["Address"].ToString() +
"<br>";
 }
 reader.Close();
 con.Close();
 }
 }
}
c) Demonstrate the use of Datalist control.
Vidyalankar School of Information Technology
Vidyalankar School of Information Technology
Advanced Web Programming
Practical #7
1122
Subject/Course: Advanced Web Programming
Topic Working with Database
8. Working with Database
a) Create a web application to display Databinding using dropdownlist control.
Code :
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="7a.aspx.cs" Inherits="AWP_Practical_7._7a" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
 <title></title>
</head>
<body>
 <form id="form1" runat="server">
 <div>
 <asp:DropDownList ID="DropDownList1" runat="server" DataSourceID="SqlDataSource1" DataTextField="A_Name"
DataValueField="A_Name"></asp:DropDownList>
 <br />
 <br />
 <asp:SqlDataSource ID="SqlDataSource1" runat="server" ConnectionString="<%$ ConnectionStrings:ConnectionString %>"
ProviderName="<%$ ConnectionStrings:ConnectionString.ProviderName %>" SelectCommand="SELECT [A_Name] FROM
[Author]"></asp:SqlDataSource>
 </div>
 </form>
</body>
</html>
Vidyalankar School of Information Technology
b) Create a web application for to display the phone no of an author using database
Code:
7b.aspx
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="7a.aspx.cs" Inherits="AWP_Practical_7._7a" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
 <title></title>
</head>
<body>
 <form id="form1" runat="server">
 <div>
 <h1><u> Author Details </u></h1>
 <hr />
 <br />
Vidyalankar School of Information Technology
 Enter Author Name :&nbsp;&nbsp;
 <asp:TextBox ID="TB1" runat="server" Width="186px"></asp:TextBox>
 <br />
 <br />
 <asp:Button ID="B1" runat="server" Text="Submit" Width="155px" OnClick="B1_Click" />
 <br />
 <br />
 <asp:Label ID="LB1" runat="server" Text="Label"></asp:Label>
 <br />
 <asp:Label ID="LB2" runat="server" Text="Label"></asp:Label>
 <br />

 </div>
 </form>
</body>
</html>
7b.aspx.cs
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Data;
using System.Data.SqlClient;
namespace AWP_Practical_7
{
Vidyalankar School of Information Technology
 public partial class _7a : System.Web.UI.Page
 {
 protected void Page_Load(object sender, EventArgs e)
 {
 }
 protected void B1_Click(object sender, EventArgs e)
 {
 string name = TB1.Text;
 SqlConnection con = new SqlConnection(@"Data
Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=E:\AWP\AWP_Practical_7\AWP_Practical_7\App_Data\Author_DB.mdf;Integrate
d Security=True");
 con.Open();
 SqlCommand cmd = new SqlCommand("SELECT A_Phone from Author where A_Name='"+name+"' ", con);
 SqlDataReader rd = cmd.ExecuteReader();

 if (rd.Read())
 {
 LB1.Text = name;
 LB2.Text =rd["A_Phone"].ToString();
 }
 con.Close();
 }
 }
}
OUTPUT:
Vidyalankar School of Information Technology
c) Create a web application for inserting and deleting record from a database. (Using Execute-NonQuery).
CODE:
7C.aspx
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="7C.aspx.cs" Inherits="AWP_Practical_7._7C" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
 <title></title>
 <style type="text/css">
 .auto-style1 {
 width: 100%;
 }
 .auto-style2 {
Vidyalankar School of Information Technology
 height: 23px;
 }
 .auto-style3 {
 height: 23px;
 width: 252px;
 }
 .auto-style4 {
 width: 252px;
 }
 </style>
</head>
<body>
 <form id="form1" runat="server">
 <div>
 <h1><u>Author Record Management</u></h1>
 <hr />
 <br />
 <table class="auto-style1">
 <tr>
 <td class="auto-style3">Enter ID</td>
 <td class="auto-style2">
 <asp:TextBox ID="TB1" runat="server"></asp:TextBox>
 </td>
 </tr>
 <tr>
 <td class="auto-style4">Enter Name</td>
 <td>
 <asp:TextBox ID="TB2" runat="server"></asp:TextBox>
 </td>
 </tr>
 <tr>
Vidyalankar School of Information Technology
 <td class="auto-style4">Enter Phone Number</td>
 <td>
 <asp:TextBox ID="TB3" runat="server"></asp:TextBox>
 </td>
 </tr>
 </table>
 <br />
 Actions :<br />
 <br />
 <asp:Button ID="B1" runat="server" Text="Insert" Width="119px" OnClick="B1_Click" />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
 <asp:Button ID="B2" runat="server" Text="Delete" Width="119px" OnClick="B2_Click" />
 <br />
 <br />
 Status Monitor :<br />
 <br />
 <asp:Label ID="LB1" runat="server" Text="Label"></asp:Label>
 <br />
 </div>
 </form>
</body>
</html>
7c.aspx.cs
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
Vidyalankar School of Information Technology
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Data;
using System.Data.SqlClient;
namespace AWP_Practical_7
{
 public partial class _7C : System.Web.UI.Page
 {
 protected void Page_Load(object sender, EventArgs e)
 {
 }
 protected void B1_Click(object sender, EventArgs e)
 {
 if(TB1.Text!= null && TB2.Text!= null && TB3.Text != null)
 {
 int id = Convert.ToInt32(TB1.Text);
 string name = TB2.Text;
 string phone = TB3.Text;
 SqlConnection con = new SqlConnection(@"Data
Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=E:\AWP\AWP_Practical_7\AWP_Practical_7\App_Data\Author
_DB.mdf;Integrated Security=True");
 con.Open();
Vidyalankar School of Information Technology
 SqlCommand cmd = new SqlCommand("INSERT into Author values('" + id + "','" + name + "','" + phone + "')",
con);
 int i = cmd.ExecuteNonQuery();
 if (i > 0)
 {
 LB1.Text = "Record Added Sucessfully";
 }
 con.Close();
 }
 else
 {
 LB1.Text = "Enter All fields";
 }
 }
 protected void B2_Click(object sender, EventArgs e)
 {
 if(TB1.Text != null)
 {
 int id = Convert.ToInt32(TB1.Text);
 SqlConnection con = new SqlConnection(@"Data
Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=E:\AWP\AWP_Practical_7\AWP_Practical_7\App_Data\Author
_DB.mdf;Integrated Security=True");
 con.Open();
 SqlCommand cmd = new SqlCommand("DELETE from Author where Id='"+id+"' ",con);
 int i = cmd.ExecuteNonQuery();
 if(i > 0)
 {
Vidyalankar School of Information Technology
 LB1.Text = "Record Deleted Sucessfully!";
 }
 }
 }
 }
}
Output:
Insert Query
Vidyalankar School of Information Technology
Vidyalankar School of Information Technology
Advanced Web Programming
Practical #8
Name Sahil
Shah
Roll
Number 21302C0022
Subject/Course: Advanced Web Programming
Topic Working with Data Controls
8. Working with Data Controls
a) Create a web application to demonstrate various uses and properties of SqlDataSource and data binding using
Drop Down List, GridView, DetailsView, and FormView Control.
Code:
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="WebForm1.aspx.cs" Inherits="practical8a.WebForm1"
%>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
<title></title>
</head>
<body>
<form id="form1" runat="server">
<div>
<asp:DropDownList ID="DropDownList1" runat="server" AutoPostBack="True" DataSourceID="SqlDataSource1"
DataTextField="name" DataValueField="name">
</asp:DropDownList>
<asp:SqlDataSource ID="SqlDataSource1" runat="server" ConnectionString="Data
Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=|DataDirectory|\Database1.mdf;Integrated Security=True"
DeleteCommand="DELETE FROM [Student] WHERE [Id] = @Id" InsertCommand="INSERT INTO [Student] ([Id], [name],
[city], [gender]) VALUES (@Id, @name, @city, @gender)" ProviderName="System.Data.SqlClient"
SelectCommand="SELECT * FROM [Student]" UpdateCommand="UPDATE [Student] SET [name] = @name, [city] = @city,
[gender] = @gender WHERE [Id] = @Id">
<DeleteParameters>
<asp:Parameter Name="Id" Type="Int32" />
</DeleteParameters>
<InsertParameters>
<asp:Parameter Name="Id" Type="Int32" />
<asp:Parameter Name="name" Type="String" />
<asp:Parameter Name="city" Type="String" />
<asp:Parameter Name="gender" Type="String" />
</InsertParameters>
<UpdateParameters>
<asp:Parameter Name="name" Type="String" />
<asp:Parameter Name="city" Type="String" />
<asp:Parameter Name="gender" Type="String" />
Vidyalankar School of Information Technology
<asp:Parameter Name="Id" Type="Int32" />
</UpdateParameters>
</asp:SqlDataSource>
<br />
<asp:GridView ID="GridView1" runat="server" AllowPaging="True" AllowSorting="True" AutoGenerateColumns="False"
BackColor="White" BorderColor="#3366CC" BorderStyle="None" BorderWidth="1px" CellPadding="4"
DataKeyNames="Id" DataSourceID="SqlDataSource1">
<Columns>
<asp:CommandField ShowDeleteButton="True" ShowEditButton="True" ShowSelectButton="True" />
<asp:BoundField DataField="Id" HeaderText="Student ID" ReadOnly="True" SortExpression="Id" />
<asp:BoundField DataField="name" HeaderText="Student Name" SortExpression="name" />
<asp:BoundField DataField="city" HeaderText="City" SortExpression="city" />
<asp:BoundField DataField="gender" HeaderText="Gender" SortExpression="gender" />
</Columns>
<FooterStyle BackColor="#99CCCC" ForeColor="#003399" />
<HeaderStyle BackColor="#003399" Font-Bold="True" ForeColor="#CCCCFF" />
<PagerStyle BackColor="#99CCCC" ForeColor="#003399" HorizontalAlign="Left" />
<RowStyle BackColor="White" ForeColor="#003399" />
<SelectedRowStyle BackColor="#009999" Font-Bold="True" ForeColor="#CCFF99" />
<SortedAscendingCellStyle BackColor="#EDF6F6" />
<SortedAscendingHeaderStyle BackColor="#0D4AC4" />
<SortedDescendingCellStyle BackColor="#D6DFDF" />
<SortedDescendingHeaderStyle BackColor="#002876" />
</asp:GridView>
<asp:SqlDataSource ID="SqlDataSource2" runat="server" ConnectionString="Data
Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=|DataDirectory|\Database1.mdf;Integrated Security=True"
DeleteCommand="DELETE FROM [Student] WHERE [Id] = @Id" InsertCommand="INSERT INTO [Student] ([Id], [name],
[city], [gender]) VALUES (@Id, @name, @city, @gender)" ProviderName="System.Data.SqlClient"
SelectCommand="SELECT * FROM [Student]" UpdateCommand="UPDATE [Student] SET [name] = @name, [city] = @city,
[gender] = @gender WHERE [Id] = @Id">
<DeleteParameters>
<asp:Parameter Name="Id" Type="Int32" />
</DeleteParameters>
<InsertParameters>
<asp:Parameter Name="Id" Type="Int32" />
<asp:Parameter Name="name" Type="String" />
<asp:Parameter Name="city" Type="String" />
<asp:Parameter Name="gender" Type="String" />
</InsertParameters>
<UpdateParameters>
<asp:Parameter Name="name" Type="String" />
<asp:Parameter Name="city" Type="String" />
<asp:Parameter Name="gender" Type="String" />
<asp:Parameter Name="Id" Type="Int32" />
</UpdateParameters>
</asp:SqlDataSource>
<br />
<br />
<asp:DetailsView ID="DetailsView1" runat="server" AllowPaging="True" AutoGenerateRows="False" CellPadding="4"
DataKeyNames="Id" DataSourceID="SqlDataSource1" ForeColor="#333333" GridLines="None" Height="50px"
OnPageIndexChanging="DetailsView1_PageIndexChanging" Width="125px">
<AlternatingRowStyle BackColor="White" ForeColor="#284775" />
<CommandRowStyle BackColor="#E2DED6" Font-Bold="True" />
Vidyalankar School of Information Technology
<EditRowStyle BackColor="#999999" />
<FieldHeaderStyle BackColor="#E9ECF1" Font-Bold="True" />
<Fields>
<asp:BoundField DataField="Id" HeaderText="Id" ReadOnly="True" SortExpression="Id" />
<asp:BoundField DataField="name" HeaderText="name" SortExpression="name" />
<asp:BoundField DataField="city" HeaderText="city" SortExpression="city" />
<asp:BoundField DataField="gender" HeaderText="gender" SortExpression="gender" />
<asp:CommandField ShowDeleteButton="True" ShowEditButton="True" ShowInsertButton="True" />
</Fields>
<FooterStyle BackColor="#5D7B9D" Font-Bold="True" ForeColor="White" />
<HeaderStyle BackColor="#5D7B9D" Font-Bold="True" ForeColor="White" />
<PagerStyle BackColor="#284775" ForeColor="White" HorizontalAlign="Center" />
<RowStyle BackColor="#F7F6F3" ForeColor="#333333" />
</asp:DetailsView>
<asp:SqlDataSource ID="SqlDataSource3" runat="server" ConnectionString="Data
Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename=|DataDirectory|\Database1.mdf;Integrated Security=True"
ProviderName="System.Data.SqlClient" SelectCommand="SELECT * FROM [Student]"></asp:SqlDataSource>
<br />
<asp:FormView ID="FormView1" runat="server" AllowPaging="True" CellPadding="4" DataKeyNames="Id"
DataSourceID="SqlDataSource1" ForeColor="#333333">
<EditItemTemplate>
 Id:
<asp:Label ID="IdLabel1" runat="server" Text='<%# Eval("Id") %>' />
<br />
 name:
<asp:TextBox ID="nameTextBox" runat="server" Text='<%# Bind("name") %>' />
<br />
 city:
<asp:TextBox ID="cityTextBox" runat="server" Text='<%# Bind("city") %>' />
<br />
 gender:
<asp:TextBox ID="genderTextBox" runat="server" Text='<%# Bind("gender") %>' />
<br />
<asp:LinkButton ID="UpdateButton" runat="server" CausesValidation="True" CommandName="Update" Text="Update"
/>
&nbsp;<asp:LinkButton ID="UpdateCancelButton" runat="server" CausesValidation="False" CommandName="Cancel"
Text="Cancel" />
</EditItemTemplate>
<EditRowStyle BackColor="#2461BF" />
<FooterStyle BackColor="#507CD1" Font-Bold="True" ForeColor="White" />
<HeaderStyle BackColor="#507CD1" Font-Bold="True" ForeColor="White" />
<InsertItemTemplate>
 Id:
<asp:TextBox ID="IdTextBox" runat="server" Text='<%# Bind("Id") %>' />
<br />
 name:
<asp:TextBox ID="nameTextBox" runat="server" Text='<%# Bind("name") %>' />
<br />
 city:
<asp:TextBox ID="cityTextBox" runat="server" Text='<%# Bind("city") %>' />
<br />
 gender:
<asp:TextBox ID="genderTextBox" runat="server" Text='<%# Bind("gender") %>' />
Vidyalankar School of Information Technology
<br />
<asp:LinkButton ID="InsertButton" runat="server" CausesValidation="True" CommandName="Insert" Text="Insert" />
&nbsp;<asp:LinkButton ID="InsertCancelButton" runat="server" CausesValidation="False" CommandName="Cancel"
Text="Cancel" />
</InsertItemTemplate>
<ItemTemplate>
 Id:
<asp:Label ID="IdLabel" runat="server" Text='<%# Eval("Id") %>' />
<br />
 name:
<asp:Label ID="nameLabel" runat="server" Text='<%# Bind("name") %>' />
<br />
 city:
<asp:Label ID="cityLabel" runat="server" Text='<%# Bind("city") %>' />
<br />
 gender:
<asp:Label ID="genderLabel" runat="server" Text='<%# Bind("gender") %>' />
<br />
 </ItemTemplate>
<PagerStyle BackColor="#2461BF" ForeColor="White" HorizontalAlign="Center" />
<RowStyle BackColor="#EFF3FB" />
</asp:FormView>
</div>
</form>
</body>
</html>
Vidyalankar School of Information Technology
b) Create a web application to display Using Disconnected Data Access and Databinding using GridView.
Code:
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Data;
using System.Data.SqlClient;
using System.Configuration;
namespace WebApplication23
{
 public partial class WebForm2 : System.Web.UI.Page
 {
 protected void Page_Load(object sender, EventArgs e)
 {
 }
 protected void Button1_Click(object sender, EventArgs e)
 {
 SqlConnection con = new SqlConnection(@"Data Source = (LocalDB)\MSSQLLocalDB;
AttachDbFilename =
C:\Users\exam\source\repos\WebApplication23\WebApplication23\App_Data\Database1.mdf; Integrated
Security = True");
 SqlCommand cmd = new SqlCommand("Select * from Student", con);
 SqlDataAdapter da = new SqlDataAdapter(cmd);
 DataSet ds = new DataSet();
 da.Fill(ds, "Student");
 GridView1.DataSource=ds;
 GridView1.DataBind();
 }
 }
}
Vidyalankar School of Information Technology
Vidyalankar School of Information Technology
Advanced Web Programming
Practical #9
1122
Subject/Course: Advanced Web Programming
Topic Working with AJAX and XML
9. Working with AJAX and XML
a) Create a web application to demonstrate reading and writing operation with XML
Webform 1
Add Using system.xml;
Code:
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Xml;
namespace WebApplication25
{
 public partial class WebForm1 : System.Web.UI.Page
 {
 protected void Page_Load(object sender, EventArgs e)
 {
 }
Vidyalankar School of Information Technology
 protected void Button1_Click(object sender, EventArgs e)
 {
 XmlTextWriter writer = new
XmlTextWriter("C:/Users/exam/source/repos/WebApplication25/WebApplication25/XMLFile1.xml", null);
 writer.WriteStartDocument();
 writer.WriteStartElement("Details", "");
 writer.WriteElementString("FirstName", "Sahil");
 writer.WriteElementString("LastName", "Shah");
 writer.WriteElementString("College", "Vsit");
 writer.WriteEndElement();
 writer.WriteEndDocument();
 writer.Close();
 Label1.Text = "Data Written Successfully";
 }
 protected void Button2_Click(object sender, EventArgs e)
 {
 String
xmlNode="C:/Users/exam/source/repos/WebApplication25/WebApplication25/XMLFile1.xml";
 XmlReader xReader = XmlReader.Create(xmlNode);
 while(xReader.Read())
 {
 switch(xReader.NodeType)
 {
 case XmlNodeType.Element:
 ListBox1.Items.Add("<" + xReader.Name + ">");
 break;
 case XmlNodeType.Text:
 ListBox1.Items.Add(xReader.Value);
 break;
 case XmlNodeType.EndElement:
Vidyalankar School of Information Technology
 ListBox1.Items.Add("</" + xReader.Name + ">");
 break;
 }
 }
 }
 }
}
Output:
b) Create a web application to demonstrate Form Security and Windows Security with proper Authentication
and Authorization properties.
Code:
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="WebForm1.aspx.cs"
Inherits="WebApplication8.WebForm1" %>
Vidyalankar School of Information Technology
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
 <title></title>
</head>
<body>
 <form id="form1" runat="server">
 <div>
 <asp:ScriptManager ID="ScriptManager" runat="server">
 </asp:ScriptManager>
 <asp:UpdatePanel ID="UpdatePanel1" runat="server">
 <ContentTemplate>
 <asp:Button ID="Button1" runat="server" OnClick="Button1_Click" Text="Button" />
 <asp:TextBox ID="txtbx1" runat="server"></asp:TextBox>
 <br />
 <asp:Timer ID="Timer1" runat="server" Interval="1000">
 </asp:Timer>
 <br />
 <asp:AdRotator ID="AdRotator1" runat="server" DataSourceID="XmlDataSource1" Height="100px"
Width="200px" />
 <asp:XmlDataSource ID="XmlDataSource1" runat="server"
DataFile="~/XMLFile1.xml"></asp:XmlDataSource>
 <br />
 <br />
 <asp:UpdateProgress ID="UpdateProgress1" runat="server">
Vidyalankar School of Information Technology
 <ProgressTemplate>
 Please wait for some time.....
 </ProgressTemplate>
 </asp:UpdateProgress>
 </ContentTemplate>
 </asp:UpdatePanel>
 </div>
 </form>
</body>
</html>
.cs file:
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
namespace WebApplication8
{
 public partial class WebForm1 : System.Web.UI.Page
 {
 protected void Page_Load(object sender, EventArgs e)
 {
Vidyalankar School of Information Technology
 }
 protected void Button1_Click(object sender, EventArgs e)
 {
 System.Threading.Thread.Sleep(2000);
 txtbx1.Text = DateTime.Now.ToLongTimeString();
 }
 }
}
.xml file:
<?xml version="1.0" encoding="utf-8" ?>
<Advertisements>
 <Ad>
 <ImageUrl>~/img1.jpeg</ImageUrl>
 </Ad>
 <Ad>
 <ImageUrl>~/img2.jpeg</ImageUrl>
 </Ad>
</Advertisements>
Output:
Vidyalankar School of Information Technology
c) Create a web application to demonstrate use of various Ajax controls.
Code:
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="WebForm1.aspx.cs"
Inherits="WebApplication1.WebForm1" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
 <title></title>
</head>
<body>
 <form id="form1" runat="server">
 <div>
 Username:
 <asp:TextBox ID="txtuname" runat="server"></asp:TextBox>
 <br />
Vidyalankar School of Information Technology
 <br />
 Password:
 <asp:TextBox ID="txtpass" runat="server" TextMode="Password"></asp:TextBox>
 <br />
 <br />
 <asp:Button ID="btnlogin" runat="server" Text="Login" OnClick="btnlogin_Click" />
 <br />
 <br />
 <asp:CheckBox ID="chkrem" runat="server" Text=" remember me" />
 </div>
 </form>
</body>
</html>
Webform1.cs:
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Web.Security;
namespace WebApplication1
{
 public partial class WebForm1 : System.Web.UI.Page
 {
 protected void Page_Load(object sender, EventArgs e)
Vidyalankar School of Information Technology
 {
 }
 protected bool authenticate(String uname, String pass)
 {
 if (uname.Equals("ABC")){
 if (pass.Equals("123")){
 return true;
 }
 }
 if (uname.Equals("PQR")){
 if (pass.Equals("100"))
 {
 return true;
 }
 }
 return false;
 }
 protected void btnlogin_Click(object sender, EventArgs e)
 {
 if (authenticate(txtuname.Text, txtpass.Text))
 {
 FormsAuthentication.RedirectFromLoginPage(txtuname.Text, chkrem.Checked);
 Session["username"] = txtuname.Text;
Vidyalankar School of Information Technology
 Response.Redirect("~/WebForm2.aspx");
 }
 else
 {
 Response.Write("Invlaid username or pass");
 }
 }

 }
}
Webform2:
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="WebForm2.aspx.cs"
Inherits="WebApplication1.WebForm2" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
 <title></title>
</head>
<body>
 <form id="form1" runat="server">
 <div>
 <asp:Label ID="Label1" runat="server" Text="Welcome"></asp:Label>
 <br />
 </div>
Vidyalankar School of Information Technology
 </form>
</body>
</html>
webform2.cs:
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
namespace WebApplication1
{
 public partial class WebForm2 : System.Web.UI.Page
 {
 protected void Page_Load(object sender, EventArgs e)
 {
 if (Session["username"] != null)
 {
 Label1.Text = Session["username"].ToString()+" WELCOME";
 }
 }
 }
}
Web.config:
<?xml version="1.0" encoding="utf-8"?>
<!--
Vidyalankar School of Information Technology
 For more information on how to configure your ASP.NET application, please visit
 https://go.microsoft.com/fwlink/?LinkId=169433
 -->
<configuration>
 <system.web>
 <authentication mode="Forms">
 <forms loginUrl="~/WebForm1.aspx"></forms>
 </authentication>
 <authorization>
 <deny users="?"/>
 </authorization>
 <compilation debug="true" targetFramework="4.6.1"/>
 <httpRuntime targetFramework="4.6.1"/>
 </system.web>
 <system.codedom>
 <compilers>
 <compiler language="c#;cs;csharp" extension=".cs"
 type="Microsoft.CodeDom.Providers.DotNetCompilerPlatform.CSharpCodeProvider,
Microsoft.CodeDom.Providers.DotNetCompilerPlatform, Version=2.0.0.0, Culture=neutral,
PublicKeyToken=31bf3856ad364e35"
 warningLevel="4" compilerOptions="/langversion:default /nowarn:1659;1699;1701"/>
 <compiler language="vb;vbs;visualbasic;vbscript" extension=".vb"
 type="Microsoft.CodeDom.Providers.DotNetCompilerPlatform.VBCodeProvider,
Microsoft.CodeDom.Providers.DotNetCompilerPlatform, Version=2.0.0.0, Culture=neutral,
PublicKeyToken=31bf3856ad364e35"
 warningLevel="4" compilerOptions="/langversion:default /nowarn:41008 /define:_MYTYPE=\&quot;Web\&quot;
/optionInfer+"/>
 </compilers>
 </system.codedom>
Vidyalankar School of Information Technology
</configuration>
Output:
"""
    print(code)