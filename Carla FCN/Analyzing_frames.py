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

from Draw_detected_lanes import road_lines

import random
import time
import numpy as np
import cv2

IM_WIDTH = 1280
IM_HEIGHT = 720

def process_img(image,name):
    image_vect = image.raw_data
    image = np.array(image_vect)
    image = np.reshape(image,(IM_HEIGHT,IM_WIDTH,4))
    image = image[:,:,:3]
    road_lines(image,name)

    cv2.imwrite(f'./raw/{name}.jpg',image)

os.system('cls')
actor_list = []
light_weather = []
try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(3.0)

    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    bp = blueprint_library.filter('model3')[0]

    spawn_point = random.choice(world.get_map().get_spawn_points())

    vehicle = world.spawn_actor(bp, spawn_point)

    vehicle.set_autopilot(True)

    actor_list.append(vehicle)

    blueprint = blueprint_library.find('sensor.camera.rgb')

    blueprint.set_attribute('image_size_x', f'{IM_WIDTH}')
    blueprint.set_attribute('image_size_y', f'{IM_HEIGHT}')

    spawn_point = carla.Transform(carla.Location(x=2.0, y=0.0, z=1.8))
    sensor = world.spawn_actor(blueprint, spawn_point, attach_to=vehicle)

    actor_list.append(sensor)

    sensor.listen(lambda image: process_img(image,image.frame))

    # Set the max time running
    time.sleep(20)

finally:
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')