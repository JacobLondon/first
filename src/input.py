import pygame
from pyngine import Event, Drawer
from .render import Renderer

class Input(Renderer):
    def __init__(self, args):
        Renderer.__init__(self, *args)
        
        # mouse
        self.mouse.locked = True
        self.mouse.set_visible(False)
        self.mouse.sensitivity = .8
        self.mouse.cutoff = .5
        self.mouse.unit_step = 2
        self.mouse.smoothing = .75

        Drawer(self, refresh=self.mouse_rotate)
        Event(self, action=self.exit_program, keys=(pygame.K_ESCAPE))

    def mouse_rotate(self):
        self.pa += self.mouse.dx * self.delta_time
