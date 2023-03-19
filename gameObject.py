import pygame


class GameObject:
    def __init__(self, x, y, width, height, image_path):
        image = image_path
        self.image = pygame.transform.scale(image,(width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def change_image(self, image):
        self.image = pygame.transform.scale(image,(self.width, self.height))
    
