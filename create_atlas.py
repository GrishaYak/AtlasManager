import os
from tkinter import filedialog, Tk, Button
from PIL import Image
from os import path, listdir
import numpy as np
import xml.etree.ElementTree as ET


def get_file_names():
    w.title("Choose the images")
    width = 300
    height = 150
    x = 1920 // 2 - width - 40
    y = 1080 // 2 - height - 50
    w.geometry(f"{width}x{height}+{x}+{y}")

    btn_dir = Button(w, text="Open the\nDirectory", command=open_dir,
                     font=("Arial", 20))
    btn_dir.place(x=0, y=0, width=width, height=height//2)
    btn_files = Button(w, text="Open Files", command=open_files,
                       font=("Arial", 20))
    btn_files.place(x=0, y=height//2, width=width, height=height//2)
    w.mainloop()

def open_dir():
    w.destroy()
    dir_path = filedialog.askdirectory(initialdir=mydir)
    only_files = [f for f in listdir(dir_path) if '.' in f]
    file_names = []
    for el in only_files:
        ok = False
        for f in image_formates:
            if f in el:
                ok = True
                break
        if not ok:
            continue
        file_names.append(path.join(dir_path, el))
    main(file_names)

def open_files():
    w.destroy()
    file_type = ' '.join(['*' + x for x in image_formates])
    file_names = filedialog.askopenfilenames(
        title="Выберите файлы",
        filetypes=[
            ("Images", file_type),
            ("All types", "*.*")
        ],
        initialdir=mydir,
    )
    main(file_names)

def main(file_names):
    if not file_names:
        return
    global out_dir
    if out_dir is None:
        least = min(file_names, key=len).replace('\\', '/')
        out_dir = least[:least.rfind('/')]
        last_dir = out_dir[out_dir.rfind('/') + 1:]
        if last_dir in {'images', 'ims'}:
            out_dir = out_dir[:-len(last_dir) - 1]
        out_dir += '/res'

    images = []
    height = 0
    width = 0
    for file in file_names:
        with Image.open(file) as img:
            img.load()
            images.append(img.convert('RGBA'))
            width += img.size[0]
            height = max(height, img.size[1])

    res = np.zeros((height, width, 4), dtype=np.uint8)
    x = 0
    y = 0
    root = ET.Element("Regions")
    for i in range(len(file_names)):
        img = images[i]
        name = file_names[i].split("/")[-1].split(".")[0]
        w, h = img.size[:2]
        ET.SubElement(root, "Region", attrib={"name": name, "x": str(x), "y": str(y)
            , "width": str(w), "height": str(h)})
        res[y:y + h, x:x + w] = img
        x += w
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    tree = ET.ElementTree(root)
    tree.write(f"{out_dir}/atlas.xml", encoding="utf-8", xml_declaration=True)
    atlas = Image.fromarray(res)
    atlas.save(f"{out_dir}/atlas.png")

if __name__ == '__main__':
    # mydir = path.dirname(path.realpath(__file__))
    mydir = 'D:/cs/atlasManager'
    out_dir = None
    w = Tk()
    image_formates = '.jpg .png .gif .webp'.split(' ')
    get_file_names()
