import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import time

# Color Scheme
BG_COLOR = "#FFEDD5"   # Warm Peach  
BTN_COLOR = "#F4A261"  # Sunset Orange  
BTN_HOVER = "#E76F51"  # Coral Pink  
FRAME_COLOR = "#A8DADC" # Ocean Teal  
TEXT_COLOR = "#264653"  # Deep Green  

# TkinterDnD window for Drag & Drop support
root = TkinterDnD.Tk()
root.title("Image Steganography - Encrypt")
root.geometry("700x700")
root.configure(bg=BG_COLOR)

# Button Hover Functions
def on_enter(e): e.widget.config(bg=BTN_HOVER)
def on_leave(e): e.widget.config(bg=BTN_COLOR)

# Title Label
title_label = tk.Label(root, text="Image Steganography - Encrypt", 
                       font=("Comic Sans MS", 26, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
title_label.pack(pady=15)

# Frame for Inputs
frame = tk.Frame(root, bg=FRAME_COLOR, bd=3, relief="ridge")
frame.pack(pady=10, padx=20, fill="both")

# Selected Image Label
selected_image_label = tk.Label(frame, text="No image selected", 
                                font=("Comic Sans MS", 16), bg=FRAME_COLOR, fg=TEXT_COLOR)
selected_image_label.pack(pady=5)

# Select Image Function
def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        update_image_selection(file_path)

def update_image_selection(file_path):
    global selected_image_path
    selected_image_path = file_path
    selected_image_label.config(text=os.path.basename(file_path))

# Select Image Button
select_button = tk.Button(frame, text="Browse Image", font=("Comic Sans MS", 16), 
                          bg=BTN_COLOR, fg="white", relief="flat", command=select_image)
select_button.pack(pady=5)
select_button.bind("<Enter>", on_enter)
select_button.bind("<Leave>", on_leave)

# Drag & Drop Label
drag_label = tk.Label(frame, text="Or Drag & Drop an Image Here", 
                      font=("Comic Sans MS", 18), bg=FRAME_COLOR, fg=TEXT_COLOR)
drag_label.pack(pady=5)

# Drag & Drop Function
def drop(event):
    file_path = event.data.strip().strip("{}")
    if os.path.isfile(file_path) and file_path.lower().endswith((".png", ".jpg", ".jpeg")):
        update_image_selection(file_path)
        messagebox.showinfo("Success", f"File Dropped: {os.path.basename(file_path)}")
    else:
        messagebox.showerror("Error", "Invalid file type. Please drop a PNG or JPG image.")

# Message Entry
msg_label = tk.Label(frame, text="Enter Secret Message:", 
                     font=("Comic Sans MS", 18), bg=FRAME_COLOR, fg=TEXT_COLOR)
msg_label.pack()
msg_entry = tk.Entry(frame, width=40, font=("Comic Sans MS", 16), bg="#E0E0E0", fg=TEXT_COLOR)
msg_entry.pack(pady=5)

# Password Entry
pass_label = tk.Label(frame, text="Enter Password:", 
                      font=("Comic Sans MS", 18), bg=FRAME_COLOR, fg=TEXT_COLOR)
pass_label.pack()
pass_entry = tk.Entry(frame, width=30, font=("Monotype Corsiva", 16), show="*", bg="#E0E0E0", fg=TEXT_COLOR)
pass_entry.pack(pady=5)

# Progress Bar Label
progress_label = tk.Label(root, text="Encryption Progress:", 
                          font=("Comic Sans MS", 16), bg=BG_COLOR, fg=TEXT_COLOR)
progress_label.pack(pady=5)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

# Encrypt Function
def encrypt_image():
    global selected_image_path
    if not selected_image_path:
        messagebox.showerror("Error", "Please select an image.")
        return
    message = msg_entry.get()
    password = pass_entry.get()
    if not message or not password:
        messagebox.showerror("Error", "Message and password cannot be empty.")
        return

    # Combine password & message
    combined_message = password + "||" + message + "####"
    binary_msg = ''.join(format(ord(char), '08b') for char in combined_message)

    # Load Image
    img = cv2.imread(selected_image_path)
    h, w, _ = img.shape
    total_pixels = h * w * 3
    if len(binary_msg) > total_pixels:
        messagebox.showerror("Error", "Message is too long for this image.")
        return

    # Hide Message in Image (LSB)
    index = 0
    for row in img:
        for pixel in row:
            for channel in range(3):
                if index < len(binary_msg):
                    pixel[channel] = np.uint8((int(pixel[channel]) & ~1) | int(binary_msg[index]))
                    index += 1

    # Start Progress Bar
    progress_bar["value"] = 0
    for i in range(1, 101, 10):
        time.sleep(0.1)
        progress_bar["value"] = i
        root.update_idletasks()

    # Save Encrypted Image
    encrypted_image_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                         filetypes=[("PNG Image", "*.png")])
    if encrypted_image_path:
        cv2.imwrite(encrypted_image_path, img)
        messagebox.showinfo("Success", "Image encrypted and saved successfully!")

# Encrypt Button
encrypt_button = tk.Button(root, text="Encrypt", font=("Comic Sans MS", 16), 
                           bg=BTN_COLOR, fg="white", relief="flat", command=encrypt_image)
encrypt_button.pack(pady=10)
encrypt_button.bind("<Enter>", on_enter)
encrypt_button.bind("<Leave>", on_leave)

# Clear Fields
def clear_fields():
    global selected_image_path
    selected_image_path = ""
    selected_image_label.config(text="No image selected")
    msg_entry.delete(0, tk.END)
    pass_entry.delete(0, tk.END)
    progress_bar["value"] = 0

# Clear Button
clear_button = tk.Button(root, text="Clear", font=("Comic Sans MS", 16), 
                         bg=BTN_COLOR, fg="white", relief="flat", command=clear_fields)
clear_button.pack(pady=5)
clear_button.bind("<Enter>", on_enter)
clear_button.bind("<Leave>", on_leave)

# Enable Drag & Drop
root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", drop)

selected_image_path = ""
root.mainloop()
