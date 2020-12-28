# Ego Lane Detection on CARLA

The first thing I did it was find a method to generate the ground truth in CARLA, i searched a lot o f methods like:

-	LaneNet
-	Robust lane detection

## Generating data

These approaches above use deep learning methods, but the easier method it was use computer vision to do this task, so I discovered a method which do this and I used this code to generate data in CARLA, the code is the Advanced lane detection folder and is a project of Jou-ching (George) Sung and this is the [repo](https://github.com/georgesung/advanced_lane_detection) and I create python script to apply the CV on carla images and store the raw rgb data and the predict data of the ego-lane which is semantic_lines.py, the reason of this name it's because I'm applying the CV on a semantic image which is focused just on the lanes of the road

## Manipulating data

After generating the data with sematic_lines.py I applied some manipulations and data augmentation on those images:

- Verified if the raw image or the predict exists and if their correspondent didn't exists I deleted this image
- Convert all PNG images to JPG
- Increased the amount of data
- Manipulated the images in two aspects:
  - Rotating randomly picking a sample from angles = [5,8,10] and neg_angles = [-5,-8,-10] 
  - Flipping Horizontally
- After these changes I resize the images to 160x80, because it will be better to run this model in this size for a faster training
- So added the images to a list and saved them as images.pkl and labels.pkl, you can found them [here](https://drive.google.com/drive/folders/13bG68L4Y0-BBRJqPy-lvhtfSOrdDkg3T?usp=sharing) 

## Training

I took the model from this [repo](https://github.com/mvirgo/MLND-Capstone) and made some changes to upgrade to a new version of tensorflow and Keras, the first results of the models it was strange, because the model wasn't predicting the lanes, so I didn't do the normalization and I trained again and now the model are OK and you can found [here](https://drive.google.com/drive/folders/13bG68L4Y0-BBRJqPy-lvhtfSOrdDkg3T?usp=sharing) or in this repo.

The result isn't the best because i think the model is overfitting, you can see the loss function and the accuracy here, but, to my mind I need to improve this results, my friends and I have some ideas to do this, like:

- Increase the dataset
- Change the number of batches
- Re-made the model and some hyperparameters

That's the reason I won't put the images here, because it's just a test and I want to Improve

## Apply on CARLA

This one it was the hardest part, because i was having problems to merge the raw image and the model prediction because they have different types of images, no shapes, but Mat types
I am getting the images with a rgb sensor and generate the predict with the model already trained, in my first tries i was using addWeighted() from cv2 to merge these two images, but it was a bad idea, because the output of the model have a different shape of the input and I was making some manipulations to fit them, and wasn't working. So I used Image from PIL to do this task and this the result running the script Analyzing_lane.py inside CARLA

- Raw image
![Raw Image](https://github.com/italovinicius18/Ego-Lane-Detection-on-CARLA/blob/main/Carla%20FCN/raw/22312.jpg)
- Lane predict
![Predict](https://github.com/italovinicius18/Ego-Lane-Detection-on-CARLA/blob/main/Carla%20FCN/predicted/22312.jpg)
- Composed image
![Blend images](https://github.com/italovinicius18/Ego-Lane-Detection-on-CARLA/blob/main/Carla%20FCN/compose/22312.jpg)

If you want to run this model in you computer use [this](https://github.com/italovinicius18/Ego-Lane-Detection-on-CARLA/blob/main/environment.yml) environment on conda
