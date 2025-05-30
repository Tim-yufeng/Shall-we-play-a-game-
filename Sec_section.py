import pygame
import random
import matplotlib



# 设置屏幕尺寸
SCREEN_WIDTH = 1200
SCREEN_HEIGHT =1000 #感觉1000*800还是有点太大了
# SCREEN_WIDTH = 1000
# SCREEN_HEIGHT =800 #感觉1000*800还是有点太大了

def sec_section():
# 初始化Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # 设置中文字体
    chinese_font = pygame.font.Font(r"Fonts_Package_fc12b50164b107e5d087c5f0bbbf6d82\SimHei\simhei.ttf", 36)
# 设置游戏标题
    pygame.display.set_caption("你是中央家族的吗？")

# 定义颜色
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    PURPLE = (105, 43, 128)
    GREY = (163, 163, 173)
    BLUE=(0,0,255)
    GREEN=(0, 128, 0)
    YELLOW=(255, 255, 0)

# 设置时钟
    clock = pygame.time.Clock()

# 设置字体
    font = pygame.font.Font(None, 36)

# 游戏结束标志
    game_over = False
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("nju.jpg").convert_alpha()
            self.image = pygame.transform.scale(self.image, (150, 150))
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
        def __init__(self,color,name,score):
            super().__init__()
            self.image = pygame.Surface((50, 50))
            self.image.fill(color)   # 设定颜色

       # 设置文字
            font = pygame.font.Font(None, 24)  # 使用默认字体，字号为24
            text = font.render(name, True, BLACK)  # 渲染文字，颜色为白色
            text_rect = text.get_rect(center=(25, 25))  # 将文字居中
            self.image.blit(text, text_rect)  # 将文字绘制到障碍物的图像上

            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = -self.rect.height
            self.speed = random.randint(4, 7) # 设置下落速度区间
            self.score = score  # 障碍物的分值
        def update(self):
            self.rect.y += self.speed
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()

    class njuObstacle(Obstacle):  #南京大学障碍物
        def __init__(self):
                super().__init__(PURPLE,'NJU',5)
    class seuObstacle(Obstacle):  # 东南大学障碍物
        def __init__(self):
                super().__init__(YELLOW,'SEU',5)
    class hhuObstacle(Obstacle):  # 河海大学障碍物
        def __init__(self):
                super().__init__(BLUE,'HHU',3)
    class nnuObstacle(Obstacle):  #南京师范大学障碍物
        def __init__(self):
                super().__init__(GREEN,'NNU',3)
    class njtuObstacle(Obstacle):  # 南京工业大学障碍物
        def __init__(self):
                super().__init__(GREY,'NJTU',2)
    class njauObstacle(Obstacle):  # 南京农业大学障碍物
        def __init__(self):
                super().__init__(GREEN,'NJAU',2)
    class njfuObstacle(Obstacle):  # 南京林业大学障碍物
        def __init__(self):
                super().__init__(GREEN,'NJFU',2)


    class njmuObstacle(Obstacle):  # 南京医科大学障碍物
        def __init__(self):
                super().__init__(BLUE,'NJMU',-3)

    class njuptObstacle(Obstacle):  # 南京邮电大学障碍物
        def __init__(self):
                super().__init__(BLUE,'NJUPT',-2)

    class njustObstacle(Obstacle):  # 南京理工大学障碍物
        def __init__(self):
                super().__init__(PURPLE,'NJUST',-4)
    class nuaaObstacle(Obstacle):  # 南京航空航天大学障碍物
        def __init__(self):
                super().__init__(BLUE,'NUAA',-4)


    def draw_multiline_text(surface, font, text, color, x, y, line_height=40):
        """渲染多行文本（支持 `\n`）"""
        for i, line in enumerate(text.splitlines()):  # 按 `\n` 分割
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (x, y + i * line_height)
            surface.blit(text_surface, text_rect)


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
    score=10 # 初始积分
    running = True

    matplotlib.rcParams['font.family'] = 'SimHei'
    matplotlib.rcParams['axes.unicode_minus'] = False

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
                obstacle_type = random.choice([njuObstacle,
                                               seuObstacle,
                                               njfuObstacle,
                                               nuaaObstacle,
                                               njustObstacle,
                                               njtuObstacle,
                                               njauObstacle,
                                               njmuObstacle,
                                               njuptObstacle,
                                               nnuObstacle,
                                               hhuObstacle])
                obstacle = obstacle_type()
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
                last_obstacle = now

            collided_obstacles = pygame.sprite.spritecollide(player, obstacles, True)  # 碰撞后障碍物消失
            for obstacle in collided_obstacles:
                score += obstacle.score  # 更新积分
                if score <= 0:
                    game_over = True
                    game_result = "很遗憾你输了\n\n（好好复习一下央大历史吧傻狍子bushi）"  # 积分降到 0 分，输掉游戏
                elif score >= 100:
                    game_over = True
                    game_result = "你赢了!你真是太了解央大历史了！"  # 积分达到 100 分，获胜

        # 绘制画面
            screen.fill(WHITE)
            all_sprites.draw(screen)

            # 显示积分
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))


        else:
    # 显示游戏结果 - 使用中文字体
            draw_multiline_text(screen, chinese_font, game_result, BLACK, SCREEN_WIDTH // 2 - 240, SCREEN_HEIGHT // 2 - 50)
            # result_text = chinese_font.render(game_result, True, BLACK)
            # screen.blit(result_text, (
            # SCREEN_WIDTH // 2 - result_text.get_width() // 2, SCREEN_HEIGHT // 2 - result_text.get_height() // 2))


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

if __name__ == '__main__':
    sec_section()
# else:
#     pygame.init()
#     chinese_font = pygame.font.Font(r"Fonts_Package_fc12b50164b107e5d087c5f0bbbf6d82\SimHei\simhei.ttf", 36)
#     SCREEN_WIDTH = 800
#     SCREEN_HEIGHT = 600
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))