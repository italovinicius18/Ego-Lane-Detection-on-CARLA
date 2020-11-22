#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pickle
import cv2
import glob
import os
from tqdm import tqdm
import matplotlib.pyplot as plt


# In[2]:


images = []
ground_truth = []

#for image in glob.glob('./raw/*.jpg'):
#    images.append(image)
#for image in glob.glob('./rotated/raw/*.jpg'):
#    images.append(image)
#for image in glob.glob('./flipped/raw/*.jpg'):
#    images.append(image)
#for image in glob.glob('./flipped/rotated/raw/*.jpg'):
#    images.append(image)

for gt in glob.glob('./warped/*.jpg'):
    ground_truth.append(gt)
for gt in glob.glob('./rotated/warped/*.jpg'):
    ground_truth.append(gt)
for gt in glob.glob('./flipped/warped/*.jpg'):
    ground_truth.append(gt)
for gt in glob.glob('./flipped/rotated/warped/*.jpg'):
    ground_truth.append(gt)


# In[3]:


print(len(images),len(ground_truth))
dim = (80, 160)


# In[4]:


def resize_gt_image(image):
    gt = cv2.resize(image,dim)
    gt = gt[:,:,1]
    gt = np.reshape(gt,(80,160,1))
    return image


# In[5]:


def resize_raw_image(image):
    image = cv2.resize(image,dim)
    return image


# In[6]:


def convert_list_to_pickle(name_file,image_list):
    with open(f"{name_file}.pkl", 'wb') as f:
        pickle.dump(image_list, f)


# In[7]:


images_resized = [[],[],[]]
ground_truth_resized = []


# In[ ]:


#i = 0
#for image in tqdm(images):
#    image = cv2.imread(image)
#    image = resize_raw_image(image)
#    images_resized[i].append(image)
#    if (len(images_resized[i]) == 5000 ):
#        i+=1
#    
#for i,batch in enumerate(images_resized):
#    convert_list_to_pickle(f'raw_images_{i}',batch)


# In[ ]:


i = 3  
for gt in range(len(ground_truth)-1,0,-1):
    gt = cv2.imread(ground_truth[gt])
    gt = resize_gt_image(gt)
    ground_truth_resized.append(gt)
    print(len(ground_truth_resized))
    if (len(ground_truth_resized) == 3088):
        i+=1
        convert_list_to_pickle(f'labels_{i}',ground_truth_resized)
        ground_truth_resized = []

convert_list_to_pickle(f'labels_{i}',ground_truth_resized)


# In[10]:


#train_images1 = pickle.load(open("raw_images_0.pkl", "rb" ))
#train_images2 = pickle.load(open("raw_images_1.pkl", "rb" ))
#train_images3 = pickle.load(open("raw_images_2.pkl", "rb" ))
#print(len(train_images1),len(train_images2),len(train_images3))
#
#
## In[ ]:
#
#
#cv2.imshow("Example train image",train_images[0])
#
#cv2.waitKey(0) 
#cv2.destroyAllWindows()


# In[ ]:




