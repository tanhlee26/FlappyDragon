import pygame 

class Item(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.speed = 5

    def update(self, speed):
        self.rect.centerx -= speed
        
class Shield(Item):
    def __init__(self, image, position):
        super().__init__(image, position)
        self.type = 'shield'

class SpeedUp(Item):
    def __init__(self, image, position):
        super().__init__(image, position)
        self.type = 'speedup'
        
