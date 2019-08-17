from math import pi, sin, cos
from typing import List, Tuple
import pygame
from pyngine import Controller, Interface, Drawer, Event

class FController(Controller):

    MOVE_F = 1
    MOVE_B = -1
    MOVE_R = 1
    MOVE_L = -1

    def __init__(self, text, resolution):
        Controller.__init__(self, Interface(text, resolution), debug=True)

        # player position
        #self.mouse.locked = True
        self.px = 8
        self.py = 8
        self.pa = 0
        self.fov = pi / 3
        self.walk_step = 5
        self.rot_r = 2.0
        self.rot_l = -self.rot_r
        self.map = [
            '################',
            '#..............#',
            '#...........#..#',
            '#....##........#',
            '#..........##..#',
            '#..............#',
            '#..............#',
            '#..............#',
            '#..............#',
            '#..............#',
            '#..............#',
            '#.....###..#####',
            '#..............#',
            '#........##....#',
            '#..............#',
            '################',
        ]
        self.map_width = 16
        self.map_height = 16
        self.wall_char = '#'
        self.depth = 16
        self.cast_step = 0.1
        self.pixel_width = 10

        #Drawer(self, refresh=self.mouse_rotate)
        Drawer(self, refresh=self.floor)
        Drawer(self, refresh=self.walls)

        Event(self, action=self.rotate, args=(self.rot_l), keys=(pygame.K_LEFT))
        Event(self, action=self.rotate, args=(self.rot_r), keys=(pygame.K_RIGHT))
        Event(self, action=self.move, args=(FController.MOVE_F, 0, self.walk_step), keys=(pygame.K_w))
        Event(self, action=self.move, args=(FController.MOVE_B, 0, self.walk_step), keys=(pygame.K_s))
        Event(self, action=self.move, args=(1, FController.MOVE_R, self.walk_step), keys=(pygame.K_d))
        Event(self, action=self.move, args=(1, FController.MOVE_L, self.walk_step), keys=(pygame.K_a))

    def floor(self):
        self.painter.fill_area(
            0,
            self.screen_height / 2,
            self.screen_width,
            self.screen_height / 2,
            color=(150, 150, 150)
        )

    def walls(self):

        # calculate ray angle for each column on screen
        for x in range(int(self.screen_width / self.pixel_width) + self.pixel_width):
            ray_angle: float = (self.pa - self.fov / 2) + (x * self.pixel_width / self.screen_width) * self.fov
            distance_to_wall: float = 0
            hit_wall: bool = False

            eye_x = sin(ray_angle)
            eye_y = cos(ray_angle)

            while not hit_wall and distance_to_wall < self.depth:
                distance_to_wall += self.cast_step
                test_x = int(self.px + eye_x * distance_to_wall)
                test_y = int(self.py + eye_y * distance_to_wall)

                # ray is out of bounds
                if (test_x < 0 or test_x >= self.map_width or test_y < 0 or test_y >= self.map_height):
                    distance_to_wall = self.depth
                    hit_wall = True
                # ray is in bounds
                else:
                    # cell is a wall
                    if self.map[test_y][test_x] == self.wall_char:
                        hit_wall = True
                    # cell is something else
                    else:
                        pass

            ceiling = self.screen_height / 2 - self.screen_height / distance_to_wall
            floor = self.screen_height - ceiling
            s = max(min(int((distance_to_wall ** -1) * 255 * 3), 255), 0)
            shade = (s, s, s)

            # draw walls
            self.painter.fill_area(
                x * self.pixel_width,
                ceiling,
                self.pixel_width,
                floor - ceiling,
                shade
            )

    def mouse_rotate(self):
        self.pa += self.mouse.yaw * self.delta_time

    def rotate(self, amount: float):
        self.pa += amount * self.delta_time

    def move(self, direction: int, strafe: int, step: float):
        """@brief Move the player forward, backward, left, or right. \\
        @param direction Direction to move:
            1: forward or to strafe
           -1: backward
        @param strafe Move left or right, ensure direction == 1:
            1: right
           -1: left
            0: neither left nor right
        @param step The size of a step to take that frame.
        """
        # take a step in the given direction
        self.px += float(direction * sin(self.pa + strafe * pi / 2) * step * self.delta_time)
        self.py += float(direction * cos(self.pa + strafe * pi / 2) * step * self.delta_time)

        # collision detection
        if self.map[int(self.py)][int(self.px)] == self.wall_char:
            # correct for direction
            if not strafe == 0: direction = -1
            self.px -= float(direction * sin(self.pa - strafe * pi / 2) * step * self.delta_time)
            self.py -= float(direction * cos(self.pa - strafe * pi / 2) * step * self.delta_time)
