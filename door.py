import pygame
from gameObject import GameObject
from dialogue import Dialogue

class Door(GameObject):

    def __init__(self, x, y, width, height, image_path, dialogue):
        super().__init__(x,y,width,height, image_path)
        self.dialogue = dialogue
        self.image = pygame.transform.scale(image_path,(width, height))