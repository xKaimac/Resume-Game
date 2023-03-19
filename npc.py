from gameObject import GameObject
import random


class Npc(GameObject):
    def __init__(self, x, y, width, height, image_path, speed, path_length, x_direction, y_direction, dialogue, number, left_edge_x, top_edge_y):
        super().__init__(x,y,width,height, image_path)
        self.image = image_path
        self.speed = speed
        self.path_forward_counter = 0
        self.path_backward_counter = 0
        self.x_direction = x_direction
        self.y_direction = y_direction
        self.path_length = path_length
        self.dialogue = dialogue
        self.object_collision = False
        self.player_collision = False
        self.action = 0
        self.number = number
        self.left_edge_x = left_edge_x
        self.top_edge_y = top_edge_y

    def boundaries(self, max_height, max_width):
        #top and bottom boundaries
        if (self.y >= (max_height-self.height) and self.y_direction > 0) or (self.y <= self.top_edge_y and self.y_direction < 0):
            self.y_direction *= -1
            return True
        #left and right boundaries
        if (self.x >= (max_width-self.width) and self.x_direction > 0) or (self.x <= self.left_edge_x and self.x_direction < 0):
            self.y_direction *= -1
            return True

    def set_action(self):
        if self.y_direction == -1:
            self.action = 1
        elif self.y_direction == 1:
            self.action = 0
        elif self.x_direction == 1:
            self.action = 3
        elif self.x_direction == -1:
            self.action = 2

    #turns the ncp around on collision with object, 
    #   stops the npc in collision with player
    def collision(self):
        if self.object_collision:
            self.x_direction = random.randint(-1,1)
            self.y_direction = random.randint(-1,1)
            self.object_collision = False
        elif self.player_collision:
            self.y_direction = 0
            self.x_direction = 0


    #movement method
    def move (self, max_height, max_width):

        self.collision()
        if self.player_collision:
            self.x_direction = 0
            self.y_direction = 0
        elif (self.path_forward_counter >= self.path_length) or self.boundaries(max_height, max_width):
            self.x_direction = random.randint(-1,1)
            self.y_direction = random.randint(-1,1)
            self.set_action()
            self.path_forward_counter = 0
        else:
            self.path_forward_counter += .025
        self.x += self.x_direction*self.speed
        self.y += self.y_direction*self.speed

    #changes animation image        
    def change_image(self, image):
        self.image = image