#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : settings.py
# @Author: TSQ
# @Date  : 2018/9/1

class Settings():
    """存储外星人入侵游戏的所有类"""

    def __init__(self):
        """初始化游戏设置"""
        #屏幕设置
        self.screen_width = 1320
        self.screen_height = 720
        self.bg_color = (230,230,230)

        #飞船碰撞次数设置
        self.ship_limit = 3

        #子弹设置
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed =3

        #外星人上下移动速度
        self.alien_drop_speed = 10

        #游戏节奏加快速度
        self.speedup_scale = 1.1

        #外星人分数提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        #游戏进度  初始化的设置
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        #move_direction为1表示右移，为-1表示左移
        self.move_direction = 1

        #分数
        self.alien_scores = 50

    def increase_speed(self):
        #游戏提高速度设置
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale


        self.alien_scores = int(self.alien_scores * self.score_scale)
        #print(self.alien_scores)