import numpy as np
import cv2
from PIL import Image
from tensorflow.keras.models import load_model


# Class to average lanes with
class Lanes():
    def __init__(self):
        self.recent_fit = []
        self.avg_fit = []


def road_lines(image,name):

    # Get image ready for feeding into model
    
    small_img = cv2.resize(image, (160, 80))
    small_img = np.array(small_img)
    small_img = small_img[None,:,:,:]
    
    # Make prediction with neural network (un-normalize value by multiplying by 255)
    #prediction = model.predict(small_img)[0] * 255
    prediction = model.predict(small_img)[0]

    # Add lane prediction to list for averaging
    lanes.recent_fit.append(prediction)
    # Only using last five for average
    if len(lanes.recent_fit) > 5:
        lanes.recent_fit = lanes.recent_fit[1:]

    # Calculate average detection
    lanes.avg_fit = np.mean(np.array([i for i in lanes.recent_fit]), axis = 0)
    
    # Re-size to match the original image
    lane_image = cv2.resize(lanes.avg_fit, (1280, 720))

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)

    
    lane = Image.fromarray(lane_image)
    lane = lane.convert("RGB")

    # Merge the lane drawing onto the original image

    result = Image.blend(image, lane, alpha=.3)

    result.save(f'compose/{name}.jpg')
    lane.save(f'predicted/{name}.jpg')


# Load Keras model
model = load_model('full_CNN_model.h5')
# Create lanes object
lanes = Lanes()