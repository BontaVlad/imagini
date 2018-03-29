import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt

from PIL import ImageTk, Image
import numpy as np
import pygubu


class MyApplication(pygubu.TkApplication):

    def _create_ui(self):
        self.builder = builder = pygubu.Builder()

        builder.add_from_file('lab2.ui')

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

    def on_mcolor_item_clicked(self, itemid):
        if getattr(self, "selected", None) is None:
            self.selected = itemid
        labels = {
            "mc_red": "Red",
            "mc_green": "Green",
            "mc_blue": "Blue",
        }
        self.mainmenu.entryconfig(labels[self.selected], state=tk.NORMAL)

        self.selected = itemid
        self.mainmenu.entryconfig(labels[itemid], state=tk.DISABLED)

        self.render('preview_color', self.output[itemid]['color'])
        self.render('preview_histogram', self.output[itemid]['histogram'])
        self.render('preview_color_eq', self.output[itemid]['color_eq'])

    def on_about_clicked(self):
        messagebox.showinfo('About', 'Histogram examples for lab 2')

    def process_image(self, input_data):
        result = {
            "mc_red": {
                "color": None,
                "histogram": None,
                "color_eq": None
            },
            "mc_green": {
                "color": None,
                "histogram": None,
                "color_eq": None
            },
            "mc_blue": {
                "color": None,
                "histogram": None,
                "color_eq": None
            },
        }

        img = np.asarray(input_data, dtype=np.uint8)
        channels = img[:,:,0], img[:,:,1], img[:,:,2]  # noqa
        for channel, key in zip(channels, result.keys()):
            image_histogram, bins = np.histogram(channel, 'sqrt', normed=True)
            cdf = image_histogram.cumsum()  # cumulative distribution function
            cdf = 255 * cdf / cdf[-1]  # normalize
            image_equalized = np.interp(channel.flatten(), bins[:-1], cdf)

            output_name = f"histogram_{key}.jpeg"
            plt.hist(channel.flatten(), bins=bins)
            plt.savefig(output_name)

            result[key]["color"] = Image.fromarray(channel)
            result[key]['color_eq'] = Image.fromarray(image_equalized.reshape(channel.shape))  # noqa
            result[key]['histogram'] = Image.open(output_name)
        return result

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
        self.output = self.process_image(img)
        self.on_mcolor_item_clicked("mc_red")


if __name__ == '__main__':
    root = tk.Tk()
    app = MyApplication(root)
    app.run()
