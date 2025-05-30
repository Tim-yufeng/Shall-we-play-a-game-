import pygame
import numpy as np

def Disassembly_of_Yangda(x, y, image_size):
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("央大解体动画")
    clock = pygame.time.Clock()

    # 颜色定义
    PURPLE = (105, 43, 128)

    # 加载中心图片（ncu.jpg），如果不存在则创建紫色方块
    try:
        center_img = pygame.image.load("ncu.jpg").convert_alpha()
        center_img = pygame.transform.scale(center_img, (150, 150))
    except:
        center_img = pygame.Surface((image_size, image_size), pygame.SRCALPHA)
        center_img.fill(PURPLE)

    center_rect = center_img.get_rect(center=(screen_width // 2, screen_height // 2))
    center_alpha = 255  # 初始透明度（完全不透明）

    # 加载7张散射图片
    image_files = [
        'nju.jpg','seu.jpg','hhu.jpg','nnu.jpg','njtu.jpg','njau.jpg','njfu.jpg'
    ]

    images = []
    for filename in image_files:
        try:
            img = pygame.image.load(filename).convert_alpha()
            img = pygame.transform.scale(img, (image_size, image_size))
            images.append(img)
        except:
            print(f"图片加载失败: {filename}")

    class MovingImage:
        def __init__(self, image, angle):
            self.image = image
            self.angle = angle  # 移动角度（弧度）
            self.speed = 2  # 移动速度
            self.max_distance = 200  # 最大移动距离
            self.distance = 0  # 已移动距离
            self.x = screen_width // 2 - image_size // 2  # 初始x位置
            self.y = screen_height // 2 - image_size // 2  # 初始y位置
            self.active = False  # 是否激活
            self.start_time = 0  # 激活时间
            self.delay = 200  # 每张图片出现的延迟时间（毫秒）

        def update(self, current_time, whether_nju):
            if not self.active and current_time >= self.start_time:
                self.active = True

            if self.active and self.distance < self.max_distance:
                self.x += np.cos(self.angle) * self.speed
                self.y += np.sin(self.angle) * self.speed
                self.distance += self.speed
            if current_time>=3000 and whether_nju==True:
                if self.y != screen_height//2 or self.x != screen_width//2:
                    d_x = self.x - screen_width//2
                    d_y = self.y - screen_height//2
                    step_x = 2 * d_x / np.sqrt(d_x ** 2 + d_y ** 2)
                    step_y = 2 * d_y / np.sqrt(d_x ** 2 + d_y ** 2)
                    self.x -= step_x
                    self.y -= step_y
                    # 检查是否到达中心（允许一定误差）
                    if abs(d_x) < 0.5 and abs(d_y) < 0.5:
                        self.x,self.y = (screen_width//2,screen_height//2)

        def draw(self, surface):
            if self.active:
                surface.blit(self.image, (self.x, self.y))


    # 创建7个移动图片对象
    moving_images = []
    for i in range(7):
        angle = 2 * np.pi * i / 7  # 均匀分布的角度
        img = MovingImage(images[i], angle)
        img.start_time = i * 200  # 延迟启动
        moving_images.append(img)

    running = True
    start_time = pygame.time.get_ticks()

    while running:
        current_time = pygame.time.get_ticks() - start_time

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 更新散射图片
        for img in moving_images:
            img.update(current_time,False)

        # 计算中心图片的透明度（随时间递减）
        if current_time < 1400:  # 7张图片×200ms=1400ms
            # 线性减少透明度，从255到0
            center_alpha = max(0, 255 - int(current_time / 1400 * 255))
            center_img.set_alpha(center_alpha)
        elif current_time>=3000:   # 中心图片基本完全透明
            # pygame.time.delay(1000)
            for i in range(1,7):
                images[i].set_alpha(max(0, 255 - int((current_time-3000) / 1400 * 255)))     # 除了nju全都原地消失[doge]


            moving_images[0].update(current_time,True)
        # 绘制
        screen.fill(PURPLE)

        # 绘制中心图片（在最底层）
        if center_alpha > 0:
            screen.blit(center_img, center_rect)

        # 绘制散射图片（在上层）
        for img in moving_images:
            img.draw(screen)

        pygame.display.flip()
        clock.tick(60)



    pygame.quit()


if __name__ == '__main__':
    Disassembly_of_Yangda(400, 300, 100)  # 示例调用
