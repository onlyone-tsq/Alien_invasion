#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : ship.py
# @Author: TSQ
# @Date  : 2018/9/1

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_settings,screen):
        #初始化飞船 并设置其初始位置
        super(Ship,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载飞船图形
        self.image = pygame.image.load('images/ship.bmp')
        #获取飞船的外接矩形
        self.rect = self.image.get_rect()
        #获取屏幕的外接矩形
        self.screen_rect = screen.get_rect()
        #print(self.rect)

        #将飞船置于屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #在飞船center属性中存储小数值
        self.center = float(self.rect.centerx)

        #移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        #根据移动标准调整飞船位置
        if self.moving_right and self.rect.right < self.screen_rect.right:
            #向右移动飞船且在屏幕内
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            # 向左移动飞船且在屏幕内
            self.center -= self.ai_settings.ship_speed_factor

        #根据center更新rect值
        self.rect.centerx = self.center

    def blitme(self):
        #在指定位置绘制飞船
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        #让飞船在屏幕上居中
        self.center = self.screen_rect.centerx