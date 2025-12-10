import pygame
import random
from game.item import Shield
from game.item import SpeedUp

class PipeManager:
    def __init__(self, pipe_surface):
        self.pipe_surface = pipe_surface
        self.pipe_list = []
        
        self.spawn_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_event, 1200)
        self.passed_pipes = set()

        self.last_pipe_pos = None

    def reset(self):
        self.pipe_list.clear()
        self.passed_pipes.clear()
        self.last_pipe_pos = None
        
    def create_pipe(self, shield_surface, speedup_surface):
        min_height = 250
        max_height = 550
        step_diff = 150

        if self.last_pipe_pos is None:
            # first pipe is free
            pos = random.randint(min_height, max_height)
        else:
            low = max(min_height, self.last_pipe_pos - step_diff)
            high = min(max_height, self.last_pipe_pos + step_diff)
            pos = random.randint(low,high)

        self.last_pipe_pos = pos

        
        bottom = self.pipe_surface.get_rect(midtop = (500, pos))
        top = self.pipe_surface.get_rect(midbottom = (500, pos - 180))
        
        new_item = None
        if random.random() < 0.3:  # 30% chance to add a shield
            item_pos = (530, pos - 75)
            if random.random() < 0.7:
                new_item = Shield(shield_surface, item_pos)
            else:
                new_item = SpeedUp(speedup_surface, item_pos)
        return (bottom, top), new_item

    def draw_pipes(self, screen):
        for pipe in self.pipe_list:
            if pipe.bottom >= 600:
                screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                screen.blit(flip_pipe, pipe)


    def move_pipes(self, speed):
        for pipe in self.pipe_list:
            pipe.centerx -= speed

        self.pipe_list = [pipe for pipe in self.pipe_list if pipe.right > -50]

    def check_collision(self, bird, hit_sound, sound_shield_break):
        for pipe in self.pipe_list[:]:
            if bird.is_speeding:
                return True
            if bird.rect.colliderect(pipe):
                if bird.is_shielded:
                    bird.is_shielded = False
                    bird.invincible_timer = 60 #(1s = 60 frame)
                    sound_shield_break.play()
                    return True
                
                if bird.invincible_timer > 0:
                    return True

                hit_sound.play()
                return False

        if bird.rect.top <= -100 or bird.rect.bottom >= 650:
            return False

        return True
    
    def scoring(self, bird_rect, score, score_sound):
        active_pipe_ids = set()
        score_added_this_frame = False # Cờ để đảm bảo âm thanh chỉ phát một lần

        for pipe in self.pipe_list:
            # Luôn thêm ID của tất cả các ống hiện tại vào tập hợp active
            active_pipe_ids.add(id(pipe)) 
            
            # Kiểm tra xem chim đã vượt qua ống VÀ ống này chưa được tính điểm
            if pipe.right < bird_rect.left and id(pipe) not in self.passed_pipes:
                
                score += 0.5 # Cộng 0.5 điểm cho MỖI ống (trên hoặc dưới)
                
                # Chỉ phát âm thanh lần đầu tiên trong khung hình này
                if not score_added_this_frame:
                    score_sound.play()
                    score_added_this_frame = True
                    
                # Thêm ID duy nhất của ống này vào set đã tính điểm
                self.passed_pipes.add(id(pipe)) 
        
        # Dọn dẹp set: Xóa ID của các ống đã bay ra khỏi màn hình
        self.passed_pipes = self.passed_pipes.intersection(active_pipe_ids)
        
        return score