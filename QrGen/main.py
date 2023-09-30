import sys
import tkinter.messagebox
import os
from tkinter import filedialog, colorchooser, simpledialog
from PIL import Image
import qrcode
from customtkinter import *
from tkinter.ttk import *

root = CTk()
root.title("QrGen")
root.geometry("740x400")

image_path_label = CTkLabel(root, text="  ")

file = ""
hex_color = "white"
bg_color = "black"
basewidth = 100
logo = None  # Store the logo image

def open_logo_image():
    global logo
    try:
        deez = filedialog.askopenfile(mode='rb', filetypes=[('Image Files', '*.jpg')])
        if deez:
            logo = Image.open(deez)
            print("Logo opened successfully!")
            tkinter.messagebox.showinfo("Success!", "Successfully opened the logo!")
        else:
            tkinter.messagebox.showinfo("Info", "No file selected.")
    except Exception as e:
        print(e)
        tkinter.messagebox.showerror("Error", "Error opening the logo: " + str(e))

label_frame = CTkFrame(root, width=200)
label_frame.pack(side=LEFT, fill=Y)

url_entry = CTkEntry(root, width=650)
CTkLabel(label_frame, text="URL: ").pack(pady=15)
url_entry.pack(pady=15, padx=10)

CTkLabel(label_frame, text="Logo (optional):").pack()
CTkButton(root, text="Select Logo Image", command=open_logo_image).pack()

def pick_qr_color():
    global hex_color
    color_code = colorchooser.askcolor(title="Choose color")
    if color_code[0] is not None:
        hex_color = color_code[0]
        print(hex_color)
    else:
        tkinter.messagebox.showerror("No color selected.", "Select a color to continue")

def pick_bg_color():
    global bg_color
    color_code = colorchooser.askcolor(title="Choose color")
    if color_code[0] is not None:
        bg_color = color_code[0]
        print(bg_color)
    else:
        tkinter.messagebox.showerror("No color selected.", "Select a color to continue")

CTkLabel(label_frame, text="QR Color:").pack(pady=15)
CTkButton(root, text="Pick QR Color", command=pick_qr_color).pack(pady=15, padx=10)

CTkLabel(label_frame, text="Background Color:").pack()
CTkButton(root, text="Pick Background Color", command=pick_bg_color).pack(padx=10)

def genQr():
    global logo
    global url_entry

    url = url_entry.get()

    if logo is None:
        tkinter.messagebox.showinfo("Info", "No logo selected.")
        return

    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo_resized = logo.resize((basewidth, hsize))

    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )

    # Adding URL or text to QRcode
    QRcode.add_data(url)

    # Generating QR code
    QRcode.make()


    QRimg = QRcode.make_image(
        fill_color=hex_color, back_color=bg_color).convert('RGB')

    # Set size of QR code
    pos = ((QRimg.size[0] - logo_resized.size[0]) // 2,
           (QRimg.size[1] - logo_resized.size[1]) // 2)
    QRimg.paste(logo_resized, pos)

    file_name = CTkInputDialog(title="Filename", text="How should I save your QR?")
    file_name = file_name.get_input()
    file_name = file_name + ".png"

    # Save the QR code generated
    QRimg.save(file_name)

    print('QR code generated!')

CTkButton(root, text="Generate Custom QR Code", command=genQr).pack(side=BOTTOM)

root.mainloop()
