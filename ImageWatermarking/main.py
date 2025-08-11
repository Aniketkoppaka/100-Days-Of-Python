import tkinter as tk
from tkinter import filedialog, font, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

BG_COLOR = "#F0F0F0"
BUTTON_COLOR = "#DDDDDD"
FONT_NAME = "Helvetica"


class WatermarkApp:
    def __init__(self, root):
        """
        Initialize the application window and its widgets.
        """
        self.root = root
        self.root.title("Image Watermarking App")
        self.root.config(padx=50, pady=50, bg=BG_COLOR)
        self.root.resizable(False, False)

        self.image_path = None
        self.original_image = None
        self.watermarked_image = None
        self.image_tk = None

        self.canvas = tk.Canvas(width=600, height=400, bg="white", highlightthickness=0)
        self.canvas_text = self.canvas.create_text(300, 200, text="Upload an image to get started.", font=(FONT_NAME, 16))
        self.canvas.grid(row=0, column=0, columnspan=3, pady=20)

        self.watermark_label = tk.Label(text="Watermark Text:", bg=BG_COLOR, font=(FONT_NAME, 12))
        self.watermark_label.grid(row=1, column=0, sticky="e")
        self.watermark_entry = tk.Entry(width=40)
        self.watermark_entry.insert(0, "© Your Website")
        self.watermark_entry.grid(row=1, column=1, columnspan=2, sticky="w")

        self.upload_button = tk.Button(text="Upload Image", command=self.upload_image, bg=BUTTON_COLOR, width=20)
        self.upload_button.grid(row=2, column=0, pady=10)

        self.add_watermark_button = tk.Button(text="Add Watermark", command=self.apply_watermark, bg=BUTTON_COLOR, width=20)
        self.add_watermark_button.grid(row=2, column=1)

        self.save_button = tk.Button(text="Save Image", command=self.save_image, bg=BUTTON_COLOR, width=20)
        self.save_button.grid(row=2, column=2)

    def upload_image(self):
        """
        Opens a file dialog to let the user select an image.
        Displays a thumbnail of the image in the canvas.
        """
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif *.bmp"), ("All files", "*.*")]
        )
        if not self.image_path:
            return

        self.original_image = Image.open(self.image_path).convert("RGBA")

        display_image = self.original_image.copy()
        display_image.thumbnail((600, 400))
        self.image_tk = ImageTk.PhotoImage(display_image)

        self.canvas.delete(self.canvas_text)
        self.canvas.config(width=display_image.width, height=display_image.height)
        self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)

        messagebox.showinfo("Success", "Image uploaded successfully!")

    def apply_watermark(self):
        """
        Applies the text from the entry field as a watermark on the image.
        """
        if not self.original_image:
            messagebox.showerror("Error", "Please upload an image first.")
            return

        watermark_text = self.watermark_entry.get()
        if not watermark_text:
            messagebox.showerror("Error", "Please enter watermark text.")
            return

        self.watermarked_image = self.original_image.copy()

        draw = ImageDraw.Draw(self.watermarked_image)
        width, height = self.watermarked_image.size
        font_size = int(width / 20)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        left, top, right, bottom = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = right - left
        text_height = bottom - top

        x = width - text_width - 20
        y = height - text_height - 20

        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))

        display_image = self.watermarked_image.copy()
        display_image.thumbnail((600, 400))
        self.image_tk = ImageTk.PhotoImage(display_image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)

        messagebox.showinfo("Success", "Watermark added! You can now save the image.")

    def save_image(self):
        """
        Opens a 'save as' dialog to save the watermarked image.
        """
        if not self.watermarked_image:
            messagebox.showerror("Error", "Please add a watermark first.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG file", "*.png"), ("JPEG file", "*.jpg"), ("All files", "*.*")]
        )
        if not save_path:
            return

        if save_path.lower().endswith('.jpg') or save_path.lower().endswith('.jpeg'):
            self.watermarked_image.convert("RGB").save(save_path)
        else:
            self.watermarked_image.save(save_path)

        messagebox.showinfo("Success", f"Image saved to {save_path}")

if __name__ == "__main__":
    window = tk.Tk()
    app = WatermarkApp(window)
    window.mainloop()