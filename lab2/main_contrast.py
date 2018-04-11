import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from PIL import ImageTk, Image
import numpy as np
import pygubu


class MyApplication(pygubu.TkApplication):

    def _create_ui(self):
        self.builder = builder = pygubu.Builder()

        builder.add_from_file('lab2_contrast.ui')

        self.mainwindow = builder.get_object('mainwindow', self.master)

        self.mainmenu = menu = builder.get_object('mainmenu', self.master)
        self.set_menu(menu)

        # Configure callbacks
        builder.connect_callbacks(self)

    def on_mfile_item_clicked(self, itemid):
        if itemid == 'mfile_open':
            file_path = askopenfilename(filetypes=(("All files", "*.*"), ))
            if not file_path:
                return
            self.file_path = file_path
            self.process_input(file_path)

        if itemid == 'mfile_save':
            messagebox.showinfo('Saving', 'File saved')

        if itemid == 'mfile_quit':
            self.quit()

    def change_contrast(self, img, level):
        factor = (259 * (level + 255)) / (255 * (259 - level))

        def contrast(c, d):
            value = 128 + factor * (c - 128)
            return max(0, min(255, value))

        vfunc = np.vectorize(contrast)
        return Image.fromarray(vfunc(img, factor).astype(np.uint8))

    def on_scale_changed(self, *args):
        scale = self.builder.get_object('sc_contrast')
        self.render('cv_result', self.change_contrast(self.image, scale.get()))

    def on_about_clicked(self):
        messagebox.showinfo('About', 'Histogram examples for lab 2')

    def resize(self, c_w, c_h, img):
        ratio_w = c_w / img.width
        ratio_h = c_h / img.height
        return img.resize((int(img.width*ratio_w),
                           int(img.height*ratio_h)))

    def render(self, canvas_name, img):
        canvas = self.builder.get_object(canvas_name, self.master)
        img = ImageTk.PhotoImage(image=self.resize(
            canvas.winfo_reqwidth(),
            canvas.winfo_reqheight(), img))
        canvas.create_image(0, 0, image=img, anchor=tk.NW)
        canvas.image = img
        canvas.pack(side="top", fill="both", expand=True)

    def process_input(self, file_path):
        img = Image.open(file_path)
        self.render('preview_original', img)
        img = np.asarray(img, dtype=np.uint8)
        self.image = img
        self.on_scale_changed(None)


if __name__ == '__main__':
    root = tk.Tk()
    app = MyApplication(root)
    app.run()
