# 角色动画
import pygame

class CharacterSprite(pygame.sprite.Sprite):
    def __init__(self, target, 
                        screen_width:int,
                        image_file:str,
                        shadow_image_file:str,
                        sound_file:str,
                        x:int, y:int, 
                        width:int=32, height:int=32, 
                        states_list:dict[int,tuple[int, int]]={}, 
                        current_status:int=0):
        """
        Args:
            target (pygame.Surface): 目标表面
            image_file (str): 图像文件路径
            x (int): 初始x坐标
            y (int): 初始y坐标
            width (int, optional): 图像宽度. Defaults to 32.
            height (int, optional): 图像高度. Defaults to 32.
            states_list (dict[int,tuple[int, int]], optional): 状态列表. Defaults to {}. (status_index, (row, frames))
            current_status (int, optional): 当前状态. Defaults to 0.
        """
        pygame.sprite.Sprite.__init__(self)
        self.target_surface = target
        self.screen_width = screen_width
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.p_x = x
        self.p_y = y
        self.t_x = x
        self.t_y = y
        self.frame_width = width
        self.frame_height = height
        self.master_image = pygame.image.load(image_file).convert_alpha()
        self.states_list = states_list
        self.current_status = current_status
        self.last_time = 0
        self.frame = 0
        self.frame = 0
        self.old_frame = -1
        self.player_speed = 3

        # 加载脚步声效（只加载一次）
        self.footstep_sound = pygame.mixer.Sound(sound_file)
        self.footstep_sound.set_volume(0.5)  # 设置音量为50%
        self.footstep_channel = pygame.mixer.Channel(0)  # 获取第一个通道
        
        # 加载阴影图像
        self.shadow_image = pygame.image.load(shadow_image_file).convert_alpha()
        

    def set_status(self, status:int):
        self.current_status = status
        self.frame = 0
        self.last_time = pygame.time.get_ticks()
    
    def move_to(self, delta_x:int, delta_y:int):
        if abs(self.p_x - self.t_x) < 10:
            if delta_x > 0:
                self.set_status(4)
            elif delta_x < 0:
                self.set_status(-4)
            self.t_x += delta_x
            self.p_y += delta_y
    
    def play_footstep(self):
        # 只有当通道没有在播放时才播放新的脚步声
        if not self.footstep_channel.get_busy():
            self.footstep_channel.play(self.footstep_sound)

    def update(self, current_time, rate=60):
        if current_time > self.last_time + rate:
            self.frame = (self.frame + 1) % self.states_list[self.current_status][1]
            self.last_time = current_time

        if self.frame != self.old_frame:            
            # 检查是否到达目标
            if abs(self.p_x - self.t_x) <= 1:
                self.p_x = self.t_x
                self.p_y = self.t_y
                self.set_status(0)
            else:
                # 播放脚步声
                self.play_footstep()
                # 移动角色
                _delta_x = (self.t_x - self.p_x) // 6
                if _delta_x == 0:
                    self.p_x = self.t_x
                self.p_x += _delta_x
                
            frame_x = self.frame * self.frame_width
            frame_y = self.states_list[self.current_status][0] * self.frame_height
            clip_rect = ( frame_x, frame_y, self.frame_width, self.frame_height )
            if self.master_image:
                _image = self.master_image.subsurface(clip_rect)
                if self.current_status < 0:
                    _image = pygame.transform.flip(_image, True, False)
                self.image = pygame.Surface((self.frame_width, self.frame_height + 2), pygame.SRCALPHA)
                self.image.blit(self.shadow_image, (0, 2))
                self.image.blit(_image, (0, 0))
            self.old_frame = self.frame
            self.rect.x = self.p_x - self.frame_width // 2
    
    def get_direction(self):
        # 获取角色移动方向
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.p_x > self.frame_width:
            return -1
        elif keys[pygame.K_d] and self.p_x < self.screen_width - self.frame_width:
            return 1
        return 0
    
    def action(self):
        # 主角移动
        direction = self.get_direction()
        if direction == -1:
            self.move_to(-self.player_speed, 0)
        elif direction == 1:
            self.move_to(self.player_speed, 0)