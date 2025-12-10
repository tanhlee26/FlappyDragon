import pygame
import sys
import random

from game.bird import Bird
from game.pipe_manager import PipeManager

from game.scoreborad import ScoreBoard
from game.item import Shield

class FlappyGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 512)

        self.screen = pygame.display.set_mode((432, 768))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font('FileGame/04B_19.TTF', 40)
        self.gameover_surface = pygame.transform.scale2x(pygame.image.load('FileGame/assets/gameover.png'))
        self.gameover_rect = self.gameover_surface.get_rect(center = (216,384))

        # variable
        self.game_speed = 5
        self.scroll_speed = 5
        self.boost_target = 0
        self.boost_amount = 5

        # Background
        self.bg = pygame.transform.scale(
            pygame.image.load('FileGame/assets/map4.png'), (432, 768)
        )

        # Bird images 
        size_bird = (84, 74)
        dragon1_imgs = [
            pygame.transform.scale(pygame.image.load(f'FileGame/assets/frame_{i:04}.png'), size_bird)
            for i in range(9)
        ]
        dragon2_imgs = [
            pygame.transform.scale(pygame.image.load(f'FileGame/assets/frame_{i}.png'), size_bird)
            for i in range(9)
        ]
        self.dragon_img_sets = [dragon1_imgs, dragon2_imgs]

        # Pipe
        pipe_img = pygame.transform.scale(
            pygame.image.load('FileGame/assets/round_tower.png'),
            (104, 640)
        )

        # Items
        self.item_list = []
        self.shield_item = pygame.transform.smoothscale(
            pygame.image.load('FileGame/assets/shield.png').convert_alpha(),
            (60, 60)
        )

        self.speedup_item = pygame.transform.smoothscale(
            pygame.image.load('FileGame/assets/speedup.png').convert_alpha(),
            (60, 60)
        )

        self.shield_visual = pygame.transform.smoothscale(
            pygame.transform.scale2x(
                pygame.image.load('FileGame/assets/shield_visual.png')
            ).convert_alpha(),
            (100, 100)
        )

        # Game objects
        self.dragon_image = random.choice(self.dragon_img_sets)
        self.bird = Bird(self.dragon_image, (100, 384))
        self.pipes = PipeManager(pipe_img)
        self.scoreBoard = ScoreBoard(self.font)

        # Sounds
        self.sound_flap = pygame.mixer.Sound('FileGame/sound/sfx_wing.wav')
        self.sound_hit = pygame.mixer.Sound('FileGame/sound/sfx_hit.wav')
        self.sound_point = pygame.mixer.Sound('FileGame/sound/sfx_point.wav')
        self.sound_powerup = pygame.mixer.Sound('FileGame/sound/powerup.wav')
        self.sound_shield_break = pygame.mixer.Sound('FileGame/sound/shield_break.wav')

        self.active = True

    # ---------------------------------------------------------------------

    def reset(self):
        self.active = True
        self.dragon_image = random.choice(self.dragon_img_sets)
        self.bird = Bird(self.dragon_image, (100, 384))
        self.pipes.reset()
        self.item_list.clear()

        self.bird.rect.center = (100, 348)
        self.bird.movement = 0
        self.bird.is_shielded = False
        self.scoreBoard.score = 0

    # ---------------------------------------------------------------------

    def update_items(self, speed):
        for item in self.item_list[:]:
            item.update(speed)
            self.screen.blit(item.image, item.rect)

            if item.rect.right < -50:
                self.item_list.remove(item)
                continue

            if self.bird.rect.colliderect(item.rect):
                if item.type == 'shield':
                    self.bird.is_shielded = True
                    self.sound_powerup.play()
                self.item_list.remove(item)

                if item.type == 'speedup':
                    self.active_speed_boost()
                    self.sound_powerup.play()

    # ---------------------------------------------------------------------

    def active_speed_boost(self):
        self.bird.is_speeding = True
        self.bird.is_shielded = True
        self.scroll_speed = 20
        self.boost_target = self.scoreBoard.score + self.boost_amount
        # xóa gravity hiện tại để chim không rơi.
        self.bird.movement = 0
        pygame.time.set_timer(self.pipes.spawn_event, 300)

    # ---------------------------------------------------------------------

    def check_boost_status(self):
        if self.bird.is_speeding:
            if self.scoreBoard.score >= self.boost_target:
                # stope speed
                self.bird.is_speeding = False
                self.bird.is_shielded = False
                self.scroll_speed = self.game_speed 
                self.bird.jump(self.sound_flap)# tránh rơi cấm đầu khi hết speed.
                pygame.time.set_timer(self.pipes.spawn_event, 1200) 
    # ---------------------------------------------------------------------

    def run(self):
        while True:

            # ------------------ HANDLE EVENTS -------------------
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.active:
                        self.bird.jump(self.sound_flap)
                    else:
                        self.reset()

                if event.type == self.pipes.spawn_event:
                    new_pipe, new_item = self.pipes.create_pipe(self.shield_item, self.speedup_item)
                    self.pipes.pipe_list.extend(new_pipe)
                    if new_item:
                        self.item_list.append(new_item)

                if event.type == self.bird.flap_event:
                    self.bird.animate()

            # ------------------ DRAW BACKGROUND -------------------
            self.screen.blit(self.bg, (0, 0))

            # ------------------ GAME ACTIVE -------------------
            if self.active:
                self.bird.update()
                self.update_items(self.scroll_speed)

                # Bird rotate
                rotated_bird = self.bird.rotate()
                self.screen.blit(
                    rotated_bird,
                    rotated_bird.get_rect(center=self.bird.rect.center)
                )

                # Shield
                if self.bird.is_shielded:
                    self.screen.blit(
                        self.shield_visual,
                        self.shield_visual.get_rect(center=self.bird.rect.center)
                    )

                # Speedup
                self.check_boost_status()
                
                # Pipe
                self.pipes.move_pipes(self.scroll_speed)
                self.pipes.draw_pipes(self.screen)

                # Score
                self.scoreBoard.score = self.pipes.scoring(
                    self.bird.rect,
                    self.scoreBoard.score,
                    self.sound_point
                )
                self.scoreBoard.draw(self.screen, 'main')

                # Collision
                self.active = self.pipes.check_collision(
                    self.bird,
                    self.sound_hit,
                    self.sound_shield_break
                )

            # ------------------ GAME OVER -------------------
            else:
                self.screen.blit(self.gameover_surface, self.gameover_rect)
                self.scoreBoard.update_highcore()
                self.scoreBoard.draw(self.screen, 'over')

            # ------------------ UPDATE SCREEN -------------------
            pygame.display.update()
            self.clock.tick(60)
