import random
import sys

import pygame

from autumn_walk.leaf_sprite import Leaf
from .character_sprite import CharacterSprite

# 初始化pygame
pygame.init()
pygame.mixer.init()  # 初始化音频

# 屏幕设置（氛围：宽屏更适合散步感）
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("秋日散步")

# 背景类，用于处理视差滚动效果
class ParallaxBackground:
    def __init__(self, image_path, screen_width, screen_height):
        self.image = pygame.image.load(image_path).convert()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_width = self.image.get_width()
        self.bg_height = self.image.get_height()
        
        # 计算背景图片需要重复的次数
        self.bg_tiles_x = (self.screen_width // self.bg_width) + 2
        self.bg_tiles_y = (self.screen_height // self.bg_height) + 1
        
        # 视差滚动参数
        self.scroll_x = 0
        self.scroll_speed = 0.5  # 视差滚动速度（比角色移动慢）
        
    def update(self, player_direction):
        # 根据角色移动方向更新背景滚动
        self.scroll_x += player_direction * self.scroll_speed
        
        # 重置滚动位置以实现循环效果
        if self.scroll_x >= self.bg_width:
            self.scroll_x = 0
        elif self.scroll_x <= -self.bg_width:
            self.scroll_x = 0
            
    def draw(self, surface):
        # 绘制背景图片（实现视差滚动效果）
        for y in range(self.bg_tiles_y):
            for x in range(self.bg_tiles_x):
                pos_x = (x * self.bg_width) + int(self.scroll_x)
                pos_y = self.screen_height - self.bg_height
                surface.blit(self.image, (pos_x, pos_y))

# 创建背景实例
background = ParallaxBackground("asset/Background/bg1.png", SCREEN_WIDTH, SCREEN_HEIGHT)

# 主角设置
protagonist = CharacterSprite(screen, 
                    SCREEN_WIDTH,
                    "asset/Prototype_Character/prototype_character.png", 
                    "asset/Extra/static_shadow.png",
                    "sound/footstep.mp3",
                    SCREEN_WIDTH // 2, 
                    SCREEN_HEIGHT - 36, # 地面位置
                    32, 32, # 角色大小
                    {0: (0, 2), 1: (1, 2), 2:(2, 2), 
                     3:(3, 4), 4:( 4, 4), -4:( 4, 4), 5:( 5, 4), 
                     6:( 6, 2), 7:( 7, 2), 8:( 8, 2), 
                     9:( 9, 3), 10:( 10, 3), 11:( 11, 3)})   
actors = pygame.sprite.Group()
actors.add(protagonist)

# 落叶效果
leaves = pygame.sprite.Group()

def main():
    # 游戏主循环
    clock = pygame.time.Clock()
    running = True

    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # 空格捡落叶（无实际功能，纯氛围交互）
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("捡起了一片落叶 🍂")  # 实际可加动画
        
        # 获取按键状态以确定角色移动方向
        # keys = pygame.key.get_pressed()
        # player_direction = 0
        # if keys[pygame.K_a]:
        #     player_direction = -1
        # elif keys[pygame.K_d]:
        #     player_direction = 1
            
        # 更新背景（根据角色移动方向）
        # background.update(player_direction)
        
        # 绘制背景
        background.draw(screen)
        
        # 更新角色
        actors.update(pygame.time.get_ticks())

        # 绘制角色
        actors.draw(screen)
        
        # 落叶生成与绘制
        if random.random() < 0.05:  # 控制落叶密度
            leaves.add(Leaf(screen, SCREEN_WIDTH, SCREEN_HEIGHT))
        leaves.update(pygame.time.get_ticks())
        leaves.draw(screen)

        protagonist.action()
        
        # 刷新屏幕
        pygame.display.flip()
        clock.tick(60)  # 控制帧率，保持流畅

    pygame.quit()
    sys.exit()
