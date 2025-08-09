import random
import pygame
import math

LEAF_COLORS = [(255, 165, 0), (222, 184, 135), (255, 99, 71), (200, 80, 50)]  # 橙、棕黄、红、深红

class Leaf(pygame.sprite.Sprite):
    def __init__(self, target:pygame.Surface, WIDTH_LIMIT:int, HIGHT_LIMIT:int):
        pygame.sprite.Sprite.__init__(self)
        self.target_surface = target
        self.x = float(random.randint(0, WIDTH_LIMIT))
        self.y = float(random.randint(-100, -10))  # 从屏幕顶部外生成
        self.size = random.randint(8, 15)
        self.color = random.choice(LEAF_COLORS)
        
        # 物理属性
        self.speed_y = random.uniform(0.5, 2.0)  # 垂直下落速度
        self.speed_x = random.uniform(-0.5, 0.5)  # 水平漂移速度
        self.oscillation_amplitude = random.uniform(0.5, 2.0)  # 摆动幅度
        self.oscillation_frequency = random.uniform(0.02, 0.05)  # 摆动频率
        self.rotation_speed = random.uniform(-2, 2)  # 旋转速度
        self.rotation = random.uniform(0, 360)  # 初始旋转角度
        
        # 形状变化属性
        self.shape_change_speed = random.uniform(0.5, 2.0)  # 形状变化速度
        self.shape_change_phase = random.uniform(0, 2 * math.pi)  # 形状变化相位
        self.fold_amount = 0  # 折叠程度 (0-1)
        self.flip_state = False  # 翻转状态
        
        # 创建更真实的叶子形状
        self.image = self.create_leaf_image()
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        self.HIGHT_LIMIT = HIGHT_LIMIT
        
        # 摆动偏移量
        self.oscillation_offset = random.uniform(0, 2 * math.pi)
        
        # 时间追踪
        self.last_update_time = 0
        
    def create_leaf_image(self, fold_amount:float=0, flip_state=False):
        """创建更真实的叶子形状，支持折叠和翻转效果"""
        # 使用一个更复杂的形状来表示叶子
        leaf_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        
        if flip_state:
            # 翻转状态：绘制简化形状
            # 叶子主体（翻转后的扁平形状）
            pygame.draw.ellipse(leaf_surface, self.color, 
                              (self.size // 2, self.size * 0.5, self.size, self.size * 0.8))
            
            # 叶柄
            pygame.draw.line(leaf_surface, (101, 67, 33), (self.size, self.size * 1.2), 
                           (self.size, self.size * 1.5), 2)
        else:
            # 正常状态：绘制完整叶子形状
            # 根据折叠程度调整叶子形状
            leaf_height = self.size * 1.5 * (1 - fold_amount * 0.3)  # 折叠时叶子变短
            leaf_width = self.size * (1 + fold_amount * 0.2)  # 折叠时叶子变宽
            
            # 叶子主体（椭圆形）
            pygame.draw.ellipse(leaf_surface, self.color, 
                              (self.size // 2 - (leaf_width - self.size) / 2, 
                               self.size * 0.2, leaf_width, leaf_height))
            
            # 叶柄
            stem_length = self.size * 0.3 * (1 - fold_amount * 0.5)  # 折叠时叶柄变短
            pygame.draw.line(leaf_surface, (101, 67, 33), 
                           (self.size, self.size * 0.2 + leaf_height), 
                           (self.size, self.size * 0.2 + leaf_height + stem_length), 2)
            
            # 叶脉（只在未完全折叠时显示）
            if fold_amount < 0.7:
                vein_intensity = 1 - fold_amount  # 折叠时叶脉变淡
                vein_color = (
                    int(139 * vein_intensity), 
                    int(69 * vein_intensity), 
                    int(19 * vein_intensity)
                )
                
                # 主叶脉
                pygame.draw.line(leaf_surface, vein_color, 
                               (self.size, self.size * 0.5), 
                               (self.size, self.size * 0.2 + leaf_height * 0.8), 1)
                
                # 横向叶脉
                if fold_amount < 0.5:
                    pygame.draw.line(leaf_surface, vein_color,
                                   (self.size * 0.7, self.size * 0.8), 
                                   (self.size * 1.3, self.size * 0.8), 1)
                    pygame.draw.line(leaf_surface, vein_color,
                                   (self.size * 0.7, self.size * 1.1), 
                                   (self.size * 1.3, self.size * 1.1), 1)
        
        return leaf_surface
    
    def update(self, current_time) -> None:
        # 计算时间差，用于平滑动画
        if self.last_update_time == 0:
            self.last_update_time = current_time
            
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # 避免过大的时间差导致的跳跃
        if delta_time > 100:  # 如果超过100ms，限制为16ms（约60FPS）
            delta_time = 16
            
        # 基于时间的运动计算，确保平滑性
        time_factor = delta_time / 16.0  # 以16ms为基准
        
        # 更新垂直位置
        self.y += self.speed_y * time_factor
        
        # 添加水平摆动效果（基于时间）
        self.x += self.oscillation_amplitude * math.sin(current_time * 0.001 * self.oscillation_frequency + self.oscillation_offset) * time_factor
        
        # 添加水平漂移
        self.x += self.speed_x * time_factor
        
        # 更新旋转角度
        self.rotation += self.rotation_speed * time_factor
        if self.rotation > 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation += 360
            
        # 更新形状变化参数
        # 折叠程度基于时间变化
        self.fold_amount = (math.sin(current_time * 0.001 * self.shape_change_speed + self.shape_change_phase) + 1) / 2
        # 翻转状态基于时间变化
        self.flip_state = math.sin(current_time * 0.001 * self.shape_change_speed * 0.7 + self.shape_change_phase) > 0.5
        
        # 创建新的叶子图像，包含形状变化效果
        self.original_image = self.create_leaf_image(self.fold_amount, self.flip_state)
        # 旋转图像
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        
        # 更新矩形位置
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        
        # 更新精确位置
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        # 如果叶子超出屏幕底部，则移除
        if self.y > self.HIGHT_LIMIT + 50:
            self.kill()
