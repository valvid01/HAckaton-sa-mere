import pygame as pg
from random import randint

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Character:
    def __init__ (self, x, y, inventory = {}, health=12,strength = 16, armor=5, gold=0):
        self.x = x
        self.y = y
        self.inventory = inventory
        self.health = health
        self.strength = strength
        self.armor = armor
        self.gold = gold
    def __repr__(self):
        return f"Position : x = {self.x}, y = {self.y}"

