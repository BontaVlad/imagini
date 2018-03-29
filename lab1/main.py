import tkinter as tk
from tkinter import Menu, Tk, Label, messagebox
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from PIL import ImageTk, Image
import numpy as np


def hello():
    print("hello!")


window = Tk()
window.title("Join")
window.geometry("800x600")
window.configure(background='grey')

org = None
org_np = None
output = None


def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


sel_filter = rgb2gray


def set_global_data(in_data):
    global org
    global org_np
    org = in_data
    org_np = np.asarray(in_data, dtype=np.uint8)


def render_output():
    global output
    output = sel_filter(org_np)
    return output


def display_output():
    out = render_output()
    image = Image.fromarray(out)
    image_tk = ImageTk.PhotoImage(image)
    panel = Label(window, image=image_tk)
    panel.image = image_tk
    panel.pack(side=tk.RIGHT)


def save_image():
    global output
    img = Image.fromarray(output)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save("image.png")
    messagebox.showinfo("Saving Image", "Image Saved")


def load_file():
    path = askopenfilename(filetypes=(("All files", "*.*"), ))
    if path:
        try:
            img = Image.open(path)
        except Exception:
            showerror("Open Source File", "Failed to read file\n'%s'" % path)
            return

    img_tk = ImageTk.PhotoImage(img)
    panel = Label(window, image=img_tk)
    panel.image = img_tk
    panel.pack(side=tk.LEFT)

    set_global_data(img)
    display_output()


def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

menubar = Menu(window)

# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=load_file)
filemenu.add_command(label="Save", command=save_image)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)

# display the menu
window.config(menu=menubar)
center(window)
window.mainloop()
