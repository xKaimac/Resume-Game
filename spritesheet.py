import pygame

class Spritesheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame_x, frame_y, width, height, scale, colour):
        self.image = pygame.Surface((width,height)).convert_alpha()
        self.image.blit(self.sheet, (0,0), (frame_x*width, frame_y*height, width, height))
        self.image = pygame.transform.scale(self.image, (width*scale, height*scale))
        self.image.set_colorkey(colour)

        return self.image    