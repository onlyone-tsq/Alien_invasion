#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-05 01:15:02
# @Author  : TSQ (812227146@qq.com)
# @Link    : ${link}
# @Version : $Id$

import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    #显示得分信息

    def __init__(self,ai_settings,screen,stats):
        #初始化得分相关属性
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        #得分信息的字体
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)

        #构造得分和最高分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        #将得分以1,000,000形式显示，并转换为图像
        rounded_score = int(round(self.stats.score,-1)) 
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)

        #将得分图像放在右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        #将最高分以1,000,000形式显示，并转换为图像
        high_score = int(round(self.stats.high_score,-1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.ai_settings.bg_color)

        #将最高分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        #将等级渲染成图像
        self.level_image = self.font.render(str(self.stats.level),True,self.text_color,self.ai_settings.bg_color)

        #将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        #显示还剩下多少飞船
        self.ships = Group()
        for ship_number in range(self.stats.ships_stat):
            ship = Ship(self.ai_settings,self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        #在屏幕上显示得分
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)


