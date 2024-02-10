import pygame
from globals import *
from globals import TILESIZE
import math
import random

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, image = pygame.Surface((TILESIZE, TILESIZE)), position = (0, 0), name: str = "default") -> None:
        super().__init__(groups)
        self.name = name
        self.in_groups = groups
        self.image = image
        self.rect = self.image.get_rect(topleft = position)
        
    def update(self):
        pass

class Mob(Entity):
    def __init__(self, groups, image=pygame.Surface((TILESIZE, TILESIZE)), position=(0, 0), parameters={}):
        super().__init__(groups, image, position)

        # Existing attributes
        self.velocity = pygame.math.Vector2()
        self.mass = 5
        self.terminal_velocity = self.mass * TERMINALVELOCITY
        self.speed = 0.5
        self.state = 'idle'  # Initial state

        # Additional attributes for state management
        self.wander_direction = random.choice([-1, 1])
        self.wander_timer = random.randint(60, 180)  # Time in frames before changing direction
        self.chase_timer = 0  # Timer for how long to chase the player
        self.attack_cooldown = 60
        self.counter = self.attack_cooldown

        if parameters:
            self.block_group = parameters['block_group']
            self.player = parameters['player']
            self.damage = parameters['damage']

    def move(self):
        self.velocity.y += GRAVITY * self.mass

        if self.velocity.y > self.terminal_velocity:
            self.velocity.y = self.terminal_velocity

        player_distance = math.sqrt((self.rect.x - self.player.rect.x) ** 2 + (self.rect.y - self.player.rect.y) ** 2)

        # State transitions
        if player_distance < TILESIZE * 10:
            self.state = 'chasing'
            self.chase_timer = 300  # Chase for a certain amount of frames
        elif self.state == 'chasing' and self.chase_timer <= 0:
            self.state = 'idle'

        # State-based behaviors
        if self.state == 'idle':
            self.wander()
        elif self.state == 'chasing':
            self.chase(player_distance)
        if self.state == 'attacking':
            self.check_player_collision()

        # Movement and collision logic
        self.rect.x += int(self.velocity.x * PLAYERSPEED)
        self.check_collision('horizontal')
        self.rect.y += int(self.velocity.y)
        self.check_collision('vertical')

    def wander(self):
        # Randomly wander around
        if self.wander_timer <= 0:
            self.wander_direction = random.choice([-1, 1])
            self.wander_timer = random.randint(60, 180)  # Change direction after a random time

        self.velocity.x = self.wander_direction * self.speed
        self.wander_timer -= 1

    def chase(self, player_distance):
        # Chase the player
        if self.rect.x > self.player.rect.x:
            self.velocity.x = -self.speed
        elif self.rect.x < self.player.rect.x:
            self.velocity.x = self.speed

        self.chase_timer -= 1

        # Transition to attacking state if close enough to the player
        if player_distance < TILESIZE/2:
            self.state = 'attacking'

    def check_collision(self, direction):
        if direction == 'horizontal':
            for block in self.block_group:
                if self.rect.colliderect(block.rect):
                    if self.velocity.x > 0:
                        self.rect.right = block.rect.left
                    if self.velocity.x < 0:
                        self.rect.left = block.rect.right
                    self.velocity.x = 0

        if direction == 'vertical':
            collisions = 0
            for block in self.block_group:
                if self.rect.colliderect(block.rect):
                    if self.velocity.y > 0:
                        collisions += 1
                        self.rect.bottom = block.rect.top
                        self.velocity.y = 0
                    if self.velocity.y < 0:
                        self.rect.top = block.rect.bottom
                        self.velocity.y = 0

            if collisions > 0:
                self.on_ground = True
            else:
                self.on_ground = False

    def check_player_collision(self):
        # Attack the player if in attacking state and cooldown has elapsed
        if self.state == 'attacking' and self.counter <= 0:
            if self.rect.colliderect(self.player.rect):
                self.player.take_damage(self.damage)  # Call the take_damage method
                self.counter = self.attack_cooldown  # Reset the attack cooldown
        # Decrement the attack cooldown counter
        if self.counter > 0:
            self.counter -= 1
            
        # knockback
        if self.player.rect.centerx > self.rect.centerx:
            self.velocity.x = -self.speed
        elif self.player.rect.centerx < self.rect.centerx:
            self.velocity.x = self.speed

    def update(self):
        self.move()
        self.check_player_collision()