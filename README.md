# Ego Lane Detection on CARLA

The first thing I did it was find a method to generate the ground truth in CARLA, i searched a lot o f methods like:

-	LaneNet
-	Robust lane detection

These approaches above use deep learning methods, but the easier method it was use computer vision to do this task, so I discovered a method which do this and I used this code to generate data in CARLA, the code is the Advanced lane detection folder and is a project of Jou-ching (George) Sung and this is the [repo](https://github.com/georgesung/advanced_lane_detection) and I create python script to apply the CV on carla images and store the raw rgb data and the predict data of the ego-lane which is semantic_lines.py, the reason of this name it's because I'm applying the CV on a semantic image which is focused just on the lanes of the road

After generating the data, I made a folder which I and manipulate the data and fixing wrong predicts, after that i create a notebook to increase the number of samples, so i flipped horizontally the images and rotate then in a random angle, which was one of [5,8,10] and [-5,-8,-10]

Now i'm gonna resize and store this data in a pickle file.