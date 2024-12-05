import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import Frame, Button, Label, Canvas
import cv2
from PIL import Image, ImageTk
import numpy as np
from sklearn.cluster import KMeans

class DominantColorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deteksi Warna")
        self.root.configure(bg="#282c34")
        self.image = None
        self.tk_image = None
        self.dominant_color = None

        # Judul aplikasi
        self.title_label = Label(root, text="Aplikasi Deteksi Warna By agusgabagus", font=("Arial", 16, "bold"), fg="#61dafb", bg="#282c34")
        self.title_label.pack(pady=10)

        # Frame untuk tombol
        self.button_frame = Frame(root, bg="#3a3f47")
        self.button_frame.pack(pady=10, fill="x")

        # Tombol untuk memuat gambar
        self.load_button = Button(self.button_frame, text="Masukan Foto", command=self.load_image, bg="#61dafb", fg="white", width=15)
        self.load_button.grid(row=0, column=0, padx=10, pady=5)

        # Tombol untuk mendeteksi warna dominan
        self.detect_button = Button(self.button_frame, text="Deteksi Warna", command=self.detect_dominant_color, bg="#61dafb", fg="white", width=20)
        self.detect_button.grid(row=0, column=1, padx=10, pady=5)

        # Label untuk menampilkan gambar
        self.image_label = Label(root, bg="#3a3f47", borderwidth=2, relief="groove")
        self.image_label.pack(pady=10)

        # Canvas untuk menampilkan warna dominan
        self.color_canvas = Canvas(root, width=100, height=100, bg="#3a3f47", borderwidth=2, relief="groove")
        self.color_canvas.pack(pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not file_path:
            return
        self.image = cv2.imread(file_path)
        self.display_image(self.image)

    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(img_rgb)
        self.tk_image = ImageTk.PhotoImage(pil_image)
        
        # Update label gambar
        self.image_label.config(image=self.tk_image)
        self.image_label.image = self.tk_image  # Keep reference

    def detect_dominant_color(self):
        if self.image is not None:
            # Resize gambar untuk mempercepat proses
            resized_image = cv2.resize(self.image, (100, 100))
            reshaped_image = resized_image.reshape((-1, 3))

            # Gunakan KMeans untuk menemukan warna dominan
            kmeans = KMeans(n_clusters=1, random_state=0)
            kmeans.fit(reshaped_image)
            self.dominant_color = kmeans.cluster_centers_[0].astype(int)

            # Tampilkan warna dominan pada canvas
            hex_color = "#{:02x}{:02x}{:02x}".format(*self.dominant_color)
            self.color_canvas.create_rectangle(0, 0, 100, 100, fill=hex_color)
            messagebox.showinfo("Warna", f"Warna Yang Dominan: {hex_color.upper()}")
        else:
            messagebox.showerror("Error", "Please load an image first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DominantColorApp(root)
    root.mainloop()
