from gameObject import GameObject
from spritesheet import Spritesheet
import pygame
import movement

class Player(GameObject):

    
    def __init__(self, x, y, width, height, image_path, dialogue, speed, left_edge_x, top_edge_y):
        super().__init__(x,y,width,height, image_path)
        self.image = image_path
        self.speed = speed
        self.dialogue = dialogue
        self.sprite_sheet = sprite_sheet = Spritesheet(pygame.image.load('assets/charsprites.png').convert_alpha())
        self.scale =  2
        self.x_direction = 0
        self.y_direction = 0
        self.left_edge_x = left_edge_x
        self.top_edge_y = top_edge_y
        self.object_collision = False
        self.object_collided_with = 0
        self.animation_list = [
            [
            sprite_sheet.get_image(0, 0, 16, 20, self.scale, (0,0,0)), #walking down 1
            sprite_sheet.get_image(1, 0, 16, 20, self.scale, (0,0,0)), #idle down
            sprite_sheet.get_image(2, 0, 16, 20, self.scale, (0,0,0)) #walking down 2
            ],
            [   
            sprite_sheet.get_image(0, 3, 16, 20, self.scale, (0,0,0)), #Walking up 1
            sprite_sheet.get_image(1, 3, 16, 20, self.scale, (0,0,0)), #idle up
            sprite_sheet.get_image(2, 3, 16, 20, self.scale, (0,0,0)) #walking up 2
            ],
            [
            sprite_sheet.get_image(0, 1, 16, 20, self.scale, (0,0,0)), #Walking left 1
            sprite_sheet.get_image(1, 1, 16, 20, self.scale, (0,0,0)), #idle left
            sprite_sheet.get_image(2, 1, 16, 20, self.scale, (0,0,0)) #walking left 2
            ],
            [
            sprite_sheet.get_image(0, 2, 16, 20, self.scale, (0,0,0)), #Walking right 1
            sprite_sheet.get_image(1, 2, 16, 20, self.scale, (0,0,0)), #idle right
            sprite_sheet.get_image(2, 2, 16, 20, self.scale, (0,0,0)) #walking right 2
            ]
        ]


    def move (self, y_direction, x_direction, max_height, max_width):
        if (self.y >= (max_height-self.height) and y_direction > 0) or (self.y <= self.top_edge_y and y_direction < 0):
            return
        if (self.x >= (max_width-self.width) and x_direction > 0) or (self.x <= self.left_edge_x and x_direction < 0):
            return
        if self.object_collision == True:
            print(f"colliding with: {self.object_collided_with}, {self.object_collision}")
            if self.y_direction == movement.Direction.UP:
                self.y = self.object_collided_with.y + self.object_collided_with.height
            elif self.y_direction == movement.Direction.DOWN:
                self.y = self.object_collided_with.y - self.height
            elif self.x_direction == movement.Direction.RIGHT:
                self.x = self.object_collided_with.x - self.width
            elif self.x_direction == movement.Direction.LEFT:
                self.x = self.object_collided_with.x
            self.object_collision = False
            print(f"colliding with: {self.object_collided_with}, {self.object_collision}")
            return
        self.y += (y_direction*self.speed)
        self.x += (x_direction*self.speed)

    def change_image(self, image):
        self.image = image
    
    def collide(self, building):
        self.object_collided_with = building