import pygame
import random
import matplotlib
from Sec_section import SCREEN_HEIGHT,SCREEN_WIDTH,sec_section

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (105, 43, 128)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("ncu.jpg").convert_alpha()
            self.image = pygame.transform.scale(self.image, (150, 150))
        except pygame.error as e:
            print(f"无法加载图片: {e}")
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
    def __init__(self, color, name, score):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)  # 设定颜色

        # 设置文字
        font = pygame.font.Font(None, 24)  # 使用默认字体，字号为24
        text = font.render(name, True, PURPLE)  # 渲染文字，颜色为白色
        text_rect = text.get_rect(center=(25, 25))  # 将文字居中
        self.image.blit(text, text_rect)  # 将文字绘制到障碍物的图像上

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(4, 6)  # 设置下落速度区间
        self.score = score  # 障碍物的分值

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Obstacle_1(Obstacle):
    def __init__(self):  # 三江师范学堂
        super().__init__(WHITE, '1902', 2)


class Obstacle_2(Obstacle):  # 两江师范学堂
    def __init__(self):
        super().__init__(WHITE, '1906', 2)


class Obstacle_3(Obstacle):  # 南京高等师范学校
    def __init__(self):
        super().__init__(WHITE, '1910', 3)


class Obstacle_4(Obstacle):  # 国立东南大学
    def __init__(self):
        super().__init__(WHITE, '1921', 3)


class Obstacle_5(Obstacle):  # 国立中央大学
    def __init__(self):
        super().__init__(WHITE, '1928', 5)


class Obstacle_6(Obstacle):  # 西迁重庆
    def __init__(self):
        super().__init__(WHITE, '1937', 5)


class Obstacle_7(Obstacle):  # 国立南京大学
    def __init__(self):
        super().__init__(WHITE, '1949', 3)


class Obstacle_8(Obstacle):  # 解体QAQ
    def __init__(self):
        super().__init__(WHITE, '1952', 0)


class Obstacle_9(Obstacle):  # 交大西迁
    def __init__(self):
        super().__init__(WHITE, '1956', 0)


class Obstacle_10(Obstacle):  # 科大诞生
    def __init__(self):
        super().__init__(WHITE, '1958', 0)

all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
game_over = False
round_completed = False

def fir_section():
    global game_over
    global round_completed

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    chinese_font = pygame.font.Font(r"Fonts_Package_fc12b50164b107e5d087c5f0bbbf6d82\SimHei\simhei.ttf", 36)
    pygame.display.set_caption("京华风云")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)


    # 初始化玩家
    player = Player()
    all_sprites.add(player)

    # 设置障碍物生成时间
    OBSTACLE_FREQ = 500  # 每500毫秒生成一个障碍物
    last_obstacle = pygame.time.get_ticks()
    # 游戏主循环
    score=0
    running = True

    matplotlib.rcParams['font.family'] = 'SimHei'
    matplotlib.rcParams['axes.unicode_minus'] = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            all_sprites.update()

            now = pygame.time.get_ticks()
            if now - last_obstacle > OBSTACLE_FREQ:
                obstacle_type = random.choice([Obstacle_1,Obstacle_2,Obstacle_3,Obstacle_4,Obstacle_5,Obstacle_6,Obstacle_7,Obstacle_8,Obstacle_9,Obstacle_10])
                obstacle = obstacle_type()
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
                last_obstacle = now

            collided_obstacles = pygame.sprite.spritecollide(player, obstacles, True)  # 碰撞后障碍物消失
            for obstacle in collided_obstacles:
                score += obstacle.score
                if isinstance(obstacle, (Obstacle_8, Obstacle_9,Obstacle_10)):
                    # if score >= 1:  # 如果分数达到100，进入下一回合
                    #     round_completed = True
                    #     game_result = "恭喜进入下一回合!"
                    #     result_text = chinese_font.render(game_result, True, BLACK)
                    #     screen.blit(result_text, (
                    #         SCREEN_WIDTH // 2 - result_text.get_width() // 2,
                    #         SCREEN_HEIGHT // 2 - result_text.get_height() // 2))
                    #     sec_section()
                    if score >= 1:
                        round_completed = True
                        game_result = "恭喜进入下一回合!"
                        result_text = chinese_font.render(game_result, True, BLACK)
                        screen.blit(result_text, (SCREEN_WIDTH // 2 - result_text.get_width() // 2,
                                                  SCREEN_HEIGHT // 2 - result_text.get_height() // 2))
                        pygame.display.flip()  # 强制更新屏幕显示结果
                        pygame.time.delay(4000)  # 暂停2秒让玩家看到结果
                        running = False  # 退出当前循环
                        sec_section()  # 进入下一回合
                    else:
                        game_over = True
                        game_result = "很遗憾你输了,你家央大就这么解体了，你再也见不到他了哦~"
                        result_text = chinese_font.render(game_result, True, BLACK)
                        screen.blit(result_text, (
                            SCREEN_WIDTH // 2 - result_text.get_width() // 2,
                            SCREEN_HEIGHT // 2 - result_text.get_height() // 2))
                # elif score >= 1:#为了调试方便先把过关分数改成 1 了，如果我后来忘改回去记得把它删掉（）
                #     game_result = "你赢了!你家央大已经爱死你啦~~~"
                #     result_text = chinese_font.render(game_result, True, BLACK)
                #     screen.blit(result_text, (
                #         SCREEN_WIDTH // 2 - result_text.get_width() // 2,
                #         SCREEN_HEIGHT // 2 - result_text.get_height() // 2))
                #     after_100_score()
                elif score >= 1:
                    round_completed = True
                    game_result = "你赢了!你家央大已经爱死你啦~~~"
                    result_text = chinese_font.render(game_result, True, BLACK)
                    screen.blit(result_text, (SCREEN_WIDTH // 2 - result_text.get_width() // 2,
                                              SCREEN_HEIGHT // 2 - result_text.get_height() // 2))
                    pygame.display.flip()
                    pygame.time.delay(1000)
                    after_100_score()
                    pygame.time.delay(6000)
            # 绘制画面
            screen.fill(WHITE)
            all_sprites.draw(screen)

            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))

        else:
            result_text = chinese_font.render(game_result, True, BLACK)
            screen.blit(result_text, (
            SCREEN_WIDTH // 2 - result_text.get_width() // 2, SCREEN_HEIGHT // 2 - result_text.get_height() // 2))


            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                game_over = False
                all_sprites.empty()
                obstacles.empty()
                player = Player()
                all_sprites.add(player)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

def after_100_score():
    global OBSTACLE_FREQ, last_obstacle

        # 加快障碍物生成速度
    # OBSTACLE_FREQ = 100  # 每50毫秒生成一个障碍物
    OBSTACLE_FREQ = 200
    last_obstacle = pygame.time.get_ticks()

        # 立即生成一批Obstacle8/9/10
    for _ in range(100):  # 一次性生成10个负面障碍物
        obstacle_type = random.choice([Obstacle_8, Obstacle_9, Obstacle_10])
        obstacle = obstacle_type()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

if __name__ == '__main__':
    fir_section()