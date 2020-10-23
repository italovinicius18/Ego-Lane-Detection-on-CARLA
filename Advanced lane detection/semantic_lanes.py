import glob
import os
import sys
try:
    sys.path.append(glob.glob('../../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla

from line_fit_video import annotate_image

import random
import time
import numpy as np
import cv2
from PIL import Image

IM_WIDTH = 1280
IM_HEIGHT = 720
i = 0

def write_ground_truth(image):
    cc = carla.ColorConverter.CityScapesPalette
    image.convert(cc)
    
    image_array = image.raw_data
    image_array = np.array(image_array).reshape((image.height,image.width,4))
    image_array = image_array[:, :, :3]

    converted = np.where(image_array == 157, 234, 50)
    converted[np.where((converted!=[157, 234, 50]).all(axis=2))] = [255,255,255]
    converted[np.where((converted==[50, 50, 50]).all(axis=2))] = [0,0,0]
    image_filtered = converted.astype('uint8')

    cv2.imwrite(f'./unwarped/{image.frame}.jpg', image_filtered)
    print(f'./unwarped/{image.frame}.jpg saved')

    try:
        annotate_image(image_filtered,image.frame)
    except NoneType:
        raise NoneType

    print(len(os.listdir('./warped/')))

    if (len(os.listdir('./warped/')) >= 5000):
        exit(0)

actor_list = []
try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    bp = blueprint_library.filter('model3')[0]
    print(bp)

    spawn_point = random.choice(world.get_map().get_spawn_points())

    vehicle = world.spawn_actor(bp, spawn_point)

    vehicle.set_autopilot(True)
    actor_list.append(vehicle)

    blueprint_semantic = blueprint_library.find('sensor.camera.semantic_segmentation')
    blueprint_semantic.set_attribute('image_size_x', f'{IM_WIDTH}')
    blueprint_semantic.set_attribute('image_size_y', f'{IM_HEIGHT}')

    spawn_point_semantic = carla.Transform(carla.Location(x=2.0, y=0.0, z=1.8))
    sensor_semantic = world.spawn_actor(blueprint_semantic, spawn_point_semantic, attach_to=vehicle)

    actor_list.append(sensor_semantic)

    blueprint_rgb = blueprint_library.find('sensor.camera.rgb')
    blueprint_rgb.set_attribute('image_size_x', f'{IM_WIDTH}')
    blueprint_rgb.set_attribute('image_size_y', f'{IM_HEIGHT}')

    spawn_point_rgb = carla.Transform(carla.Location(x=2.0, y=0.0, z=1.8))
    sensor_rgb = world.spawn_actor(blueprint_rgb, spawn_point_rgb, attach_to=vehicle)

    actor_list.append(sensor_rgb)

    #Maybe we cant generate the ground truth, so wont save this image

    sensor_semantic.listen(lambda image: write_ground_truth(image))
    sensor_rgb.listen(lambda image: image.save_to_disk('raw/%06d.png' % image.frame))

    time.sleep(3000)

finally:
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')