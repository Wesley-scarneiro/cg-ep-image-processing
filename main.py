import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

def plot_image_subplot(position, image, title, cmap=None):
    plt.subplot(2, 3, position)
    plt.imshow(image, cmap=cmap)
    plt.title(title)
    plt.axis('off')

def plot_images(image_rgb, gaussian_blurred, opened_image, segmented_image, result_image, image_name):
    plt.figure(figsize=(20, 10))

    plot_image_subplot(1, image_rgb, 'Original')
    plot_image_subplot(2, gaussian_blurred, 'Gaussiana Suavizada', cmap='gray')
    plot_image_subplot(3, opened_image, 'Erosão e dilatação', cmap='gray')
    plot_image_subplot(4, segmented_image, 'Filtro', cmap='gray')
    plot_image_subplot(5, result_image, 'Resultado Final')

    plt.savefig(f'output/{image_name.replace(".jpg", "")}_segmented.jpg')
    plt.show()

def process_image(image_name: str):
    original_image = cv2.imread(f'images/{image_name}')
  
    imagem_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    imagem_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # Filtros de suavização da imagem
    gaussian_blurred = cv2.GaussianBlur(imagem_gray, (15, 15), 0)

    # Abertura morfológica (erosão e dilatação)
    kernel = np.ones((50, 50), np.uint8)
    opened_image = cv2.morphologyEx(gaussian_blurred, cv2.MORPH_OPEN, kernel)

    # Thresholding para segmentar a imagem suavizada
    _, segmented_image = cv2.threshold(opened_image, 40, 255, cv2.THRESH_BINARY)
    result_image = np.ones_like(imagem_rgb) * 255
    result_image[segmented_image == 255] = imagem_rgb[segmented_image == 255]

    # Exibir e salvar o resultado
    plot_images(imagem_rgb, gaussian_blurred, opened_image, segmented_image, result_image, image_name)

def get_images(directory):
    images = []
    for entry in os.listdir(directory):
        images.append(entry)
    return images

def main():
    images = get_images("images/")
    for image in images:
        process_image(image)
    # process_image('heic0910i.jpg')

if __name__ == "__main__":
    main()
