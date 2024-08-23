#!/usr/bin/env python
# coding: utf-8

# In[2]:


from PIL import Image, ImageFile
import os
import numpy as np
ImageFile.LOAD_TRUNCATED_IMAGES = True


# In[3]:


def new_position(position, stride, dimensions):
    position = (position[0] + stride, position[1])
    if position[0] < dimensions[0] and position[1] < dimensions[1]:
        return position
    else:
        np = (-stride, position[1] + stride)
        return new_position(np, stride, dimensions)
        


# In[4]:


def mcd(num_a, num_b):
    mcd = 0
    for i in range(1, min(num_a, num_b) + 1):
        if (num_a % i == 0) and (num_b % i == 0):
            # print(f"i = {i } = nai {num_a % i }, nbi = {num_b % i } ") 
            mcd = i
    return mcd


# In[32]:


def get_sorted_images(dir, sortdata):
    images = [(image,Image.open(image)) for image in os.listdir(dir) if image.endswith(".jpg")]
    nums = [sortdata[key] for key,value in images]
    c_images = [0 for i in range(len(images))]
    for (_, image), position in zip(images, nums):
        c_images.insert(position,image)
    c_images = [image for image in c_images if image != 0]
    return [image.resize((stride,stride)) for image in c_images]


# In[13]:


with open("dump_albumes_all.txt") as file:
    sortdata = file.readlines()
    sortdata.reverse()
    sortdata = {f'albumArt_{album.split("->")[0].strip()}.jpg': n for n, album in enumerate(sortdata)}


# In[34]:


dimensions = (1080, 1920)
stride = mcd(*dimensions)
stride = 120
resized_images = get_sorted_images("./dump2", sortdata)
new_image = Image.new('RGB', dimensions)
position = (0,0)
cntr = 0
for image in resized_images:
    new_image.paste(image, box = position)
    position = new_position(position, stride, dimensions)
    if (position[1] >= (dimensions[1] - stride )) and (position[0] >= (dimensions[0] - stride)):
        break
    
new_image.save("final_2_phone.png")

