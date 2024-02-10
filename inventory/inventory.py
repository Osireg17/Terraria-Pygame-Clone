# 11.25 video 10
from globals import *
from world.items import *
from events import EventHandler
from world.player import Player
class Inventory: 
    def __init__(self, app, textures) -> None:
        self.app = app
        self.screen = app.screen
        self.textures = textures
            
        self.slots = []
        for index in range(5):
            self.slots.append(Item())
        self.slots[0] = ShortSwordItem('short_sword', 1)
        self.slots[1] = BlockItem('grass', 5)
        self.slots[2] = BlockItem('dirt', 3)
        self.slots[3] = BlockItem('stone', 3)
        
        self.active_slot = 0
        self.font = pygame.font.SysFont('Arial', 20)
    
    def debug(self):
        for slot in self.slots:
            print(slot)
            
    def use(self, player, position):
        if self.slots[self.active_slot].name != "default":
            self.slots[self.active_slot].use(player, position)
            
    def add_item(self, item: Item):
        first_available_slot = len(self.slots) # first empty slot
        target_slot = len(self.slots) # first slot of same name
        
        for index, slot in enumerate(self.slots):
            if slot.name == "default" and index < first_available_slot:
                first_available_slot = index
            if slot.name == item.name:
                target_slot = index
        if target_slot < len(self.slots):
            self.slots[target_slot].quantity += items[item.name].quantity
        elif first_available_slot < len(self.slots):
            self.slots[first_available_slot] = items[item.name].item_type(item.name, items[item.name].quantity)
    def update(self):
        if EventHandler.keydown(pygame.K_RIGHT):
            if self.active_slot < len(self.slots)-1:
                self.active_slot += 1
            print(f'Active slot: {self.active_slot}')
        if EventHandler.keydown(pygame.K_LEFT):
            if self.active_slot > 0:
                self.active_slot -= 1
            print(f'Active slot: {self.active_slot}')
        if EventHandler.clicked_any():
            self.debug()
            
    def draw(self):
        pygame.draw.rect(self.screen, "gray", pygame.Rect(0, 0, (TILESIZE*2)*len(self.slots), (TILESIZE*2)))
        
        x_offset = TILESIZE/2
        y_offset = TILESIZE/2
        
        for i in range(len(self.slots)):
            if i == self.active_slot:
                pygame.draw.rect(self.screen, "white", pygame.Rect(i*(TILESIZE*2), 0, TILESIZE*2, TILESIZE*2))
            pygame.draw.rect(self.screen, "black", pygame.Rect(i*(TILESIZE*2), 0, TILESIZE*2, TILESIZE*2), 2)
            if self.slots[i].name != "default":
                self.screen.blit(self.textures[self.slots[i].name], (x_offset + (TILESIZE*2)*i, y_offset))
                text = self.font.render(str(self.slots[i].quantity), True, "white")
                self.screen.blit(text, (x_offset + (TILESIZE*2)*i, y_offset))
            pygame.draw.rect(self.screen, "black", pygame.Rect(x_offset + (TILESIZE*2)*i, y_offset, TILESIZE, TILESIZE), 2)
         