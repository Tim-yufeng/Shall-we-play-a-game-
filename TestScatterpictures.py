from Sec_section import SCREEN_HEIGHT, SCREEN_WIDTH, sec_section
import pygame
import random
import math
import numpy as np
import os
from Disassembly_of_Yangda2 import Disassembly_of_Yangda

# 初始化pygame
pygame.init()
chinese_font = pygame.font.Font(r"Fonts_Package_fc12b50164b107e5d087c5f0bbbf6d82\SimHei\simhei.ttf", 36)
font = pygame.font.Font(None, 36)

# 屏幕设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("京华风云")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (105, 43, 128)

# 字体设置
# try:
#     chinese_font = pygame.font.Font("simhei.ttf", 36)
# except:
#     chinese_font = pygame.font.SysFont(None, 36)
# font = pygame.font.SysFont(None, 36)

# 游戏变量
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
game_over = False
round_completed = False
OBSTACLE_FREQ = 500  # 障碍物生成间隔（毫秒）
last_obstacle = 0
score = 0

def draw_multiline_text(surface, font, text, color, x, y, line_height=40):
    """渲染多行文本（支持 `\n`）"""
    for i, line in enumerate(text.splitlines()):  # 按 `\n` 分割
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y + i * line_height)
        surface.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 创建玩家图像（如果没有图片则使用紫色方块）
        try:
            self.original_image = pygame.image.load("ncu.jpg").convert_alpha()
            self.image = pygame.transform.scale(self.original_image, (150, 150))
        except:
            self.image = pygame.Surface((150, 150), pygame.SRCALPHA)
            self.image.fill(PURPLE)
            self.original_image = self.image.copy()

        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5
        self.alpha = 255
        self.fading = False
        self.moving_to_center = False  # 新增移动状态
        self.target_y = SCREEN_HEIGHT // 2  # 目标Y坐标
        self.target_x = SCREEN_WIDTH // 2  # 目标X坐标

        # 手动散射相关
        self.is_scattering = False
        self.scattering_images = []

        # 游戏结束散射相关
        self.game_end_scattering = False
        self.scattering_objects = []
        self.scattering_images_game_end = []

        # 粒子效果
        self.particles = []

    def trigger_scattering(self):
        """按S键触发的手动散射效果"""
        if not self.is_scattering:
            self.is_scattering = True
            image_paths = [
                'nju.jpg','seu.jpg','hhu.jpg','nnu.jpg','njtu.jpg','njau.jpg','njfu.jpg']

            # 如果图片不存在则创建彩色方块
            for i in range(6):
                try:
                    img = pygame.image.load(image_paths[i]).convert_alpha()
                    img = pygame.transform.scale(img, (60, 60))
                except:
                    img = pygame.Surface((60, 60), pygame.SRCALPHA)
                    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                    img.fill(color)

                self.scattering_images.append(
                    ScatteringImage(self.rect.centerx, self.rect.centery, img)
                )

    def trigger_game_end_scattering(self):
        """游戏结束时触发的散射效果"""
        if not self.game_end_scattering:
            self.game_end_scattering = True
            self.fading = True  # 玩家淡出

            # 创建7个方向的散射对象
            image_paths = [
                'nju.jpg','seu.jpg','hhu.jpg','nnu.jpg','njtu.jpg','njau.jpg','njfu.jpg' ]

            for i in range(7):
                try:
                    img = pygame.image.load(image_paths[i]).convert_alpha()
                    img = pygame.transform.scale(img, (100, 100))
                except:
                    img = pygame.Surface((100, 100), pygame.SRCALPHA)
                    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                    img.fill(color)

                angle = 2 * math.pi * i / 7
                obj = {
                    'image': img,
                    'angle': angle,
                    'speed': 2,
                    'distance': 0,
                    'max_distance': 300,
                    'x': self.rect.centerx - 50,
                    'y': self.rect.centery - 50,
                    'active': True
                }
                self.scattering_objects.append(obj)

    def update(self):
        # 移动控制
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

        if self.moving_to_center:
            # 缓慢向中心移动（每帧移动2像素）
            # if self.rect.centery > self.target_y:
            #     self.rect.centery -= 2

            if self.rect.centery != self.target_y or self.rect.centerx != self.target_x:
                d_x=self.rect.centerx - self.target_x
                d_y=self.rect.centery - self.target_y
                step_x = 2 * d_x / np.sqrt(d_x**2+d_y**2)
                step_y = 2 * d_y / np.sqrt(d_x ** 2 + d_y ** 2)
                self.rect.centerx-=step_x
                self.rect.centery-=step_y
                # 检查是否到达中心（允许一定误差）
                if abs(d_x) < 2 and abs(d_y) < 2:
                    self.rect.center = (self.target_x, self.target_y)
                    self.moving_to_center = False
                    # self.trigger_game_end_scattering()  # 到达后触发散射
                    Disassembly_of_Yangda(self.rect.centerx, self.rect.centery, 100)
            else:
                self.moving_to_center = False
                Disassembly_of_Yangda(self.rect.centerx, self.rect.centery, 100)
                # self.trigger_game_end_scattering()  # 到达后触发散射

        # 手动散射更新
        if self.is_scattering:
            for img in self.scattering_images[:]:
                if not img.update():
                    self.scattering_images.remove(img)
            if not self.scattering_images:
                self.is_scattering = False

        # 游戏结束散射更新
        if self.game_end_scattering:
            for obj in self.scattering_objects[:]:
                if obj['active'] and obj['distance'] < obj['max_distance']:
                    obj['x'] += math.cos(obj['angle']) * obj['speed']
                    obj['y'] += math.sin(obj['angle']) * obj['speed']
                    obj['distance'] += obj['speed']
                else:
                    obj['active'] = False
                    self.scattering_objects.remove(obj)

        # 淡出效果
        if self.fading and self.alpha > 0:
            self.alpha = max(0, self.alpha - 2)
            self.image = self.original_image.copy()
            self.image.set_alpha(self.alpha)


class ScatteringImage:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.lifetime = random.randint(60, 120)  # 帧数
        self.current_life = 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # 重力效果
        self.current_life += 1
        return self.current_life < self.lifetime

    def draw(self, surface):
        surface.blit(self.image, (self.x - 30, self.y - 30))


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, color, name, score, size, mediumSpeed):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.image.fill((*color, 128))
        text = font.render(name, True, PURPLE)
        text_rect = text.get_rect(center=(size // 2, size // 2))
        self.image.blit(text, text_rect)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - size)
        self.rect.y = -size
        self.speed = random.randint(mediumSpeed - 1, mediumSpeed + 1)
        self.score = score

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Obstacle_1(Obstacle):
    def __init__(self):  # 三江师范学堂
        super().__init__(WHITE, '1902', 2,50,5)
class Obstacle_2(Obstacle):  # 两江师范学堂
    def __init__(self):
        super().__init__(WHITE, '1906', 2,50,5)
class Obstacle_3(Obstacle):  # 南京高等师范学校
    def __init__(self):
        super().__init__(WHITE, '1910', 3,50,5)
class Obstacle_4(Obstacle):  # 国立东南大学
    def __init__(self):
        super().__init__(WHITE, '1921', 3,50,5)
class Obstacle_5(Obstacle):  # 国立中央大学
    def __init__(self):
        super().__init__(WHITE, '1928', 5,50,5)
class Obstacle_6(Obstacle):  # 西迁重庆
    def __init__(self):
        super().__init__(WHITE, '1937', 5,50,5)
class Obstacle_7(Obstacle):  # 国立南京大学
    def __init__(self):
        super().__init__(WHITE, '1949', 3,50,5)
class Obstacle_8(Obstacle):  # 解体QAQ
    def __init__(self):
        super().__init__(WHITE, '1952', 0,50,5)
class Obstacle_9(Obstacle):  # 交大西迁
    def __init__(self):
        super().__init__(WHITE, '1956', 0,50,5)
class Obstacle_10(Obstacle):  # 科大诞生
    def __init__(self):
        super().__init__(WHITE, '1958', 0,50,5)
class Obstacle_11(Obstacle):
    def __init__(self):
        super().__init__(WHITE, '1952', 0,150,3)
class Obstacle_12(Obstacle):
    def __init__(self):
        super().__init__(WHITE, '1956', 0,150,3)
class Obstacle_13(Obstacle):
    def __init__(self):
        super().__init__(WHITE, '1958', 0,150,3)


def after_100_score():
    """得分达到100后生成的障碍物"""
    for _ in range(30):
        obstacle = random.choice([Obstacle_11, Obstacle_12, Obstacle_13])()
        obstacle.rect.x = random.randint(0, SCREEN_WIDTH - obstacle.rect.width)
        obstacle.rect.y = random.randint(-200, -obstacle.rect.height)
        all_sprites.add(obstacle)
        obstacles.add(obstacle)


def game_loop():
    global game_over, round_completed, last_obstacle, score

    # 初始化游戏状态
    all_sprites.empty()
    obstacles.empty()
    player = Player()
    all_sprites.add(player)
    score = 0
    game_over = False
    round_completed = False
    last_obstacle = pygame.time.get_ticks()

    clock = pygame.time.Clock()
    running = True

    while running:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # 按S键触发手动散射
                    player.trigger_scattering()

        if not game_over:
            # 游戏逻辑更新
            all_sprites.update()

            # 障碍物生成
            now = pygame.time.get_ticks()
            if now - last_obstacle > OBSTACLE_FREQ:
                obstacle = random.choice([
                    Obstacle_1, Obstacle_2, Obstacle_3, Obstacle_4, Obstacle_5,
                    Obstacle_6, Obstacle_7, Obstacle_8, Obstacle_9, Obstacle_10
                ])()
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
                last_obstacle = now

            # 碰撞检测
            collided_obstacles = pygame.sprite.spritecollide(player, obstacles, True)
            for obstacle in collided_obstacles:
                score += obstacle.score
                if isinstance(obstacle, (Obstacle_8, Obstacle_9, Obstacle_10)):
                    if score < 1:
                        game_over = True
                        game_result = """很遗憾,你家央大解体了，你再也见不到他了哦~""" #目前失败的字样是无法正常显示的，成功的可以
                        player.moving_to_center = True  # 开始移动

                elif score >= 1:   # 为方便调试分数改为了1，可再调整
                    round_completed = True
                    after_100_score()
                    player.moving_to_center = True  # 开始移动

        # 绘制
        screen.fill(WHITE)
        all_sprites.draw(screen)

        # 绘制手动散射效果
        if player.is_scattering:
            for img in player.scattering_images:
                img.draw(screen)

        # 绘制游戏结束散射效果
        if player.game_end_scattering:
            for obj in player.scattering_objects:
                if obj['active']:
                    screen.blit(obj['image'], (obj['x'], obj['y']))

        # 显示分数
        score_text = font.render(f"分数: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # 游戏结束显示
        if round_completed:
            text = "你赢了!你家央大已经爱死你啦~~~\n\n恭喜进入下一回合!"
            draw_multiline_text(screen, chinese_font, text, BLACK, SCREEN_WIDTH // 2 - 240, SCREEN_HEIGHT // 2 - 50)
        pygame.display.flip()


        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    game_loop()