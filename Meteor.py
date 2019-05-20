import pygame
from pygame.color import Color
from pygame.sprite import Sprite
from pygame.surface import Surface

class METEOR(Sprite):
    def __init__(self):
        Sprite.__init__(self)

        self.sprite_image = 'Meteor.png'
        self.speed = 8
        self.HP = 1
        self.sprite_width = 34
        self.sprite_height = 36
        self.sprite_sheet = pygame.image.load(
                                self.sprite_image).convert()
        self.sprite_columns = 30    # 기둥이 몇 게인지
        self.current_frame = 0
        self.image = Surface((self.sprite_width, self.sprite_height))

        rect = (self.sprite_width*self.current_frame, 0, 
                self.sprite_width, self.sprite_height)
        self.image.blit( self.sprite_sheet, (0, 0), rect)
        self.image.set_colorkey(Color(255, 201, 14))
        self.rect = self.image.get_rect()
       
    def update(self):
        if self.current_frame == self.sprite_columns - 1:
            self.current_frame = 0
        else:
            self.current_frame += 1

        rect = (self.sprite_width*self.current_frame, 0, 
                self.sprite_width, self.sprite_height)
        self.image.blit( self.sprite_sheet, (0, 0), rect)