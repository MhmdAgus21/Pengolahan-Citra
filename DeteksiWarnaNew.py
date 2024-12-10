import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

# Fungsi untuk memilih dan memproses gambar
def load_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
    )
    if not file_path:
        return
    img = cv2.imread(file_path)
    process_image(img)

# Fungsi untuk memproses gambar
def process_image(img):
    # Konversi citra RGB ke HSV
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Reshape data untuk clustering
    pixel_data = hsv_img.reshape((-1, 3))
    pixel_data = np.float32(pixel_data)

    # K-Means Clustering
    k = 3  # Jumlah klaster
    kmeans = KMeans(n_clusters=k, random_state=0).fit(pixel_data)
    clustered = kmeans.labels_.reshape(hsv_img.shape[:2])

    # Warna dominan
    colors = kmeans.cluster_centers_
    dominant_colors = colors.astype(int)

    # Tampilkan hasil
    show_results(img, hsv_img, clustered, dominant_colors)

# Fungsi untuk menampilkan hasil
def show_results(original, hsv, clustered, dominant_colors):
    # Visualisasi hasil
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.title("Original Image")
    plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    plt.axis("off")

    plt.subplot(2, 2, 2)
    plt.title("HSV Image")
    plt.imshow(hsv[:, :, 0], cmap='hsv')
    plt.axis("off")

    plt.subplot(2, 2, 3)
    plt.title("Clustered Image")
    plt.imshow(clustered, cmap='viridis')
    plt.axis("off")

    # Menampilkan warna dominan
    plt.subplot(2, 2, 4)
    plt.title("Dominant Colors")
    for i, color in enumerate(dominant_colors):
        plt.bar(i, 1, color=np.array(color) / 255, edgecolor='black')
    plt.xticks(range(len(dominant_colors)), [f"Color {i+1}" for i in range(len(dominant_colors))])
    plt.axis("off")

    plt.tight_layout()
    plt.show()

# Fungsi utama untuk GUI
def main():
    root = tk.Tk()
    root.title("Image Processing with K-Means")
    root.geometry("500x300")
    root.configure(bg="#f0f0f0")  # Warna latar belakang aplikasi

    title_label = tk.Label(
        root, text="Image Processing with K-Means", 
        font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333"
    )
    title_label.pack(pady=10)

    btn_load = tk.Button(
        root, text="Load Image", command=load_image, 
        width=20, bg="#4caf50", fg="white", font=("Helvetica", 12, "bold")
    )
    btn_load.pack(pady=20)

    btn_exit = tk.Button(
        root, text="Exit", command=root.destroy, 
        width=20, bg="#f44336", fg="white", font=("Helvetica", 12, "bold")
    )
    btn_exit.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
