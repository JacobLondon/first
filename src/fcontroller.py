from math import pi, sin, cos
from typing import List, Tuple
import pygame
from pyngine import Controller, Interface, Drawer, Event

class FController(Controller):
    def __init__(self, text, resolution):
        Controller.__init__(self, Interface(text, resolution), debug=True)

        # player position
        self.px = 8
        self.py = 8
        self.pa = 0
        self.fov = pi / 4
        self.map = [
            '################',
            '#..............#',
            '#..............#',
            '#..............#',
            '#..............#',
            '#..............#',
            '#..............#',
            '#..............#',
            '#..............#',
            '#..............#',
            '#..............#',
            '#..........#####',
            '#..............#',
            '#..............#',
            '#..............#',
            '################',
        ]
        self.map_width = 16
        self.map_height = 16
        self.depth = 16
        self.pixel_width = 25
        
        Drawer(self, refresh=(self.walls))

        def keyl():
            self.pa -= 0.8 * self.delta_time
        def keyr():
            self.pa += 0.8 * self.delta_time
        def keyw():
            self.px += sin(self.pa) * 5 * self.delta_time
            self.py += cos(self.pa) * 5 * self.delta_time
            # forward collision detection
            if self.map[int(self.py)][int(self.px)] == '#':
                self.px -= sin(self.pa) * 5 * self.delta_time
                self.py -= cos(self.pa) * 5 * self.delta_time
        def keys():
            self.px -= sin(self.pa) * 5 * self.delta_time
            self.py -= cos(self.pa) * 5 * self.delta_time
            # backward collision detection
            if self.map[int(self.py)][int(self.px)] == '#':
                self.px += sin(self.pa) * 5 * self.delta_time
                self.py += cos(self.pa) * 5 * self.delta_time

        Event(self, action=keyl, keys=(pygame.K_LEFT,))
        Event(self, action=keyr, keys=(pygame.K_RIGHT,))
        Event(self, action=keyw, keys=(pygame.K_w,))
        Event(self, action=keys, keys=(pygame.K_s,))

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
                    if self.map[test_y][test_x] == '#':
                        hit_wall = True

            ceiling = int(self.screen_height / 2) - self.screen_height / distance_to_wall
            floor = self.screen_height - ceiling
            shade = (0, 0, 0)
            if distance_to_wall < self.depth / 4:
                shade = (255, 255, 255)
            elif distance_to_wall < self.depth / 3:
                shade = (200, 200, 200)
            elif distance_to_wall < self.depth / 2:
                shade = (100, 100, 100)
            elif distance_to_wall < self.depth:
                shade = (50, 50, 50)
            else:
                shade = (0, 0, 0)

            # draw the column
            for y in range(self.screen_height):
                if y < ceiling:
                    # must be roof
                    self.painter.fill_area(x * self.pixel_width, y, self.pixel_width, 1, (10, 10, 10))
                elif y > ceiling and y <= floor:
                    # must be wall
                    self.painter.fill_area(x * self.pixel_width, y, self.pixel_width, 1, shade)
                else:
                    # must be floor
                    self.painter.fill_area(x * self.pixel_width, y, self.pixel_width, 1, (150, 150, 150))
