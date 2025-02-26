import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import time

# Color Scheme
BG_COLOR = "#FFEDD5"   # Warm Peach  
BTN_COLOR = "#F4A261"  # Sunset Orange  
BTN_HOVER = "#E76F51"  # Coral Pink  
FRAME_COLOR = "#A8DADC" # Ocean Teal  
TEXT_COLOR = "#264653"  # Deep Green  

# TkinterDnD window for Drag & Drop support
root = TkinterDnD.Tk()
root.title("Image Steganography - Decrypt")
root.geometry("700x600")
root.configure(bg=BG_COLOR)

# Button Hover Functions
def on_enter(e): e.widget.config(bg=BTN_HOVER)
def on_leave(e): e.widget.config(bg=BTN_COLOR)

# Title Label
title_label = tk.Label(root, text="Image Steganography - Decrypt", 
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

# Password Entry
pass_label = tk.Label(frame, text="Enter Password:", font=("Comic Sans MS", 18), 
                      bg=FRAME_COLOR, fg=TEXT_COLOR)
pass_label.pack()
pass_entry = tk.Entry(frame, width=30, font=("Comic Sans MS", 16), show="*", bg="#E0E0E0", fg=TEXT_COLOR)
pass_entry.pack(pady=5)

# Progress Bar Label
progress_label = tk.Label(root, text="Decryption Progress:", font=("Comic Sans MS", 16), 
                          bg=BG_COLOR, fg=TEXT_COLOR)
progress_label.pack(pady=5)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

# Decrypt Function
def decrypt_image():
    if not selected_image_path:
        messagebox.showerror("Error", "Please select an encrypted image.")
        return
    entered_password = pass_entry.get()
    if not entered_password:
        messagebox.showerror("Error", "Please enter the password.")
        return

    # Start Progress Bar
    progress_bar["value"] = 0
    for i in range(1, 101, 10):
        time.sleep(0.1)
        progress_bar["value"] = i
        root.update_idletasks()

    # Load Image
    img = cv2.imread(selected_image_path)
    binary_msg = ""
    for row in img:
        for pixel in row:
            for channel in range(3):
                binary_msg += str(pixel[channel] & 1)

    # Convert Binary to Text
    decoded_msg = ""
    for i in range(0, len(binary_msg), 8):
        char = chr(int(binary_msg[i:i+8], 2))
        decoded_msg += char
        if decoded_msg.endswith("####"):
            break

    # Split Password & Message
    try:
        stored_password, hidden_message = decoded_msg.split("||", 1)
        hidden_message = hidden_message.replace("####", "")
    except ValueError:
        messagebox.showerror("Error", "Decryption failed. Corrupted image or incorrect password.")
        return

    # Show Message if Password Matches
    if stored_password == entered_password:
        messagebox.showinfo("Decryption Successful", f"Decrypted Message: {hidden_message}")
    else:
        messagebox.showerror("Error", "Incorrect password! Cannot decrypt message.")

# Decrypt Button
decrypt_button = tk.Button(root, text="Decrypt", font=("Comic Sans MS", 16), 
                           bg=BTN_COLOR, fg="white", relief="flat", command=decrypt_image)
decrypt_button.pack(pady=10)
decrypt_button.bind("<Enter>", on_enter)
decrypt_button.bind("<Leave>", on_leave)

# Clear Fields
def clear_fields():
    global selected_image_path
    selected_image_path = ""
    selected_image_label.config(text="No image selected")
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
