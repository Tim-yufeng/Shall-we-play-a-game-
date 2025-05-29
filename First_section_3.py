import pygame
import random
import math
from Sec_section import SCREEN_HEIGHT, SCREEN_WIDTH, sec_section

# 初始化颜色和字体
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (105, 43, 128)

# 全局变量
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
game_over = False
round_completed = False
OBSTACLE_FREQ = 500  # 障碍物生成间隔（毫秒）
last_obstacle = 0
score = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("ncu.jpg").convert_alpha()
            self.image = pygame.transform.scale(self.image, (150, 150))
        except pygame.error as e:
            print(f"无法加载图片: {e}")
            self.image = pygame.Surface((150, 150))
            self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5
        self.alpha=255
        self.fading=False
        self.particles = []  # 粒子容器
        self.fading_particles = False
        self.scattering_images = []

    def NCU_fading(self):
        self.fading=True
        self.fading_particles = True
        image_paths = ["nju.png","University/hhu.jpg", "University/njau.jpg", "University/njfu.jpg", "University/njtu.jpg", "University/nnu.jpg", "University/seu.jpg"]
        for i in range(6):
            self.scattering_images.append(ScatteringImage(self.rect.centerx, self.rect.centery, image_paths[i]))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if self.fading and self.alpha > 0:
            self.alpha=max(0,self.alpha-5)
            self.image.set_alpha(self.alpha)
            if random.random() < 1:
                self.particles.append(DisappearParticle(
                    self.rect.centerx + random.randint(-20, 20),
                    self.rect.centery + random.randint(-20, 20)
                ))
            for img in self.scattering_images:
                img.update()
        self.particles = [p for p in self.particles if p.update()]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, color, name, score, size, mediumSpeed):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.image.fill((*color, 128))  # RGBA，A=128（半透明）
        font = pygame.font.Font(None, size//2)
        text = font.render(name, True, PURPLE)
        text_rect = text.get_rect(center=(size//2, size//2))
        self.image.blit(text, text_rect)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(mediumSpeed-1, mediumSpeed+1)
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

class DisappearParticle:
    def __init__(self, x, y, color=PURPLE):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.color = color

        # 随机运动方向
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(0.5, 3)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        # 生命周期（随机）
        self.lifetime = random.randint(20, 40)
        self.current_life = 0

    def update(self):
        """更新粒子状态"""
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # 重力
        self.current_life += 1
        self.alpha = 255 - int((self.current_life / self.lifetime) * 255)
        self.size = max(0.5, self.size * 0.97)  # 粒子逐渐缩小
        return self.current_life < self.lifetime and self.size > 0.5

    def draw(self, surface):
        """绘制粒子"""
        if self.alpha > 0:
            # 创建带透明度的表面
            particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                particle_surface,
                (*self.color, self.alpha),
                (self.size, self.size),
                self.size
            )
            surface.blit(particle_surface, (int(self.x) - self.size, int(self.y) - self.size))


class ScatteringImage:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))  # 调整图片大小
        except:
            self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
            self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 128))

        # 随机运动方向
        angle = random.uniform(0, math.pi * 2)
        self.speed = random.uniform(2, 5)
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed

        # 旋转相关
        self.rotation = 0
        self.rotation_speed = random.uniform(-5, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # 轻微重力效果
        self.rotation += self.rotation_speed
        return True  # 始终存在，不自动消失

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.image, self.rotation)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        surface.blit(rotated_image, rect)

def draw_multiline_text(surface, font, text, color, x, y, line_height=40):
    """渲染多行文本（支持 `\n`）"""
    for i, line in enumerate(text.splitlines()):  # 按 `\n` 分割
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y + i * line_height)
        surface.blit(text_surface, text_rect)

def after_100_score():
    occupied_positions = []  # 记录已占用位置
    for _ in range(30):
        obstacle_type = random.choice([Obstacle_11, Obstacle_12, Obstacle_13])
        obstacle = obstacle_type()
        maxattempts=500 # 分散障碍物的尝试次数
        i=0
        # 随机位置，直到不与其他障碍物重叠
        while i<=maxattempts:
            obstacle.rect.x = random.randint(0, SCREEN_WIDTH - obstacle.rect.width)
            obstacle.rect.y = random.randint(-200, -obstacle.rect.height)  # 从顶部外生成
            i+=1
            # 检查是否与已有障碍物重叠
            if not any(obstacle.rect.colliderect(pygame.Rect(x, y, 200, 200)) for (x, y) in occupied_positions):
                occupied_positions.append((obstacle.rect.x, obstacle.rect.y))
                break
        all_sprites.add(obstacle)
        obstacles.add(obstacle)


def fir_section():
    global game_over, round_completed, OBSTACLE_FREQ, last_obstacle, score
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    chinese_font = pygame.font.Font(r"Fonts_Package_fc12b50164b107e5d087c5f0bbbf6d82\SimHei\simhei.ttf", 36)
    pygame.display.set_caption("京华风云")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # 重置游戏状态
    all_sprites.empty()
    obstacles.empty()
    player = Player()
    all_sprites.add(player)
    score = 0
    game_over = False
    round_completed = False
    last_obstacle = pygame.time.get_ticks()

    # 新增变量：用于过渡阶段计时
    transition_start_time = None
    transition_duration = 4000  # 过渡阶段持续时间（毫秒）

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

        if not game_over and pygame.display.get_init():
            screen.fill(WHITE)
            all_sprites.update()

            if not round_completed:
                # 正常游戏阶段的障碍物生成
                now = pygame.time.get_ticks()
                if now - last_obstacle > OBSTACLE_FREQ:
                    obstacle_type = random.choice([Obstacle_1, Obstacle_2, Obstacle_3, Obstacle_4, Obstacle_5,
                                                   Obstacle_6, Obstacle_7, Obstacle_8, Obstacle_9, Obstacle_10])
                    obstacle = obstacle_type()
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
                            game_result = """很遗憾,你家央大解体了，你再也见不到他了哦~"""
                    elif score >= 1:
                        round_completed = True
                        transition_start_time = pygame.time.get_ticks()
                        after_100_score()

            else:
                # 过渡阶段（round_completed = True）
                now = pygame.time.get_ticks()
                if now - transition_start_time >= transition_duration:
                    running = False
                    sec_section()  # 进入下一回合
                collided_obstacles = pygame.sprite.spritecollide(player, obstacles, True)
                for obstacle in collided_obstacles:
                    if isinstance(obstacle, (Obstacle_11, Obstacle_12, Obstacle_13)):
                        player.NCU_fading()

            for particle in player.particles:
                particle.draw(screen)

            # 绘制所有精灵
            all_sprites.draw(screen)

            if player.fading:
                for img in player.scattering_images:
                    img.draw(screen)

            # 显示分数
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))

            # 在过渡阶段显示"恭喜进入下一回合"
            if round_completed:
                text = "你赢了!你家央大已经爱死你啦~~~\n\n恭喜进入下一回合!"
                draw_multiline_text(screen, chinese_font, text, BLACK, SCREEN_WIDTH // 2 - 240, SCREEN_HEIGHT // 2 - 50)
            pygame.display.flip()


        elif game_over:
            # 游戏结束处理
            screen.fill(WHITE)
            result_text = chinese_font.render(game_result, True, BLACK)
            screen.blit(result_text, (SCREEN_WIDTH // 2 - result_text.get_width() // 2,
                                      SCREEN_HEIGHT // 2 - result_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    fir_section()