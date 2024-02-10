import pygame 
from globals import *
from events import EventHandler
from world.sprite import Entity

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, image: pygame.Surface, position: tuple, parameters: dict ) -> None:
        super().__init__(groups) 
        self.image = image
        self.rect = self.image.get_rect(topleft = position)
        
        
        self.texture = parameters['texture']
        self.group_list = parameters['group_list']
        self.block_group = self.group_list['block_group']
        self.enemy_group = self.group_list['enemy_group']
        self.inventory = parameters['iventory']
        
        self.health = parameters['health']
        self.max_health = parameters['health']
        
        self.velocity = pygame.math.Vector2()
        self.mass = 5  
        self.termnal_velocity = self.mass * TERMINALVELOCITY
        
        
        self.on_ground = True
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.velocity.x = -1
        if keys[pygame.K_d]:
            self.velocity.x = 1
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            if self.velocity.x  > 0:
                self.velocity.x -= 0.1
            elif self.velocity.x < 0:
                self.velocity.x += 0.1
                
        if abs(self.velocity.x) < 0.3:
            self.velocity.x = 0
            
        if EventHandler.clicked(1):
            # loop through and check if I have collided with an enemy
            for enemy in self.enemy_group:
                if enemy.rect.collidepoint(pygame.mouse.get_pos()):
                    self.inventory.slots[self.inventory.active_slot].attack(self, enemy)
        
    def move(self):
        self.velocity.y += GRAVITY * self.mass
        
        if self.velocity.y > self.termnal_velocity: 
            self.velocity.y = self.termnal_velocity
        
        self.rect.x += int(self.velocity.x * PLAYERSPEED)
        self.check_collision('horizontal')
        self.rect.y += int(self.velocity.y)
        self.check_collision('vertical')
        
        if self.on_ground and EventHandler.keydown(pygame.K_SPACE):
            self.velocity.y = -PLAYERJUMPPOWER 
    def check_collision(self, direction):
        if direction == 'horizontal':
            for block in self.block_group:
                if self.rect.colliderect(block.rect):
                    if self.velocity.x > 0:
                        self.rect.right = block.rect.left
                    elif self.velocity.x < 0:
                        self.rect.left = block.rect.right
        if direction == 'vertical':
            collisions = 0
            for block in self.block_group:
                if self.rect.colliderect(block.rect):
                    if self.velocity.y > 0:
                        collisions += 1
                        self.rect.bottom = block.rect.top
                        self.velocity.y = 0
                    elif self.velocity.y < 0:
                        self.rect.top = block.rect.bottom
                        self.velocity.y = 0
                        
            if collisions > 0:
                self.on_ground = True
            else:
                self.on_ground = False
                
    def block_handling(self):
        placed = False
        collision = False
        mouse_pos = self.get_adjusted_pos()
        
        if EventHandler.clicked_any():
            for block in self.block_group:
                if block.rect.collidepoint(mouse_pos):
                    collision = True
                    if EventHandler.clicked(1):
                        self.inventory.add_item(block)
                        block.kill()
                if EventHandler.clicked(3):
                    if not collision:
                        placed = True
        if placed and not collision:
            self.inventory.use(self, self.get_block_pos(mouse_pos))
                        
    def get_adjusted_pos(self) -> tuple:
        mouse_pos = pygame.mouse.get_pos()
        
        player_offset = pygame.math.Vector2()
        player_offset.x = SCREENWIDTH/2 - self.rect.centerx
        player_offset.y = SCREENHEIGHT/2 - self.rect.centery
        
        return (mouse_pos[0] - player_offset.x, mouse_pos[1] - player_offset.y)
    
    def get_block_pos(self, mouse_pos: tuple) -> tuple[int, int]:
        return (int((mouse_pos[0]//TILESIZE)*TILESIZE), int((mouse_pos[1]//TILESIZE)*TILESIZE))
    
    def take_damage(self, damage: int):
        self.health -= damage
        
        if self.health <= 0:
            self.kill()
        
    def update(self):
        self.input()
        self.move()
        self.block_handling()