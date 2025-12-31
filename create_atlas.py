import os
from tkinter import filedialog, Tk, Button
from PIL import Image
from os import path, listdir
import numpy as np
import xml.etree.ElementTree as ET
from disassemble_atlas import dissasemble_atlas

def create_w():
    global w
    w = Tk()
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


def open_dir():
    w.destroy()
    dir_path = filedialog.askdirectory(initialdir=initial_dir)
    if not dir_path:
        create_w()
        w.mainloop()
        return
    only_files = [f for f in listdir(dir_path) if '.' in f]
    file_names = []
    for el in only_files:
        ok = '.xml' in el
        for f in image_formates:
            if f in el:
                ok = True
                break
        if not ok:
            continue
        file_names.append(path.join(dir_path, el))
    process(file_names)

def open_files():
    w.destroy()
    file_type = ' '.join(['*' + x for x in image_formates])
    file_names = filedialog.askopenfilenames(
        title="Выберите файлы",
        filetypes=[
            ("Images", file_type, "Atlas", '*.xml'),
            ("All types", "*.*")
        ],
        initialdir=initial_dir,
    )
    if not file_names:
        create_w()
        w.mainloop()
        return
    process(file_names)

def process(file_names):
    imgs = []
    xmls = []
    for f in file_names:
        if '.xml' in f:
            xmls.append(f)
            continue
        imgs.append(f)
    main(imgs, xmls)

def get_xml(image_name, xml_names):
    name = image_name.split('/')[-1]
    name = name[:name.rfind('.')]
    xml = ''
    for description in xml_names:
        short = description.split('/')[-1].rstrip('.xml')
        if short == name:
            xml = description
            break
    return xml

def main(image_names, xml_names):
    if not image_names:
        return
    global out_dir
    # if out_dir is None:
    #     least = min(file_names, key=len).replace('\\', '/')
    #     out_dir = least[:least.rfind('/')]
    #     last_dir = out_dir[out_dir.rfind('/') + 1:]
    #     if last_dir in {'images', 'ims'}:
    #         out_dir = out_dir[:-len(last_dir) - 1]
    #     out_dir += '/atlas'
    out_dir = mydir + '/atlas'

    images = []
    height = 0
    width = 0

    for file in image_names:
        with Image.open(file) as img:
            img.load()
            images.append(img.convert('RGBA'))
            width += img.size[0]
            height = max(height, img.size[1])
    ind = -1
    for i in range(len(image_names)):
        if "font.png" in image_names[i]:
            ind = i
            break
    if ind != -1:
        image_names = [image_names[ind]] + image_names[:ind] + image_names[ind + 1:]
        images = [images[ind]] + images[:ind] + images[ind + 1:]
    res = np.zeros((height, width, 4), dtype=np.uint8)
    x = 0
    y = 0
    root = ET.Element("TextureAtlas")
    texture = ET.SubElement(root, "Texture")
    texture.text = "images/atlas"
    regions = ET.SubElement(root, "Regions")
    for i in range(len(image_names)):
        img = images[i]
        w, h = img.size[:2]
        res[y:y + h, x:x + w] = img

        xml = get_xml(image_names[i], xml_names)
        if xml:
            cur_atlas = ET.parse(xml)
            cur_rt = cur_atlas.getroot()
            cur_regions = cur_rt.find('Regions')
            for region in cur_regions:
                atr = region.attrib
                reg_name = atr['name']
                reg_x = int(atr['x'])
                reg_y = int(atr['y'])
                reg_width = atr['width']
                reg_height = atr['height']
                ET.SubElement(regions, "Region", attrib={"name": reg_name, "x":str(reg_x + x), "y":str(reg_y+y), 
                                                         "width": reg_width, "height": reg_height})
        else:
            name = image_names[i].split("/")[-1].split(".")[0]
            ET.SubElement(regions, "Region", attrib={"name": name, "x": str(x), "y": str(y)
                , "width": str(w), "height": str(h)})
        
        x += w

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    tree = ET.ElementTree(root)
    tree.write(f"{out_dir}/atlas.xml", encoding="utf-8", xml_declaration=True)
    atlas = Image.fromarray(res)
    atlas.save(f"{out_dir}/atlas.png")

if __name__ == '__main__':
    mydir = path.dirname(path.realpath(__file__))
    initial_dir = '~/cs/atlas'
    out_dir = None
    w = None
    image_formates = '.jpg .png .gif .webp'.split(' ')
    create_w()
    w.mainloop()
