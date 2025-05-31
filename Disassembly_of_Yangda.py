import pygame
import math
def Disassembly_of_Yangda(x,y,image_size):
    # pygame.init()
    # # 设置窗口
    screen_width=800
    screen_height=600
    screen = pygame.display.set_mode((screen_width, screen_height))
    # pygame.display.set_caption("动画示例")
    clock = pygame.time.Clock()  # 用于控制帧率
    # 颜色定义
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    PURPLE=(105,43,128)

    image_files=['nju.jpg','seu.jpg','hhu.jpg','nnu.jpg','njtu.jpg','njau.jpg','njfu.jpg']
    # image=['nju','seu','hhu','nnu','njtu','njau','njfu']

    #图片大小
    image_size=image_size

    # 加载7张图片（这里假设图片名为image1.png到image7.png）
    images = []
    # for i in range(1, 8):
    for filename in image_files:
        try:

            img = pygame.image.load(filename).convert_alpha()
            img = pygame.transform.scale(img, (image_size, image_size))
            images.append(img)
        except:

            print("图片加载失败！")


    # 定义图片类
    class MovingImage:
        def __init__(self, image, angle):
            self.image = image
            self.angle = angle  # 移动角度（弧度）
            self.speed = 2  # 移动速度
            self.max_distance = 200  # 最大移动距离
            self.distance = 0  # 已移动距离
            self.x = screen_width // 2 - image_size//2  # 初始x位置（居中）
            self.y = screen_height // 2 - image_size//2  # 初始y位置（居中）
            self.active = False  # 是否激活
            self.start_time = 0  # 激活时间
            self.delay = 200  # 每张图片出现的延迟时间（毫秒）

        def update(self, current_time):
            # 检查是否应该激活
            if not self.active and current_time >= self.start_time:
                self.active = True

            # 如果激活且还有移动距离，则更新位置
            if self.active and self.distance < self.max_distance:
                self.x += math.cos(self.angle) * self.speed
                self.y += math.sin(self.angle) * self.speed
                self.distance += self.speed

        def draw(self, surface):
            if self.active:
                surface.blit(self.image, (self.x, self.y))


    # 创建7个移动图片对象，每个间隔200毫秒出现
    moving_images = []
    for i in range(7):
        # 计算角度（7个方向均匀分布）
        angle = 2 * math.pi * i / 7
        img = MovingImage(images[i], angle)
        img.start_time = i * 200  # 每张图片延迟200毫秒出现
        moving_images.append(img)

    running = True
    start_time = pygame.time.get_ticks()

    while running:
        current_time = pygame.time.get_ticks() - start_time
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_r:  # 按R键重置动画
            #         start_time = pygame.time.get_ticks()
            #         for i, img in enumerate(moving_images):
            #             img.__init__(images[i], 2 * math.pi * i / 7)
            #             img.start_time = i * 200
            # 更新
        for img in moving_images:
            img.update(current_time)

        # 绘制
        screen.fill(PURPLE)

        # 绘制所有图片（后出现的会覆盖先出现的）
        for img in moving_images:
            img.draw(screen)

        # 显示说明文字
        # font = pygame.font.SysFont(None, 24)
        # text = font.render("按R键重置动画", True, WHITE)
        # screen.blit(text, (10, 10))

        # 更新游戏/动画状态



        pygame.display.flip()  # 更新显示
        clock.tick(60)  # 控制帧率为60FPS
    pygame.quit()
if __name__ == '__main__':
    Disassembly_of_Yangda()