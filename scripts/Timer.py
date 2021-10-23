import pygame
from pygame.locals import *

class Timer:
    def __init__(self):
        self.first=True
        self.start=pygame.time.get_ticks()
    def reset(self):
        self.first=True
    def stand_by(self,t):#[ms]
        if self.first:
            self.start=pygame.time.get_ticks()
            self.first=False
        else:
            if (pygame.time.get_ticks()-self.start)>=t:
                self.first=True
                return True
        return False