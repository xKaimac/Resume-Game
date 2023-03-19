import pygame
from movement import Direction
from movement import Movement
from player import Player
from npc import Npc
from spritesheet import Spritesheet
from gameObject import GameObject
from dialogue import Dialogue
from house import House
from door import Door
import asyncio

class Level:
    def __init__(self):

        #Window size
        self.width = 512
        self.height = 512

        #Creates game window
        self.game_window = pygame.display.set_mode((self.width,self.height))

        #clock and framerate settings
        self.clock = pygame.time.Clock()
        self.framerate = 60
        self.last_update = pygame.time.get_ticks()

        #Starting level
        self.state = 'village'

        #Font for text
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)

        #Scale for all characters
        self.player_scale = 2

        #Player settings
        self.action = 0
        self.animation_steps = 3
        self.animation_cooldown = 200 #milliseconds
        self.frame = 0
        self.counter = 0
        
        #holds x_y values when entering a building so that you spawn back at the door in the village
        self.previous_x = 0
        self.previous_y = 0
        self.previous_state = 0

        #Loads sprite sheet for characters
        self.sprite_sheet = Spritesheet(pygame.image.load('assets/charsprites.png').convert_alpha())
        self.sprite_sheet_aaron = Spritesheet(pygame.image.load('assets/aaron_welk.png').convert_alpha())
        self.sprite_sheet_shaun = Spritesheet(pygame.image.load('assets/Shaun_watson.png').convert_alpha())
        self.sprite_sheet_richard = Spritesheet(pygame.image.load('assets/richard_liebbrandt.png').convert_alpha())
        self.sprite_sheet_rach = Spritesheet(pygame.image.load('assets/rach.png').convert_alpha())
        
        #Sprite sheets for animals
        self.sprite_sheet_snickers = Spritesheet(pygame.image.load('assets/snickers.png').convert_alpha())
        self.sprite_sheet_chunks = Spritesheet(pygame.image.load('assets/chunks.png').convert_alpha())
        self.sprite_sheet_ranger = Spritesheet(pygame.image.load('assets/ranger.png').convert_alpha())
        
        #Font for text
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)

        #Non-character object creation
        #background
        self.background = GameObject(0,0,self.width,self.height,pygame.image.load('assets/32x32map.png'))

        ##BUILDINGS
        #Dialogue
        #Dialogue boxes and text 
        self.default_dialogue = Dialogue('',pygame.image.load('assets/Empty.png'),0,0,0,0)
        self.green_house_dialogue = Dialogue('Alistair\'s work', 
            pygame.image.load('assets/small_dialogue.png'),100,430,420,50)
        self.red_house_dialogue = Dialogue('Alistair\'s education', 
            pygame.image.load('assets/small_dialogue.png'),90,430,420,50)
        self.blue_house_dialogue = Dialogue('Alistair\'s home', 
            pygame.image.load('assets/small_dialogue.png'),70,430,420,50)
        self.rock_sign_dialogue = Dialogue('rock', 
            pygame.image.load('assets/small_dialogue.png'),70,430,420,50)
        self.door_dialogue = Dialogue("Press space to enter", 
            pygame.image.load('assets/small_dialogue.png'),70,430,420,50)
        self.exit_door_dialogue = Dialogue("Press space to exit", 
            pygame.image.load('assets/small_dialogue.png'),70,430,420,50)
        self.book_dialogue = Dialogue("Press space to read", 
            pygame.image.load('assets/small_dialogue.png'),70,430,420,50)
        self.computer_dialogue = Dialogue("Press space to use", 
            pygame.image.load('assets/small_dialogue.png'),70,430,420,50)
        self.table_dialogue = Dialogue("Press space to read", 
            pygame.image.load('assets/small_dialogue.png'),70,430,420,50)
        self.dialogue_option_check = 0 
        self.dialogue_option = self.green_house_dialogue
        self.text_surface = self.my_font.render(self.dialogue_option.text, False, (0,0,0))

        #Object creation
        #This one is just the overlay to move behind buildings
        self.buildings = GameObject(0,0,self.width,self.height,pygame.image.load('assets/buildings.png'))

        ##Village buildings
        #houses
        self.red_house = House(32,90,130,25,pygame.image.load('assets/treasure.png'), self.default_dialogue)
        self.blue_house = House(328,338,130,25,pygame.image.load('assets/treasure.png'), self.default_dialogue)
        self.green_house = House(44,320,100,25,pygame.image.load('assets/treasure.png'), self.default_dialogue)
        self.rect_list = [self.red_house, self.blue_house, self.green_house]

        #signs and rocks
        self.red_sign = House(45, 160, 10, 1,pygame.image.load('assets/treasure.png'),self.red_house_dialogue)
        self.blue_sign = House(341, 408, 10, 1,pygame.image.load('assets/treasure.png'),self.blue_house_dialogue)
        self.green_sign = House(110, 390, 10, 1,pygame.image.load('assets/treasure.png'),self.green_house_dialogue)
        self.rock_sign = House(405, 125, 10, 1,pygame.image.load('assets/treasure.png'),self.rock_sign_dialogue)

        #doors
        self.red_door = Door(100,120,5,1,pygame.image.load('assets/treasure.png'), self.door_dialogue)
        self.green_door = Door(80,347,5,1,pygame.image.load('assets/treasure.png'), self.door_dialogue)
        self.blue_door = Door(396,365,5,1,pygame.image.load('assets/treasure.png'), self.door_dialogue)
        #self.rock_door = Door()

        self.door_list = [self.red_door, self.green_door, self.blue_door]

        #default buildings are village (spawn)
        self.buildings_list = [self.red_house, self.blue_house, self.green_house,
            self.red_sign, self.blue_sign, self.green_sign, self.rock_sign,
            self.red_door, self.blue_door, self.green_door]
        self.village_building_list = [self.red_house, self.blue_house, self.green_house,
            self.red_sign, self.blue_sign, self.green_sign, self.rock_sign,
            self.red_door, self.blue_door, self.green_door]
        self.village_door_list = [self.red_door, self.blue_door, self.green_door]

        #School buildings
        self.school_door = Door(238,400,35,5,pygame.image.load('assets/treasure.png'), self.door_dialogue)
        self.left_table = House(180,300,5,5,pygame.image.load('assets/treasure.png'), self.default_dialogue)
        self.middle_table = House(250,300,5,5,pygame.image.load('assets/treasure.png'), self.default_dialogue)
        self.book = Door(320,300,5,5,pygame.image.load('assets/treasure.png'), self.book_dialogue)
        self.school_building_list = [self.school_door, self.left_table, self.middle_table, self.book]

        #home buildings
        self.home_door = Door(238,400,35,5,pygame.image.load('assets/treasure.png'), self.exit_door_dialogue)
        self.table = Door(250,230,115,10,pygame.image.load('assets/treasure.png'), self.table_dialogue)
        self.home_building_list = [self.home_door, self.table]

        #work buildings
        self.work_door = Door(238,409,20,5,pygame.image.load('assets/treasure.png'), self.exit_door_dialogue)
        self.computer = Door(350,348,40,5,pygame.image.load('assets/treasure.png'), self.computer_dialogue)
        self.boss_table = House(100,170,120,15,pygame.image.load('assets/treasure.png'), self.default_dialogue)
        self.money_stack = House(100,200,35,10,pygame.image.load('assets/treasure.png'), self.default_dialogue)
        self.my_table = House(310,315,100,35,pygame.image.load('assets/treasure.png'), self.default_dialogue)
        self.paper_stack = House(400,270,5,5,pygame.image.load('assets/treasure.png'), self.default_dialogue)
        self.work_building_list = [self.work_door, self.boss_table, self.money_stack, self.my_table, self.paper_stack, self.computer]

        #set scale for player size
        self.player_scale = 2
        self.black = (0,0,0)
        self.house_collision = ''

        ##NPC
        #Walk is [0, 2] in each sublist
        #Idle is [1] in each sublist
        #Actions are 0: walk down. 1: walk left. 2: walk up. 3: walk right
        self.npc_animation_lists = [[##Rach
            [
            self.sprite_sheet_rach.get_image(0, 0, 16, 20, self.player_scale, self.black), #walking down 1
            self.sprite_sheet_rach.get_image(1, 0, 16, 20, self.player_scale, self.black), #idle down
            self.sprite_sheet_rach.get_image(2, 0, 16, 20, self.player_scale, self.black) #walking down 2
            ],
            [   
            self.sprite_sheet_rach.get_image(0, 1, 16, 20, self.player_scale, self.black), #Walking up 1
            self.sprite_sheet_rach.get_image(1, 1, 16, 20, self.player_scale, self.black), #idle up
            self.sprite_sheet_rach.get_image(2, 1, 16, 20, self.player_scale, self.black) #walking up 2
            ],
            [
            self.sprite_sheet_rach.get_image(0, 2, 16, 20, self.player_scale, self.black), #Walking left 1
            self.sprite_sheet_rach.get_image(1, 2, 16, 20, self.player_scale, self.black), #idle left
            self.sprite_sheet_rach.get_image(2, 2, 16, 20, self.player_scale, self.black) #walking left 2
            ],
            [
            self.sprite_sheet_rach.get_image(0, 3, 16, 20, self.player_scale, self.black), #Walking right 1
            self.sprite_sheet_rach.get_image(1, 3, 16, 20, self.player_scale, self.black), #idle right
            self.sprite_sheet_rach.get_image(2, 3, 16, 20, self.player_scale, self.black) #walking right 2
            ]],
            [[##Placeholder
            self.sprite_sheet.get_image(6, 0, 16, 20, self.player_scale, self.black), #walking down 1
            self.sprite_sheet.get_image(7, 0, 16, 20, self.player_scale, self.black), #idle down
            self.sprite_sheet.get_image(8, 0, 16, 20, self.player_scale, self.black) #walking down 2
            ],
            [   
            self.sprite_sheet.get_image(6, 3, 16, 20, self.player_scale, self.black), #Walking up 1
            self.sprite_sheet.get_image(7, 3, 16, 20, self.player_scale, self.black), #idle up
            self.sprite_sheet.get_image(8, 3, 16, 20, self.player_scale, self.black) #walking up 2
            ],
            [
            self.sprite_sheet.get_image(6, 1, 16, 20, self.player_scale, self.black), #Walking left 1
            self.sprite_sheet.get_image(7, 1, 16, 20, self.player_scale, self.black), #idle left
            self.sprite_sheet.get_image(8, 1, 16, 20, self.player_scale, self.black) #walking left 2
            ],
            [
            self.sprite_sheet.get_image(6, 2, 16, 20, self.player_scale, self.black), #Walking right 1
            self.sprite_sheet.get_image(7, 2, 16, 20, self.player_scale, self.black), #idle right
            self.sprite_sheet.get_image(8, 2, 16, 20, self.player_scale, self.black) #walking right 2
            ]],
            [[##Aaron
            self.sprite_sheet_aaron.get_image(0, 0, 16, 20, self.player_scale, self.black), #walking down 1
            self.sprite_sheet_aaron.get_image(1, 0, 16, 20, self.player_scale, self.black), #idle down
            self.sprite_sheet_aaron.get_image(2, 0, 16, 20, self.player_scale, self.black) #walking down 2
            ],
            [   
            self.sprite_sheet_aaron.get_image(0, 1, 16, 20, self.player_scale, self.black), #Walking up 1
            self.sprite_sheet_aaron.get_image(1, 1, 16, 20, self.player_scale, self.black), #idle up
            self.sprite_sheet_aaron.get_image(2, 1, 16, 20, self.player_scale, self.black) #walking up 2
            ],
            [
            self.sprite_sheet_aaron.get_image(0, 2, 16, 20, self.player_scale, self.black), #Walking left 1
            self.sprite_sheet_aaron.get_image(1, 2, 16, 20, self.player_scale, self.black), #idle left
            self.sprite_sheet_aaron.get_image(2, 2, 16, 20, self.player_scale, self.black) #walking left 2
            ],
            [
            self.sprite_sheet_aaron.get_image(0, 3, 16, 20, self.player_scale, self.black), #Walking right 1
            self.sprite_sheet_aaron.get_image(1, 3, 16, 20, self.player_scale, self.black), #idle right
            self.sprite_sheet_aaron.get_image(2, 3, 16, 20, self.player_scale, self.black) #walking right 2
            ]],
            [[##Shaun
            self.sprite_sheet_shaun.get_image(0, 0, 16, 20, self.player_scale, self.black), #walking down 1
            self.sprite_sheet_shaun.get_image(1, 0, 16, 20, self.player_scale, self.black), #idle down
            self.sprite_sheet_shaun.get_image(2, 0, 16, 20, self.player_scale, self.black) #walking down 2
            ],
            [   
            self.sprite_sheet_shaun.get_image(0, 1, 16, 20, self.player_scale, self.black), #Walking up 1
            self.sprite_sheet_shaun.get_image(1, 1, 16, 20, self.player_scale, self.black), #idle up
            self.sprite_sheet_shaun.get_image(2, 1, 16, 20, self.player_scale, self.black) #walking up 2
            ],
            [
            self.sprite_sheet_shaun.get_image(0, 2, 16, 20, self.player_scale, self.black), #Walking left 1
            self.sprite_sheet_shaun.get_image(1, 2, 16, 20, self.player_scale, self.black), #idle left
            self.sprite_sheet_shaun.get_image(2, 2, 16, 20, self.player_scale, self.black) #walking left 2
            ],
            [
            self.sprite_sheet_shaun.get_image(0, 3, 16, 20, self.player_scale, self.black), #Walking right 1
            self.sprite_sheet_shaun.get_image(1, 3, 16, 20, self.player_scale, self.black), #idle right
            self.sprite_sheet_shaun.get_image(2, 3, 16, 20, self.player_scale, self.black) #walking right 2
            ]],
            [[#Richard
            self.sprite_sheet_richard.get_image(0, 0, 16, 20, self.player_scale, self.black), #walking down 1
            self.sprite_sheet_richard.get_image(1, 0, 16, 20, self.player_scale, self.black), #idle down
            self.sprite_sheet_richard.get_image(2, 0, 16, 20, self.player_scale, self.black) #walking down 2
            ],
            [   
            self.sprite_sheet_richard.get_image(0, 1, 16, 20, self.player_scale, self.black), #Walking up 1
            self.sprite_sheet_richard.get_image(1, 1, 16, 20, self.player_scale, self.black), #idle up
            self.sprite_sheet_richard.get_image(2, 1, 16, 20, self.player_scale, self.black) #walking up 2
            ],
            [
            self.sprite_sheet_richard.get_image(0, 2, 16, 20, self.player_scale, self.black), #Walking left 1
            self.sprite_sheet_richard.get_image(1, 2, 16, 20, self.player_scale, self.black), #idle left
            self.sprite_sheet_richard.get_image(2, 2, 16, 20, self.player_scale, self.black) #walking left 2
            ],
            [
            self.sprite_sheet_richard.get_image(0, 3, 16, 20, self.player_scale, self.black), #Walking right 1
            self.sprite_sheet_richard.get_image(1, 3, 16, 20, self.player_scale, self.black), #idle right
            self.sprite_sheet_richard.get_image(2, 3, 16, 20, self.player_scale, self.black) #walking right 2
            ]],
            [[#Snickers
            self.sprite_sheet_snickers.get_image(0, 0, 20, 16, self.player_scale, self.black), #walking down 1
            self.sprite_sheet_snickers.get_image(1, 0, 20, 16, self.player_scale, self.black), #idle down
            self.sprite_sheet_snickers.get_image(2, 0, 20, 16, self.player_scale, self.black) #walking down 2
            ],
            [   
            self.sprite_sheet_snickers.get_image(0, 1, 20, 16, self.player_scale, self.black), #Walking up 1
            self.sprite_sheet_snickers.get_image(1, 1, 20, 16, self.player_scale, self.black), #idle up
            self.sprite_sheet_snickers.get_image(2, 1, 20, 16, self.player_scale, self.black) #walking up 2
            ],
            [
            self.sprite_sheet_snickers.get_image(0, 2, 20, 16, self.player_scale, self.black), #Walking left 1
            self.sprite_sheet_snickers.get_image(1, 2, 20, 16, self.player_scale, self.black), #idle left
            self.sprite_sheet_snickers.get_image(2, 2, 20, 16, self.player_scale, self.black) #walking left 2
            ],
            [
            self.sprite_sheet_snickers.get_image(0, 3, 20, 16, self.player_scale, self.black), #Walking right 1
            self.sprite_sheet_snickers.get_image(1, 3, 20, 16, self.player_scale, self.black), #idle right
            self.sprite_sheet_snickers.get_image(2, 3, 20, 16, self.player_scale, self.black) #walking right 2
            ]],
            [[#Chunks
            self.sprite_sheet_chunks.get_image(0, 0, 20, 16, self.player_scale, self.black), #walking down 1
            self.sprite_sheet_chunks.get_image(1, 0, 20, 16, self.player_scale, self.black), #idle down
            self.sprite_sheet_chunks.get_image(2, 0, 20, 16, self.player_scale, self.black) #walking down 2
            ],
            [   
            self.sprite_sheet_chunks.get_image(0, 1, 20, 16, self.player_scale, self.black), #Walking up 1
            self.sprite_sheet_chunks.get_image(1, 1, 20, 16, self.player_scale, self.black), #idle up
            self.sprite_sheet_chunks.get_image(2, 1, 20, 16, self.player_scale, self.black) #walking up 2
            ],
            [
            self.sprite_sheet_chunks.get_image(0, 2, 20, 16, self.player_scale, self.black), #Walking left 1
            self.sprite_sheet_chunks.get_image(1, 2, 20, 16, self.player_scale, self.black), #idle left
            self.sprite_sheet_chunks.get_image(2, 2, 20, 16, self.player_scale, self.black) #walking left 2
            ],
            [
            self.sprite_sheet_chunks.get_image(0, 3, 20, 16, self.player_scale, self.black), #Walking right 1
            self.sprite_sheet_chunks.get_image(1, 3, 20, 16, self.player_scale, self.black), #idle right
            self.sprite_sheet_chunks.get_image(2, 3, 20, 16, self.player_scale, self.black) #walking right 2
            ]],
            [[#Ranger
            self.sprite_sheet_ranger.get_image(0, 0, 20, 16, self.player_scale, self.black), #walking down 1
            self.sprite_sheet_ranger.get_image(1, 0, 20, 16, self.player_scale, self.black), #idle down
            self.sprite_sheet_ranger.get_image(2, 0, 20, 16, self.player_scale, self.black) #walking down 2
            ],
            [   
            self.sprite_sheet_ranger.get_image(0, 1, 20, 16, self.player_scale, self.black), #Walking up 1
            self.sprite_sheet_ranger.get_image(1, 1, 20, 16, self.player_scale, self.black), #idle up
            self.sprite_sheet_ranger.get_image(2, 1, 20, 16, self.player_scale, self.black) #walking up 2
            ],
            [
            self.sprite_sheet_ranger.get_image(0, 2, 20, 16, self.player_scale, self.black), #Walking left 1
            self.sprite_sheet_ranger.get_image(1, 2, 20, 16, self.player_scale, self.black), #idle left
            self.sprite_sheet_ranger.get_image(2, 2, 20, 16, self.player_scale, self.black) #walking left 2
            ],
            [
            self.sprite_sheet_ranger.get_image(0, 3, 20, 16, self.player_scale, self.black), #Walking right 1
            self.sprite_sheet_ranger.get_image(1, 3, 20, 16, self.player_scale, self.black), #idle right
            self.sprite_sheet_ranger.get_image(2, 3, 20, 16, self.player_scale, self.black) #walking right 2
            ]]
        ]

        #NPC settings
        self.npc_collision = False

        #Create player object
        self.player = Player(233,400,16*self.player_scale,20*self.player_scale,
            self.sprite_sheet.get_image(1, 0, 16, 20, self.player_scale, (0,0,0)),self.height/200,2, 0, 50)

        #Create NPC objects
        #NPC dialogue
        self.npc_rach_dialogue = Dialogue("Alistair is the best!", 
            pygame.image.load('assets/small_dialogue.png'),70,430,420,50)
        self.npc_shaun_dialogue = Dialogue("Shaun, Senior Supervisor at FH", 
            pygame.image.load('assets/small_dialogue.png'),70,430,420,50)
        self.npc_aaron_dialogue = Dialogue("Aaron, Solutions Architect at NBN", 
            pygame.image.load('assets/small_dialogue.png'),70,430,420,50)
        self.npc_richard_dialogue = Dialogue("Dr Richard Liebbrandt, professor", 
            pygame.image.load('assets/small_dialogue.png'),70,430,420,50)
        self.npc_villain_dialogue = Dialogue("Don't touch that rock!", 
            pygame.image.load('assets/small_dialogue.png'),70,430,420,50)

        #animal dialogue
        self.animal_snickers_dialogue = Dialogue("~~purrrrr~~", 
            pygame.image.load('assets/small_dialogue.png'),70,430,420,50)
        self.animal_chunks_dialogue = Dialogue("Meow!", 
            pygame.image.load('assets/small_dialogue.png'),70,430,420,50)
        self.animal_ranger_dialogue = Dialogue("Woof!", 
            pygame.image.load('assets/small_dialogue.png'),70,430,420,50)


        #village npcs
        self.npc_villain = Npc(475,150,16*self.player_scale,20*self.player_scale,
            self.npc_animation_lists[1][0][0],self.height/1000, 1.5, 1, 0, self.npc_villain_dialogue, 1, 0, 50)
        self.village_npc_list = [self.npc_villain]

        #school npcs
        self.npc_richard = Npc(240,130,16*self.player_scale,20*self.player_scale,
            self. npc_animation_lists[4][0][0],0, 0, 1, 0, self.npc_richard_dialogue, 4, 0, 50)
        self.school_npc_list = [self.npc_richard]

        #home npcs
        self.npc_rach = Npc(200,250,16,20*self.player_scale,
            self.npc_animation_lists[0][0][0],self.height/1000, 1.25, 0, 1, self.npc_rach_dialogue, 0, 0, 50)
        self.animal_snickers = Npc(300,300,20*self.player_scale/4,16*self.player_scale/4,
            self.npc_animation_lists[5][0][0],self.height/2000, .5, 0, 1, self.animal_snickers_dialogue, 5, 0, 50)
        self.animal_chunks = Npc(300,240,20*self.player_scale/4,16*self.player_scale/4,
            self.npc_animation_lists[6][0][0],self.height/2000, 2.25, 0, 1, self.animal_chunks_dialogue, 6, 0, 50)
        self.animal_ranger = Npc(200,200,20*self.player_scale/4,16*self.player_scale/4,
            self.npc_animation_lists[7][0][0],self.height/2000, 1.5, 0, 1, self.animal_ranger_dialogue, 7, 0, 50)
        self.home_npc_list = [self.npc_rach, self.animal_snickers, self.animal_chunks, self.animal_ranger]

        #work npcs
        self.npc_aaron = Npc(250,125,16*self.player_scale,20*self.player_scale,
            self.npc_animation_lists[2][0][0],self.height/1000, 2, 1, 1, self.npc_aaron_dialogue, 2, 0, 50)
        self.npc_shaun = Npc(240,300,16*self.player_scale,20*self.player_scale,self.
            npc_animation_lists[3][0][0],self.height/1000, 1.25, 0, 0, self.npc_shaun_dialogue, 3, 0, 50)
        self.work_npc_list = [self.npc_aaron, self.npc_shaun]

        #npc list for level
        self.npc_list =  [self.npc_villain]
        


    #updates animations for all characters
    def update_animation(self, list):
        current_time = pygame.time.get_ticks()
        if self.npc_collision == False:
            if current_time - self.last_update >= self.animation_cooldown:
                self.frame += 1
                self.last_update = current_time
                if self.frame >= len(list):
                    self.frame = 0
        elif self.npc_collision == True:
            self.frame = 1
        return list[self.frame]

    def check_if_collided(self):
        
        #Checks for collision between player and houses
        for building in self.buildings_list:
            if self.detect_collision(self.player, building):
                self.set_dialogue(building)
                self.player.collide(building)
                #Top of player to bottom of building
                if abs(self.player.y - (building.y + building.height)) < self.collision_tolerance:
                    self.player.y = building.y + building.height
                #Bottom of player to bottom of building
                if abs((self.player.y + self.player.height) - building.y) < self.collision_tolerance:
                    self.player.y = building.y - self.player.height
                #Right of player to left of building
                if abs((self.player.x + self.player.width) - building.x) < self.collision_tolerance:
                    self.player.x = building.x - self.player.width
                #Left of player to right of building
                if abs(self.player.x - (building.x + building.width)) < self.collision_tolerance:
                    self.player.x = building.x + building.width
                return True

        #Checks for collision for npcs    
        for npc in self.npc_list:

            #collision with other npcs
            for npc_2 in self.npc_list:
                if self.detect_collision(npc, npc_2) and npc != npc_2:
                    #Top of player to bottom of building
                    if abs(npc.y - (npc_2.y + npc_2.height)) < self.collision_tolerance:
                        npc.y = npc_2.y + npc_2.height
                    #Bottom of player to bottom of building
                    if abs((npc.y + npc.height) - npc_2.y) < self.collision_tolerance:
                        npc.y = npc_2.y - npc.height
                    #Right of player to left of building
                    if abs((npc.x + npc.width) - npc_2.x) < self.collision_tolerance:
                        npc.x = npc_2.x - npc.width
                    #Left of player to right of building
                    if abs(npc.x - (npc_2.x + npc_2.width)) < self.collision_tolerance:
                        npc.x = npc_2.x + npc_2.width

            #Collision with houses
            for building in self.buildings_list:
                if self.detect_collision(building, npc):
                    #Top of player to bottom of building
                    if abs(npc.y - (building.y + building.height)) < self.collision_tolerance:
                        npc.y = building.y + building.height
                    #Bottom of player to bottom of building
                    if abs((npc.y + npc.height) - building.y) < self.collision_tolerance:
                        npc.y = building.y - npc.height
                    #Right of player to left of building
                    if abs((npc.x + npc.width) - building.x) < self.collision_tolerance:
                        npc.x = building.x - npc.width
                    #Left of player to right of building
                    if abs(npc.x - (building.x + building.width)) < self.collision_tolerance:
                        npc.x = building.x + building.width

            #collision with the player
            if self.detect_collision(self.player, npc):
                #Top of player to bottom of npc
                if abs(self.player.y - (npc.y + npc.height)) < self.collision_tolerance:
                    self.player.y = npc.y + npc.height
                #Bottom of player to bottom of npc
                if abs((self.player.y + self.player.height) - npc.y) < self.collision_tolerance:
                    self.player.y = npc.y - self.player.height
                #Right of player to left of npc
                if abs((self.player.x + self.player.width) - npc.x) < self.collision_tolerance:
                    self.player.x = npc.x - self.player.width
                #Left of player to right of npc
                if abs(self.player.x - (npc.x + npc.width)) < self.collision_tolerance:
                    self.player.x = npc.x + npc.width
                npc.player_collision = True
                self.player.collide(npc)
                match self.action:
                    case Movement.DOWN.value:
                        npc.action = Movement.UP.value
                    case Movement.UP.value:
                        npc.action = Movement.DOWN.value
                    case Movement.LEFT.value:
                        npc.action = Movement.RIGHT.value
                    case Movement.RIGHT.value:
                        npc.action = Movement.LEFT.value
                self.npc_collision = True
                npc.change_image(self.update_animation(self.npc_animation_lists[npc.number][npc.action])) 
                npc.collision()
                self.set_dialogue(npc)
                return True
            else:
                npc.player_collision = False

        else: 
            self.dialogue_option = self.default_dialogue
            self.npc_collision = False
            self.player.object_collision = False
            return False

    #Clears all objects and npcs from the working list
    def reset_objects(self):
        print(f"Buidings before delete: {len(self.buildings_list)}")
        self.buildings_list.clear()
        print(f"\nBuildings after delete: {len(self.buildings_list)}\n npcs before delete: {len(self.npc_list)}")
        self.npc_list.clear()
        print(f"\n npcs after delete: {len(self.npc_list)}")

    #changes the scene of the game
    def change_state(self, state):
        match state:
            case 'village':
                self.player.x = self.previous_x
                self.player.y = self.previous_y
                self.state = 'village'
                self.player.change_image(self.sprite_sheet.get_image(1, 0, 16, 20, self.player_scale, (0,0,0)))
                self.height = 512
                self.width = 512
                self.player.left_edge_x = 0
                self.player.top_edge_y = 50
                self.reset_objects()
                for door in self.village_door_list:
                    self.door_list.append(door)
                for npc in self.village_npc_list:
                    npc.left_edge_x = 0
                    npc.top_edge_y = 50
                    self.npc_list.append(npc)
                for building in self.village_building_list:
                    self.buildings_list.append(building)
                self.background = GameObject(0,0,self.width,self.height,pygame.image.load('assets/32x32map.png'))
                self.buildings = GameObject(0,0,self.width,self.height,pygame.image.load('assets/buildings.png'))

            case 'school':
                self.state = 'school'
                self.player.change_image(self.sprite_sheet.get_image(1, 0, 16, 20, self.player_scale, (0,0,0)))
                self.player.x = 237
                self.player.y = 350
                self.height = 401
                self.width = 420
                self.player.left_edge_x = 80
                self.player.top_edge_y = 143
                self.reset_objects()
                self.door_list.append(self.school_door)
                for npc in self.school_npc_list:
                    npc.left_edge_x = 80
                    npc.top_edge_y = 143
                    self.npc_list.append(npc)
                for building in self.school_building_list:
                    self.buildings_list.append(building)
                self.buildings = GameObject(0,0,512,512,pygame.image.load('assets/school_overlay.png'))
                self.background = GameObject(0,0,512,512,pygame.image.load('assets/school_background.png'))
                
            case 'education':
                self.state = 'education'
                self.reset_objects()
                self.previous_state = 'school'
                self.player.change_image(pygame.image.load('assets/Empty.png'))
                self.buildings = GameObject(0,0,512,512,pygame.image.load('assets/Empty.png'))
                self.background = GameObject(0,0,512,512,pygame.image.load('assets/school_text.png'))
            
            case 'home':
                self.state = 'home'
                self.player.change_image(self.sprite_sheet.get_image(1, 0, 16, 20, self.player_scale, (0,0,0)))
                self.player.x = 237
                self.player.y = 350
                self.height = 401
                self.width = 420
                self.player.left_edge_x = 80
                self.player.top_edge_y = 160
                self.reset_objects()
                self.door_list.append(self.home_door)
                for npc in self.home_npc_list:
                    npc.left_edge_x = 80
                    npc.top_edge_y = 160
                    self.npc_list.append(npc)
                for building in self.home_building_list:
                    self.buildings_list.append(building)
                self.buildings = GameObject(0,0,512,512,pygame.image.load('assets/home_overlay.png'))
                self.background = GameObject(0,0,512,512,pygame.image.load('assets/home_background.png'))

            case 'about_me':
                self.state = 'about_me'
                self.previous_state = 'home'
                self.player.change_image(pygame.image.load('assets/Empty.png'))
                self.reset_objects()
                self.buildings = GameObject(0,0,512,512,pygame.image.load('assets/Empty.png'))
                self.background = GameObject(0,0,512,512,pygame.image.load('assets/book_text.png'))

            case 'work':
                self.state = 'work'
                self.player.change_image(self.sprite_sheet.get_image(1, 0, 16, 20, self.player_scale, (0,0,0)))
                self.player.x = 237
                self.player.y = 360
                self.height = 410
                self.width = 420
                self.player.left_edge_x = 80
                self.player.top_edge_y = 143
                self.reset_objects()
                self.door_list.append(self.work_door)
                for npc in self.work_npc_list:
                    npc.left_edge_x = 80
                    npc.top_edge_y = 143
                    self.npc_list.append(npc)
                for building in self.work_building_list:
                    self.buildings_list.append(building)
                self.buildings = GameObject(0,0,512,512,pygame.image.load('assets/work_overlay.png'))
                self.background = GameObject(0,0,512,512,pygame.image.load('assets/work_background.png'))

            case 'computer':
                self.state = 'computer'
                self.player.change_image(pygame.image.load('assets/Empty.png'))
                self.reset_objects()
                self.previous_state = 'work'
                self.buildings = GameObject(0,0,512,512,pygame.image.load('assets/Empty.png'))
                self.background = GameObject(0,0,512,512,pygame.image.load('assets/work_text.png'))



    #Draws objects on screen and updates the frame
    def draw_objects(self):

        #draw objects in background        
        for building in self.buildings_list:
            self.game_window.blit(building.image,(building.x, building.y))

        #builds back background for next frame
        self.game_window.blit(self.background.image, (self.background.x, self.background.y))
        
        #Builds back characters for next frame
        #npcs    
        for npc in self.npc_list:
            self.game_window.blit(npc.image,(npc.x, npc.y))

        #player
        self.game_window.blit(self.player.image,(self.player.x, self.player.y))

        #overlay so that player has the appearance of walking behind the buildings
        self.game_window.blit(self.buildings.image, (self.buildings.x, self.buildings.y))
        if self.check_if_collided() == True:
            self.game_window.blit(self.dialogue_option.image,(self.dialogue_option.x,self.dialogue_option.y))
            self.game_window.blit(self.text_surface,(self.dialogue_option.text_x, self.dialogue_option.text_y))

        pygame.display.update()

    
    #Sets the dialogue option for objects
    def set_dialogue(self, object):
        self.dialogue_option = object.dialogue
        self.text_surface = self.my_font.render(self.dialogue_option.text, False, (0,0,0))

    #moves all characters in the game (npcs and player)
    def move_characters(self):
        if self.state == 'village':
            self.previous_x = self.player.x
            self.previous_y = self.player.y
        self.player.move(self.player.y_direction, self.player.x_direction, self.height, self.width)
        if self.state != 'school':
            for npc in self.npc_list:
                npc.move(self.height, self.width)

    #Detects collision between objects
    def detect_collision(self, object_1, object_2):
        self.collision_tolerance = 10
        #Checks collision on y axis
        if (object_1.y > object_2.y + object_2.height):
            return False
        elif (object_1.y + object_1.height) < object_2.y:
            return False

        #Checks collision on x axis
        if (object_1.x > object_2.x + object_2.width):
            return False
        elif (object_1.x + object_1.width) < object_2.x:
            return False
        else:
            return True

    async def run_game_loop(self):

        #Game loop
        while True:

        #Handle events
            events = pygame.event.get()
            for event in events:
                match event.type:

                    #Handles closing the game               
                    case pygame.QUIT:
                        return

                #Handles movement keys for player
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_UP:
                            self.action = Movement.UP.value
                            self.player.y_direction = Direction.UP.value
                        case pygame.K_DOWN:
                            self.action = Movement.DOWN.value
                            self.player.y_direction = Direction.DOWN.value
                        case pygame.K_RIGHT:
                            self.action = Movement.RIGHT.value
                            self.player.x_direction = Direction.RIGHT.value
                        case pygame.K_LEFT:
                            self.action = Movement.LEFT.value
                            self.player.x_direction = Direction.LEFT.value
                        case pygame.K_w:
                            self.action = Movement.UP.value
                            self.player.y_direction = Direction.UP.value
                        case pygame.K_s:
                            self.action = Movement.DOWN.value
                            self.player.y_direction = Direction.DOWN.value
                        case pygame.K_d:
                            self.action = Movement.RIGHT.value
                            self.player.x_direction = Direction.RIGHT.value
                        case pygame.K_a:
                            self.action = Movement.LEFT.value
                            self.player.x_direction = Direction.LEFT.value
                        
                        #handles interaction with objects.    
                        case pygame.K_SPACE:
                            if self.detect_collision(self.red_door, self.player):
                                self.change_state('school')
                            elif self.state == 'school' and self.detect_collision(self.book, self.player):
                                self.change_state('education')
                            elif self.detect_collision(self.green_door, self.player):
                                self.change_state('work')
                            elif self.state == 'work' and self.detect_collision(self.computer, self.player):
                                self.change_state('computer')
                            elif self.detect_collision(self.blue_door, self.player):
                                self.change_state('home')
                            elif self.state == 'home' and self.detect_collision(self.table, self.player):
                                self.change_state('about_me')
                            elif self.detect_collision(self.school_door, self.player): 
                                self.change_state('village')
                            elif self.detect_collision(self.work_door, self.player):
                                self.change_state('village')
                            elif self.detect_collision(self.home_door, self.player):
                                self.change_state('village')
                            elif self.state == 'education':
                                self.change_state(self.previous_state)
                            elif self.state == 'about_me':
                                self.change_state(self.previous_state)
                            elif self.state == 'computer':
                                self.change_state(self.previous_state)
                #Handles movement of player to stop
                if event.type == pygame.KEYUP:
                    match event.key:
                        #Stops movement on Y axis, but changes animation to left or right if a key is still pressed down
                        case pygame.K_UP:
                            self.player.y_direction = Direction.STOP.value
                            if  self.player.x_direction == Direction.RIGHT.value:
                                self.action = Movement.RIGHT.value
                            elif self.player.x_direction == Direction.LEFT.value:
                                self.action = Movement.LEFT.value
                        case pygame.K_DOWN:
                            self.player.y_direction = Direction.STOP.value
                            if  self.player.x_direction == Direction.RIGHT.value:
                                self.action = Movement.RIGHT.value
                            elif self.player.x_direction == 0:
                                self.action = Movement.LEFT.value
                        case pygame.K_w:
                            self.player.y_direction = Direction.STOP.value
                            if  self.player.x_direction == Direction.RIGHT.value:
                                self.action = Movement.RIGHT.value
                            elif self.player.x_direction == Direction.LEFT.value:
                                self.action = Movement.LEFT.value
                        case pygame.K_s:
                            self.player.y_direction = Direction.STOP.value
                            if  self.player.x_direction == Direction.RIGHT.value:
                                self.action = Movement.RIGHT.value
                            elif self.player.x_direction == 0:
                                self.action = Movement.LEFT.value

                        #Stops movement on X axis, but changes animation to up or down if a key is still pressed down                                
                        case pygame.K_RIGHT:
                            self.player.x_direction = Direction.STOP.value
                            if  self.player.y_direction == Direction.DOWN.value:
                                self.action = Movement.DOWN.value
                            elif self.player.y_direction == Direction.UP.value:
                                self.action = Movement.UP.value
                        case pygame.K_LEFT:
                            self.player.x_direction = Direction.STOP.value
                            if  self.player.y_direction == Direction.DOWN.value:
                                self.action = Movement.DOWN.value
                            elif self.player.y_direction == Direction.UP.value:
                                self.action = Movement.UP.value
                        case pygame.K_d:
                            self.player.x_direction = Direction.STOP.value
                            if  self.player.y_direction == Direction.DOWN.value:
                                self.action = Movement.DOWN.value
                            elif self.player.y_direction == Direction.UP.value:
                                self.action = Movement.UP.value
                        case pygame.K_a:
                            self.player.x_direction = Direction.STOP.value
                            if  self.player.y_direction == Direction.DOWN.value:
                                self.action = Movement.DOWN.value
                            elif self.player.y_direction == Direction.UP.value:
                                self.action = Movement.UP.value
            if self.state != 'computer' and self.state != 'education' and self.state != 'about_me':
                #moves the player according to above input
                if self.player.x_direction != 0 or self.player.y_direction !=0:
                    self.player.change_image(self.update_animation(self.player.animation_list[self.action]))
                for npc in self.npc_list:
                    if npc.x_direction !=0 or npc.y_direction != 0:
                        npc.change_image(self.update_animation(self.npc_animation_lists[npc.number][npc.action]))   
                self.move_characters()

            #Detect collision
            #if self.check_if_collided():
            #    self.player.x_direction = 0
            #    self.player.y_direction = 0      

            #update display
            self.draw_objects()
            self.clock.tick(self.framerate)

            #required for using in HTML
            await asyncio.sleep(0)