from globals import *

atlas_texture_data = {
    'grass': {'type':'block', 'size':(TILESIZE, TILESIZE), 'pos':(0, 0)},
    'dirt': {'type':'block', 'size':(TILESIZE, TILESIZE), 'pos':(0, 1)},
    'stone': {'type':'block', 'size':(TILESIZE, TILESIZE), 'pos':(1, 0)},
}

solo_texture_data = {
    'player_static': {'type':'player', 'file_path':'pictures/player.png', 'size':(TILESIZE*2, TILESIZE*2)},
    'enemy_static': {'type':'enemy', 'file_path':'pictures/zombie.png', 'size':(TILESIZE*2, TILESIZE*2)},
    'short_sword': {'type':'weapon', 'file_path':'weapons/shortsword.png', 'size':(TILESIZE, TILESIZE)},
}