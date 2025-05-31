import pygame
import numpy as np
from Sec_section import SCREEN_HEIGHT,SCREEN_WIDTH,sec_section

def Disassembly_of_Yangda(x, y, image_size):
    global nju_inposition
    nju_inposition = False
    pygame.init()
    chinese_font = pygame.font.Font(r"Fonts_Package_fc12b50164b107e5d087c5f0bbbf6d82\SimHei\simhei.ttf", 36)
    font = pygame.font.Font(None, 36)
    screen_width = 1200
    screen_height = 1000
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("央大解体动画")
    clock = pygame.time.Clock()

    # 颜色定义
    BLACK=(0,0,0)
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

    def draw_multiline_text(surface, font, text, color, x, y, line_height=40):
        """渲染多行文本（支持 `\n`）"""
        for i, line in enumerate(text.splitlines()):  # 按 `\n` 分割
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (x, y + i * line_height)
            surface.blit(text_surface, text_rect)

    class MovingImage:
        def __init__(self, image, angle):
            self.original_image = image  # ✅ 保存原始图片（避免多次缩放失真）
            self.image = image  # 当前显示的图片（动态缩放）
            self.angle = angle  # 移动角度（弧度）
            self.speed = 2  # 移动速度
            self.max_distance = 200  # 最大移动距离
            self.distance = 0  # 已移动距离
            self.x = screen_width // 2 - image_size // 2
            self.y = screen_height // 2 - image_size // 2
            self.active = False  # 是否激活
            self.start_time = 0  # 激活时间
            self.delay = 200  # 每张图片出现的延迟时间（毫秒）

        def update(self, current_time, whether_nju):
            global nju_inposition


            if not self.active and current_time >= self.start_time:
                self.active = True

            if self.active and self.distance < self.max_distance:
                self.x += np.cos(self.angle) * self.speed
                self.y += np.sin(self.angle) * self.speed
                self.distance += self.speed

            if current_time >= 3000 and whether_nju:
                target_Xpostion=screen_width // 2
                target_Ypostion=screen_height // 2
                if (self.x != target_Xpostion) or (self.y != target_Ypostion):
                    d_x = self.x - target_Xpostion
                    d_y = self.y - target_Ypostion
                    d_distance = np.sqrt(d_x ** 2 + d_y ** 2)

                    # 计算移动步长（向中心靠拢）
                    step_x = 2 * d_x / d_distance
                    step_y = 2 * d_y / d_distance
                    self.x -= step_x
                    self.y -= step_y

                    # ✅ 关键修复：动态缩放图片并保存到 self.image
                    scale_factor = 2 * (1 - d_distance / self.max_distance)
                    new_width = int(self.original_image.get_width() * scale_factor)
                    new_height = int(self.original_image.get_height() * scale_factor)
                    self.image = pygame.transform.smoothscale(self.original_image, (new_width, new_height))

                    # 检查是否到达中心（允许误差）
                    if abs(d_x) < 0.5 and abs(d_y) < 0.5:
                        self.x, self.y = target_Xpostion, target_Ypostion
                        nju_inposition=True
                        # text = "恭喜解锁新人物——NJU ！！\n\n 按下Enter进入下一关"
                        # draw_multiline_text(screen, chinese_font, text, BLACK, screen_width // 2 - 240,
                        #                     screen_height // 2 - 50)


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
            if event.type == pygame.KEYDOWN and nju_inposition==True:
                if event.key == pygame.K_RETURN:  # 主键盘回车键
                    sec_section()
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

            if nju_inposition == True:
                text = "恭喜解锁新人物——NJU ！！\n\n 按下Enter进入下一关"
                draw_multiline_text(screen, chinese_font, text, BLACK, screen_width // 2 - 240,
                                    screen_height // 2 - 50)

        # 绘制
        screen.fill(PURPLE)

        # 绘制中心图片（在最底层）
        if center_alpha > 0:
            screen.blit(center_img, center_rect)

        # 绘制散射图片（在上层）
        for img in moving_images:
            img.draw(screen)

        if nju_inposition:
            text = "恭喜解锁新人物——NJU ！！\n\n 按下Enter进入下一关"
            draw_multiline_text(screen, chinese_font, text, BLACK, screen_width // 2-200 , screen_height // 2-200 )

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_RETURN:  # 主键盘回车键
        #         print("主键盘 Enter 被按下！")


        pygame.display.flip()
        clock.tick(60)



    pygame.quit()


if __name__ == '__main__':
    Disassembly_of_Yangda(400, 300, 100)  # 示例调用
