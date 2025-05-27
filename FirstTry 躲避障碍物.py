import pygame
import random

# 初始化Pygame
pygame.init()

# 设置屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 设置游戏标题
pygame.display.set_caption("躲避障碍物")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 设置时钟
clock = pygame.time.Clock()

# 设置字体
font = pygame.font.Font(None, 36)

# 游戏结束标志
game_over = False
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# 创建精灵组
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# 初始化玩家
player = Player()
all_sprites.add(player)

# 设置障碍物生成时间
OBSTACLE_FREQ = 500  # 每500毫秒生成一个障碍物
last_obstacle = pygame.time.get_ticks()
# 游戏主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # 更新游戏状态
        all_sprites.update()

        # 生成障碍物
        now = pygame.time.get_ticks()
        if now - last_obstacle > OBSTACLE_FREQ:
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)
            last_obstacle = now

        # 检测碰撞
        if pygame.sprite.spritecollide(player, obstacles, False):
            game_over = True

        # 绘制画面
        screen.fill(WHITE)
        all_sprites.draw(screen)
    else:
        # 显示游戏结束文本
        text = font.render("Game Over! Press R to Restart", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

        # 处理重新开始
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_over = False
            all_sprites.empty()
            obstacles.empty()
            player = Player()
            all_sprites.add(player)

    # 更新显示
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

# 退出Pygame
pygame.quit()

# 设置文字
# font = pygame.font.Font(None, 24)  # 使用默认字体，字号为24
# text = font.render("Hit!", True, WHITE)  # 渲染文字，颜色为白色
# text_rect = text.get_rect(center=(25, 25))  # 将文字居中
# self.image.blit(text, text_rect)  # 将文字绘制到障碍物的图像上