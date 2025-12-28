# AtlasManager

#### This is a program that will help you with creating texture atlases.

---

### What is a texture atlas?

Texture atlas is an image that contains multiple textures inside of it and has a file describing which textures are in this atlas and where are they. 

These atlases are needed in gamedev for instance. It is faster to load one texture and draw its regions multiple times than loading one texture and only drawing it once until loading another. You can read about this here: [Chapter 07: Optimizing Texture Rendering | MonoGame](https://docs.monogame.net/articles/tutorials/building_2d_games/07_optimizing_texture_rendering/index.html)

---

### Installation

1) Download the code from this repo

2) Create a virtual enviroment with libraries specified in requirements.txt

3) Done! It's ready to work

---

### How to use it?

* #### create_atlas
  
  It will ask you whether you want to choose 1) A directory containing all textures that you need in your atlas; or 2) Textures one by one. Than it will create a folder atlas/ that will contain atlas.png (image that contains or chosen textures) and atlas.xml (file that describes the atlas). 
  
  You may also create atlas from other atlases. To do this, you just have to choose not only an atlas image but also a .xml file that describes it. However, .xml file and image must have the same names, otherwise AtlasManager won't understand what does the .xml file relate to.

* #### disassemble_atlas
  
  Create input.txt file that contains to lines: 1) full path to an image that you want to disassemble; 2) full path to .xml file that describes an atlas that you want to dissasemble. After it finishes its work, you will have a folder named images that will contain all the textures that were in atlas.


