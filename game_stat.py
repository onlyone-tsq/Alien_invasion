#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-01 20:27:42
# @Author  : TSQ (812227146@qq.com)
# @Link    : ${link}
# @Version : $Id$

class GameStats():
#统计游戏信息
    def __init__(self,ai_settings):
        #初始化统计信息
        self.ai_settings = ai_settings
        self.reset_stat()
        #游戏刚启动时game_active为True
        self.game_active = False
        #最高分不能随便重置
        self.high_score = 0
        self.level = 1

    def reset_stat(self):
    #初始化游戏运行期间可能变化的统计信息
        self.ships_stat = self.ai_settings.ship_limit
        self.score = 0