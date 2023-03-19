import pygame
from gameObject import GameObject

class Dialogue(GameObject):

    def __init__(self, text, image, text_x, text_y, width, height):
        self.text = text
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image,(self.width, self.height))
        self.x = 40
        self.y = 420
        self.text_x = text_x
        self.text_y = text_y

    def change_text(self, text):
        self.text = text

        

    