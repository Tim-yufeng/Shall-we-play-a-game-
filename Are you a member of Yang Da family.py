import pygame
import random
import matplotlib.pyplot as plt
import matplotlib
import textwrap
plt.figure()
# 设置中文字体
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False


text = ("欢迎来玩小游戏“你是央家的吗”，在这里你可以快速了解游戏规则\n"
        "你将通过左右键操作下方的红色方块向左向右移动，接住那些掉下来的南京高校，但是高校名都是英文简写哦，你熟悉南京高校的英文简写吗\n"
        "\n不是每个高校都可以接哦，你只有接住那些央家的高校才能获得分数，接错了会倒扣分数哦。\n"
        "\n（对了，每个高校对应积分的绝对值可能和该学校实力正相关哦）。\n"
        "\n你在刚开始拥有10分，达到50分你就赢啦！但是如果分数减至0分你就失败喽。\n"
        "\n准备好了吗？关闭这个窗口，让我们开始吧！")
wrapped_text = textwrap.fill(text, width=40)

# 在整个图形上居中（0.5, 0.5 表示正中间）
plt.figtext(
    0.5, 0.5, wrapped_text,
    ha='center', va='center',
    bbox=dict(facecolor='white', alpha=0.8),
    fontsize=10,
)

plt.show()
# 初始化Pygame
pygame.init()
# 在初始化Pygame后，设置中文字体
# 替换下面的路径为实际的中文字体文件路径
chinese_font = pygame.font.Font(r"C:\Users\金御风\PycharmProjects\Shall-we-play-a-game\Fonts_Package_fc12b50164b107e5d087c5f0bbbf6d82\SimHei\simhei.ttf", 36)  # 如果没有字体文件，可以尝试系统自带字体

# 设置屏幕尺寸
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 设置游戏标题
pygame.display.set_caption("你是央家的吗")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PURPLE = (105, 43, 128)  # 修正颜色值
GREY = (163, 163, 173)   # 修正颜色值
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
        self.speed = random.randint(3, 5)
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
class njnuObstacle(Obstacle):  #南京师范大学障碍物
    def __init__(self):
            super().__init__(GREEN,'NJNU',3)
class njtuObstacle(Obstacle):  # 南京工业大学障碍物
    def __init__(self):
            super().__init__(GREY,'NJTU',2)
class njauObstacle(Obstacle):  # 南京农业大学障碍物
    def __init__(self):
            super().__init__(GREEN,'NJAU',2)
class njfuObstacle(Obstacle):  # 南京农业大学障碍物
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
                                           njnuObstacle,
                                           hhuObstacle])
            obstacle = obstacle_type()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)
            last_obstacle = now

        # # 检测碰撞
        # if pygame.sprite.spritecollide(player, obstacles, False):
        #     game_over = True
            # 检测碰撞
        collided_obstacles = pygame.sprite.spritecollide(player, obstacles, True)  # 碰撞后障碍物消失
        for obstacle in collided_obstacles:
            score += obstacle.score  # 更新积分
            if score <= 0:
                game_over = True
                game_result = "很遗憾你输了（好好复习一下央大历史吧傻狍子 bushi）"  # 积分降到 0 分，输掉游戏
            elif score >= 50:
                game_over = True
                game_result = "你赢了!你真是太了解央大历史了！"  # 积分达到 50 分，获胜

        # 绘制画面
        screen.fill(WHITE)
        all_sprites.draw(screen)

        # 显示积分
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))


    else:
# 显示游戏结果 - 使用中文字体
        result_text = chinese_font.render(game_result, True, BLACK)
        screen.blit(result_text, (
        SCREEN_WIDTH // 2 - result_text.get_width() // 2, SCREEN_HEIGHT // 2 - result_text.get_height() // 2))


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

