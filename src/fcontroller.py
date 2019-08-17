from math import pi, sin, cos
from typing import List, Tuple
import pygame
from pyngine import Controller, Interface, Drawer, Event

class FController(Controller):
    ROT_R = 1.5
    ROT_L = -1.5
    MOVE_F = 1
    MOVE_B = -1
    MOVE_R = 1
    MOVE_L = -1
    def __init__(self, text, resolution):
        Controller.__init__(self, Interface(text, resolution), debug=True)

        # player position
        self.px = 8
        self.py = 8
        self.pa = 0
        self.fov = pi / 3
        self.map = [
            '################',
            '#..............#',
            '#...........#..#',
            '#..............#',
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
        self.pixel_width = 5

        Drawer(self, refresh=self.floor)
        Drawer(self, refresh=self.walls)

        Event(self, action=self.rotate, args=(FController.ROT_L), keys=(pygame.K_LEFT))
        Event(self, action=self.rotate, args=(FController.ROT_R), keys=(pygame.K_RIGHT))
        Event(self, action=self.move, args=(FController.MOVE_F, 0), keys=(pygame.K_w))
        Event(self, action=self.move, args=(FController.MOVE_B, 0), keys=(pygame.K_s))
        Event(self, action=self.move, args=(1, FController.MOVE_R), keys=(pygame.K_d))
        Event(self, action=self.move, args=(1, FController.MOVE_L), keys=(pygame.K_a))

    def floor(self):
        self.painter.fill_area(0, self.screen_height / 2, self.screen_width, self.screen_height / 2, color=(150, 150, 150))

    def walls(self):

        # calculate ray angle for each column on screen
        for x in range(int(self.screen_width / self.pixel_width) + self.pixel_width):
            ray_angle: float = (self.pa - self.fov / 2) + (x * self.pixel_width / self.screen_width) * self.fov
            distance_to_wall: float = 0
            hit_wall: bool = False

            eye_x = sin(ray_angle)
            eye_y = cos(ray_angle)

            while not hit_wall and distance_to_wall < self.depth:
                distance_to_wall += 0.1
                test_x = int(self.px + eye_x * distance_to_wall)
                test_y = int(self.py + eye_y * distance_to_wall)

                # test if ray is out of bounds
                if (test_x < 0 or test_x >= self.map_width
                    or test_y < 0 or test_y >= self.map_height):
                    hit_wall = True
                    distance_to_wall = self.depth
                else:
                    # ray is in bounds, see if cell is a wall
                    if self.map[test_y][test_x] == self.wall_char:
                        hit_wall = True

            ceiling = int(self.screen_height / 2) - self.screen_height / distance_to_wall
            floor = self.screen_height - ceiling
            s = max(min(int((distance_to_wall ** -1) * 255 * 3), 255), 0)
            shade = (s, s, s)

            # draw walls
            self.painter.fill_area(x * self.pixel_width, ceiling, self.pixel_width, floor - ceiling, shade)

    def rotate(self, amount: float):
        self.pa += amount * self.delta_time

    def move(self, direction: int, strafe: int):
        self.px += float(direction * sin(self.pa + strafe * pi / 2) * 5 * self.delta_time)
        self.py += float(direction * cos(self.pa + strafe * pi / 2) * 5 * self.delta_time)
        # forward collision detection
        if self.map[int(self.py)][int(self.px)] == self.wall_char:
            if not strafe == 0: direction = -1
            self.px -= float(direction * sin(self.pa - strafe * pi / 2) * 5 * self.delta_time)
            self.py -= float(direction * cos(self.pa - strafe * pi / 2) * 5 * self.delta_time)
