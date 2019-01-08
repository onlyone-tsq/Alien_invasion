#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : game_functions.py
# @Author: TSQ
# @Date  : 2018/9/1

import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    # 响应按下
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_x:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    # 响应松开
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, ship, bullets,play_button,stats,aliens,sb):
    # 响应键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_paly_button(stats, play_button, mouse_x, mouse_y, aliens, ship, bullets, ai_settings,screen, sb)

def check_paly_button(stats,play_button,mouse_x,mouse_y,aliens,ship,bullets,ai_settings,screen,sb):
    #在玩家单击play时，游戏开始
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏速度
        ai_settings.initialize_dynamic_settings()

        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.reset_stat()
        stats.game_active = True

        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #清空外星人和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

def update_screen(ai_settings, screen, ship, aliens, bullets,play_button,stats,sb):
    # 更新屏幕上图像，并切换新屏幕
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    #如果游戏处于非活动状态，就绘制play
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(bullets,aliens,ship,ai_settings,screen,stats,sb):
    # 更新子弹位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(bullets,aliens,ship,ai_settings,screen,stats,sb)

def check_bullet_alien_collisions(bullets,aliens,ship,ai_settings,screen,stats,sb):
    #检查是否有子弹击中外星人，若击中则删除相应子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)

    #检查collisions来更新得分
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_scores * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        #加快游戏节奏
        ai_settings.increase_speed()

        #提高等级
        stats.level +=1
        sb.prep_level()

        create_fleet(ai_settings, screen, aliens, ship)    

def fire_bullet(ai_settings, screen, ship, bullets):
    # 创建一颗子弹，将其加入编组bullets
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_alien_x(ai_settings, alien_width):
    # 获得每行能容纳的外星人数 
    # 计算单个外星人占据的宽度，包括自身宽度和间距，这里间距也等于外星人宽度
    number_aliens_x = int(
        (ai_settings.screen_width - 2 * alien_width) / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    #获取整个屏幕能容纳多少行外星人
    #计算整个屏幕的有效空间
    available_space_y = ai_settings.screen_height - ship_height - 3 * alien_height
    number_rows =  int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,number_rows):
    #创建一个外星人，并放在当前行
    # 每个外星人的宽度，高度
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.y = alien.rect.height + 2 * alien.rect.height * number_rows
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)

def create_fleet(ai_settings, screen, aliens, ship):
    # 创建外星人群
    # 获得每行能容纳的外星人数
    alien = Alien(ai_settings,screen) 
    number_aliens_x = get_number_alien_x(ai_settings,alien.rect.width)
    #获取整个屏幕能容纳多少行外星人
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

    # 根据屏幕容纳行数和每行容纳数量，创建外星人
    for alien_row in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 创建一个外星人并加入当前行
            create_alien(ai_settings,screen,aliens,alien_number,alien_row)

def check_fleet_edges(ai_settings,aliens):
    #当外星人到达边缘时，采取相应措施
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    #将外星人整体下移，并改变左右移动方向
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_speed
    ai_settings.move_direction *= -1 

def ship_hit(ai_settings,screen,aliens,ship,bullets,stats,sb):
    #响应被外星人撞到的飞船
    stats.ships_stat -= 1
    sb.prep_ships()

    if stats.ships_stat > 0:
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并将飞船置于屏幕底部中央
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, aliens, ship, bullets, stats,sb):
    #检查是否有外星人到了底部
    screen_rect = screen.get_rect()
    for alien in aliens:
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞到一样处理
            ship_hit(ai_settings, screen, aliens, ship, bullets, stats, sb)
            break

def update_aliens(ai_settings,aliens,ship,screen,bullets,stats,sb):
    #检查外星人是否处于边缘，并更新整群外星人的位置
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #检测外星人和飞船的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings, screen, aliens, ship, bullets, stats, sb)
        #print("Ship hit!!!")

    check_aliens_bottom(ai_settings, screen, aliens, ship, bullets, stats,sb)

def check_high_score(stats,sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
