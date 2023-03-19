import pygame
import asyncio
from level import Level

game = Level()

pygame.init()

asyncio.run(game.run_game_loop())