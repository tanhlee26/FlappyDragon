import pygame

class Bird:
    def __init__(self, images, position):
        self.images = images
        self.index = 0
        self.image = self.images[self.index] 
        self.rect = self.image.get_rect(center = position)
        self.movement = 0
        self.gravity = 0.3
        self.is_shielded = False
        self.invincible_timer = 0
        self.rect.inflate_ip(-30,-30)
        self.is_speeding = False
        

        self.flap_event = pygame.USEREVENT + 0
        pygame.time.set_timer(self.flap_event, 65)
    def update(self):

        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            # nhấp nháy trong trạng thái bất tử.
            if self.invincible_timer % 20 < 5:
                self.image.set_alpha(128)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

        if self.is_speeding:
            if self.rect.centery > 348:
                self.rect.centery -= 2
            elif self.rect.centery < 348:
                self.rect.centery += 2
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
        else:
            self.movement += self.gravity
            self.rect.centery += self.movement

    def jump(self, sound):
        self.movement = 0
        self.movement -= 6
        sound.play()
    
    def rotate(self):
        return pygame.transform.rotozoom(self.image, -self.movement * 3, 1)

    def animate(self):
        self.index = (self.index + 1) % len(self.images)
        self.image = self.images[self.index]
        current_center = self.rect.center 

        self.rect = self.image.get_rect(center = current_center)
        self.rect.inflate_ip(-20, -20)