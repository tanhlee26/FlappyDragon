# Tệp: game/scoreborad.py
# Hãy chép và dán TOÀN BỘ nội dung này

class ScoreBoard:
    def __init__(self, font):
        self.font = font
        self.score = 0
        self.high_score = 0

    def update_highcore(self):
        # Đảm bảo điểm số là int khi so sánh
        current_score = int(self.score)
        if current_score > self.high_score:
            self.high_score = current_score

    def draw(self, screen, state):
        if state == 'main':
            # Sửa lỗi hiển thị: Thêm int()
            surf = self.font.render(str(int(self.score)), True, (255, 255, 255))
            rect = surf.get_rect(center=(216, 100))
            screen.blit(surf, rect)

        else:
            # Sửa lỗi hiển thị: Thêm int()
            score_surf = self.font.render(f"Score: {int(self.score)}", True, (255, 255, 255))
            hs_surf = self.font.render(f"High Score: {int(self.high_score)}", True, (255, 255, 255))

            screen.blit(score_surf, score_surf.get_rect(center = (216, 100)))
            screen.blit(hs_surf, hs_surf.get_rect(center = (216, 620)))