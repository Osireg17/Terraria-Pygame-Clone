import pygame

class EventHandler:
    events = []

    @staticmethod
    def poll_events():
        EventHandler.events = pygame.event.get()
        
    @staticmethod
    def keydown(key):
        for event in EventHandler.events:
            if event.type == pygame.KEYDOWN and event.key == key:
                return True
        return False
    @staticmethod
    def clicked(leftright = 1) -> bool:
        for event in EventHandler.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == leftright:
                    return True
        return False
    
    @staticmethod
    def clicked_any() -> bool:
        for event in EventHandler.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
        return False

        