#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : alien_invasion.py
# @Author: TSQ
# @Date  : 2018/9/1

#import sys

import pygame

from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stat import GameStats 
from button import Button
from scoreboard import Scoreboard
#from alien import Alien

def run_game():
    #初始化pygame、设置和屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #创建play按钮
    play_button = Button(screen,"play")
    #创建一个用于存储游戏统计信息的实例,并显示记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)

    #创建一个飞船、子弹、外星人的编组
    ship = Ship(ai_settings,screen)
    bullets = Group()
    aliens = Group()

    #创建外星人人群
    gf.create_fleet(ai_settings,screen,aliens,ship)

    #开始游戏的主循环
    while True:
        #监视键盘和鼠标事件
        gf.check_events(ai_settings,screen,ship,bullets, play_button,stats,aliens,sb)

        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets,aliens,ship,ai_settings,screen,stats,sb)
            gf.update_aliens(ai_settings,aliens,ship,screen,bullets,stats,sb)

        # 更新屏幕上图像，并切换新屏幕
        gf.update_screen(ai_settings,screen,ship,aliens,bullets,play_button,stats,sb)

run_game()