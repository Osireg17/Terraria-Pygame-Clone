import pygame
from globals import *
from world.sprite import Entity, Mob
from world.texturedata import solo_texture_data, atlas_texture_data
from world.player import Player
from opensimplex import OpenSimplex
import random
from camera import Camera
from inventory.inventory import Inventory
from world.items import *

class Scene:
    def __init__(self, app) -> None:
        self.app = app
        
        self.textures = self.gen_solo_texture()
        self.textures.update(self.gen_atlas_texture('pictures/owatlas.png'))
        
        self.sprites = Camera()
        self.blocks = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.group_list: dict[str, pygame.sprite.Group] = {
            'sprites': self.sprites,
            'block_group': self.blocks,
            'enemy_group': self.enemy_group,
        }
        # Inventory
        self.inventory = Inventory(self.app, self.textures)
        self.entity = Entity([self.sprites], image=self.textures['grass'])
        Entity([self.sprites], position=(200, 200), image=self.textures['stone'])
        

        self.PLAYER = Player([self.sprites], self.textures['player_static'], (0, 0), parameters={'texture': self.textures, 'group_list': self.group_list, 'iventory': self.inventory, 'health': 50,})
        
        # Mob([self.sprites], self.textures['enemy_static'], (400, 100), parameters={'block_group': self.blocks, 'player': self.PLAYER} )
        
        # random generate multiple enemies
        for _ in range(3):
            Mob([self.sprites, self.enemy_group], self.textures['enemy_static'], (random.randint(0, 1000), 100), parameters={'block_group': self.blocks, 'player': self.PLAYER, 'damage': 5} )
        self.gen_world()
        
        self.chunks: dict[tuple[int, int], Chunk] = {}
        self.active_chunks: dict[tuple[int, int], Chunk] = {}
        
    def gen_solo_texture(self) -> dict:
        textures = {}
        
        for name, data in solo_texture_data.items():
            texture = pygame.image.load(data['file_path']).convert_alpha()
            texture = pygame.transform.scale(texture, data['size'])
            textures[name] = texture
            
        return textures
    def gen_atlas_texture(self, filepath):
        textures = {}
        atlas_image = pygame.transform.scale(pygame.image.load(filepath).convert_alpha(), (TILESIZE*16, TILESIZE*16))
        
        for name, data in atlas_texture_data.items():
            textures[name] = atlas_image.subsurface(pygame.Rect(data['pos'][0]*TILESIZE,
                                                                data['pos'][1]*TILESIZE, 
                                                                data['size'][0],
                                                                data['size'][1]
                                                                ))
        
        return textures
    def gen_world(self):
        pass
                
    def health_bar(self):
        health_bar_width = 200
        health_bar_height = 35
        screen_width = self.app.screen.get_width()
        health_percentage = self.PLAYER.health / self.PLAYER.max_health

    # Background rectangle (red part)
        background_rect = pygame.Rect(screen_width - health_bar_width, 10, health_bar_width, health_bar_height)
        pygame.draw.rect(self.app.screen, 'red', background_rect)

    # Foreground rectangle (green part)
        foreground_width = health_bar_width * health_percentage
        foreground_rect = pygame.Rect(screen_width - health_bar_width, 10, foreground_width, health_bar_height)
        pygame.draw.rect(self.app.screen, 'green', foreground_rect)

    # Health bar outline
        border_color = 'white'  # Change as per your design
        pygame.draw.rect(self.app.screen, border_color, background_rect, 2)  # 2 is the border thickness

    # Health text
        font = pygame.font.SysFont('Arial', 18)  # You can choose your font and size
        health_text = font.render(f'{self.PLAYER.health}/{self.PLAYER.max_health}', True, 'white')
        text_rect = health_text.get_rect(center=background_rect.center)
        self.app.screen.blit(health_text, text_rect)

        
    def update(self):
        self.sprites.update()  
        self.inventory.update()
        self.health_bar()
        
        player_chunk_pos = Chunk.get_chunk_pos(self.PLAYER.rect.center)
        
        positions = [
            player_chunk_pos,
            (player_chunk_pos[0] + 1, player_chunk_pos[1]),
            (player_chunk_pos[0] - 1, player_chunk_pos[1]),
            (player_chunk_pos[0], player_chunk_pos[1] + 1),
            (player_chunk_pos[0], player_chunk_pos[1] - 1),
            (player_chunk_pos[0] + 1, player_chunk_pos[1] + 1),
            (player_chunk_pos[0] - 1, player_chunk_pos[1] - 1),
            (player_chunk_pos[0] + 1, player_chunk_pos[1] - 1),
            (player_chunk_pos[0] - 1, player_chunk_pos[1] + 1),
            
        ]
        
        for position in positions:
            if position not in self.active_chunks:
                if position in self.chunks:
                    self.chunks[position].load_chunk()
                    self.active_chunks[position] = self.chunks[position]
                else:
                    self.chunks[position] = Chunk(position, self.group_list, self.textures)
                    self.active_chunks[position] = self.chunks[position]
        
        target = None
        for position, chunk in list(self.active_chunks.items()):
            if position not in positions:
                target = position
        if target:
            self.active_chunks[target].unload_chunk()
            self.active_chunks.pop(target)
    def draw(self):
        self.app.screen.fill('lightblue')
        self.sprites.draw(self.PLAYER, self.app.screen)
        self.inventory.draw()
        
        
class Chunk:
    CHUNCKSIZE = 30
    CHUNCKSIZE_PX = CHUNCKSIZE * TILESIZE
    
    def __init__(self, position: tuple[int, int], group_list: dict[str, pygame.sprite.Group], textures: dict[str, pygame.Surface]) -> None:
        self.position = position
        self.group_list = group_list
        self.textures = textures
        
        self.blocks: list[Entity] = []
        self.gen_chunk()
        
    def gen_chunk(self):
        noise_gen = OpenSimplex(
            seed=random.randint(0, 10000000)
        )
        height_map  = []
        for y in range(Chunk.CHUNCKSIZE * self.position[0], Chunk.CHUNCKSIZE * self.position[0] + Chunk.CHUNCKSIZE):
            noise_val = noise_gen.noise2(y*0.05, 0)
            height = int((noise_val + 1) * 4 + 5)
            height_map.append(height)
            
        for x in range(len(height_map)):
            if self.position[1] > 0:
                height_value =  Chunk.CHUNCKSIZE
            elif self.position[1] < 0:
                height_value = 0
            else:
                height_value = height_map[x]
            
            for y in range(height_value):
                block_type = 'dirt'
                if y == height_map[x]-1:
                    block_type = 'grass'
                if y < height_map[x]-5:
                    block_type = 'stone'
                use_type =  items[block_type].use_type
                groups = [self.group_list[group] for group in items[block_type].groups]
                self.blocks.append(use_type(groups, self.textures[block_type], position=(x * TILESIZE + (Chunk.CHUNCKSIZE_PX * self.position[0]), (Chunk.CHUNCKSIZE - y ) * TILESIZE + (Chunk.CHUNCKSIZE_PX * self.position[1])), name=block_type))

    def load_chunk(self):
        for block in self.blocks:
            groups = [self.group_list[group] for group in items[block.name].groups]
            for group in groups:
                group.add(block)
    def unload_chunk(self):
        for block in self.blocks:
            block.kill()
            
    @staticmethod
    def get_chunk_pos(position: tuple[int, int]) -> tuple[int, int]:
        return (position[0] // Chunk.CHUNCKSIZE_PX, position[1] // Chunk.CHUNCKSIZE_PX)
    