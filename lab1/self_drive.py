import sys
import numpy as np
import math
import matplotlib.pyplot as plt
from picar_4wd.pwm import PWM
from picar_4wd.pin import Pin
from picar_4wd.servo import Servo
from picar_4wd.ultrasonic import Ultrasonic 
from picar_4wd.filedb import FileDB  
from picar_4wd.utils import *
import picar_4wd as fc
import time

config = FileDB("config")
left_front_reverse = config.get('left_front_reverse', default_value = False)
right_front_reverse = config.get('right_front_reverse', default_value = False)
left_rear_reverse = config.get('left_rear_reverse', default_value = False)
right_rear_reverse = config.get('right_rear_reverse', default_value = False)    
ultrasonic_servo_offset = int(config.get('ultrasonic_servo_offset', default_value = 0)) 

us = Ultrasonic(Pin('D8'), Pin('D9'))
servo = Servo(PWM("P0"), offset=ultrasonic_servo_offset)

side_length = 100
RES = 15

from pathsolver import PathSolver

class AutoPilot(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = np.zeros((self.height, self.width), dtype=np.uint8)

        self.cur_x = (side_length // 2)
        self.cur_y = (side_length // 2)

        # counter-clockwise is positive
        self.cur_theta = 0
    
    def get_position(self):
        return (self.cur_x, self.cur_y, self.cur_theta)
        
    def scan_surrounding(self):
        dis = []
        for angle in range(-60, 60, 10):
            servo.set_angle(angle)
            time.sleep(0.3)
            distance = us.get_distance()
            print(distance)
            # Observations that are too far are tossed
            if distance != -2 and distance < 50:
                dis.append((angle, distance))

        return dis

    def set_obstacle(self, obs):
        radians = np.deg2rad(obs[0]) + np.deg2rad(self.cur_theta)
        x = round(obs[1] * np.sin(radians) / RES)
        y = round(obs[1] * np.cos(radians) / RES)

        x = x + self.cur_x
        y = y + self.cur_y

        EPS = 2
        for t_y in range(y - EPS, y + EPS + 1):
            for t_x in range(x - EPS, x + EPS + 1):
                if 0 <= t_x < side_length and 0 <= t_y < side_length:
                    self.map[y][x] = 1
    
    def set_surrounding(self):
        obstacles = self.scan_surrounding()
        for obs in obstacles:
            self.set_obstacle(obs)
    
    def get_map(self):
        return self.map
    
    def forward(self):
        # Move 15 cm forward
        fc.forward(20)
        time.sleep(0.5)
        fc.stop()
        
        x_increment = round(15 * np.sin(np.deg2rad(self.cur_theta)) / RES)
        y_increment = round(15 * np.cos(np.deg2rad(self.cur_theta)) / RES)

        self.cur_x += x_increment
        self.cur_y += y_increment

        time.sleep(0.4)

    def backward(self):
        # Move 15 cm backward
        fc.backward(20)
        time.sleep(0.5)
        fc.stop()

        x_increment = round(15 * np.sin(np.deg2rad(self.cur_theta)) / RES)
        y_increment = round(15 * np.cos(np.deg2rad(self.cur_theta)) / RES)

        self.cur_x -= x_increment
        self.cur_y -= y_increment

        time.sleep(0.4)
    
    def turn_right(self):
        # turn right for 90 degrees
        fc.turn_right(20)
        time.sleep(1.325)
        fc.stop()

        self.cur_theta -= 90
        self.cur_theta = self.cur_theta % 360

        time.sleep(0.4)
    
    def turn_left(self):
        # turn left for 90 degrees
        fc.turn_left(20)
        time.sleep(1.325)
        fc.stop()

        self.cur_theta += 90
        self.cur_theta = self.cur_theta % 360

        time.sleep(0.4)
    
    def get_map_viz(self):
        ret = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        ret[self.map == 1] = (255, 0, 0) # RED for obstacle
        ret[self.map == 2] = (0, 255, 0) # GREEN for car
        return ret
    
    def get_map_viz_with_path(self, path):
        viz = self.get_map_viz()
        for i in range(len(path) - 1):
            x, y = path[i]
            viz[y, x] = (0, 0, 255) # BLUE for path
        return viz

    def get_path(self, start, goal):
        solver = PathSolver(self.map)
        return solver.solve_for_path(start, goal)
import cv2
if __name__ == '__main__':
    my_pilot = AutoPilot(side_length, side_length)

    # 30, 95
    goal = (side_length // 2 - 100 // RES, side_length // 2 + 225 // RES)

    for i in range(100):
        my_pilot.set_surrounding()
        cur_x, cur_y, cur_theta = my_pilot.get_position()
        if abs(cur_x - goal[0]) < 1 and abs(cur_y - goal[1]) < 1:
            break
        # navigate forward
        path = my_pilot.get_path((cur_x, cur_y), goal)

        cur_pos, next_pos = path[0], path[1]

        # Get target theta
        if next_pos[0] > cur_pos[0]:
            target_theta = 90
            assert next_pos[1] == cur_pos[1]
        elif next_pos[0] < cur_pos[0]:
            target_theta = 270
            assert next_pos[1] == cur_pos[1]
        elif next_pos[1] > cur_pos[1]:
            target_theta = 0
            assert next_pos[0] == cur_pos[0]
        elif next_pos[1] < cur_pos[1]:
            target_theta = 180
            assert next_pos[0] == cur_pos[0]
        else:
            raise Exception("Invalid path")
        
        # Turn if necessary
        if cur_theta != target_theta:
            print(path[:2])
            print(f"tar: {target_theta} cur: {cur_theta}")
            if (target_theta - cur_theta) % 360 == 90:
                my_pilot.turn_left()
            elif (target_theta - cur_theta) % 360 == 270:
                my_pilot.turn_right()
            else:
                my_pilot.turn_right()
                my_pilot.turn_right()
        
        # Move forward
        my_pilot.forward()

        cur_x, cur_y, cur_theta = my_pilot.get_position()
        print(f"x: {cur_x} y: {cur_y} t: {cur_theta}")
        assert (cur_x, cur_y) == next_pos

        viz_map = my_pilot.get_map_viz_with_path(path)
        cv2.imshow('viz', viz_map)
        cv2.waitKey(1)

    # for i in range(5):
    #     my_pilot.forward()
    #     my_pilot.set_surrounding()

    # viz_map = my_pilot.get_map_viz()
    #plt.imshow(viz_map)
    #plt.show()
