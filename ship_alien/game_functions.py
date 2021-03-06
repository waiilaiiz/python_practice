import sys

import pygame
from time import sleep
from bullet import Bullet

from alien import Alien

def check_keydown_evets(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_LEFT:
        ship.move_left = True
    elif event.key == pygame.K_RIGHT:
        ship.move_right = True
    elif event.key == pygame.K_UP:
        ship.move_top = True
    elif event.key == pygame.K_DOWN:
        ship.move_bottom = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_LEFT:
        ship.move_left = False
    elif event.key == pygame.K_RIGHT:
        ship.move_right = False
    elif event.key == pygame.K_UP:
        ship.move_top = False
    elif event.key == pygame.K_DOWN:
        ship.move_bottom = False


def check_events(ai_setting, screen, ship, bullets):
    """响应按键和键盘事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_evets(event, ai_setting, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def update_screen(ai_settings, screen, ship, bullets, aliens):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    pygame.display.flip()

def update_aliens(ai_settings, stats, screen, aliens, ship, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        print("ship hit")
        ship_hit(ai_settings, stats, screen, aliens, ship, bullets)
    check_aliens_bottom(aliens, stats, screen, ship, aliens, bullets)

def update_bullets(ai_settings, screen,ship, aliens, bullets):
    bullets.update()
    collisions = pygame.sprite.groupcollide(aliens, bullets, True, True)
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def ship_hit(ai_settings, stats, screen, aliens, ship, bullets):
    '''响应被外星人撞到的飞船'''
    if stats.ships_left > 0:
        # 将ships_left减1
        stats.ships_left -= 1

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(1)
    else:
        stats.game_active = False



def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    alien_number_x = get_number_aliens_x(ai_settings, alien.rect.width)
    alinen_number_rows = get_number_aliens_y(ai_settings, ship.rect.height, alien.rect.height)
    for alien_number_y in range(alinen_number_rows):
        for alien_number in range(alien_number_x):
            create_aline(ai_settings, screen, aliens, alien_number, alien_number_y)

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_aliens_y(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height + ship_height))
    number_alien_y = int(available_space_y / (2 * alien_height))
    return number_alien_y

def create_aline(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)

    alien_width = alien.rect.width
    alien_height = alien.rect.height

    alien.x = alien_width + 2 * alien_width * alien_number
    alien.y = alien_height + 2 * alien_height * row_number

    alien.rect.x = alien.x
    alien.rect.y = alien.y

    aliens.add(alien)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_speed
    ai_settings.alien_fleet_direct *= -1

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    '''检查是否有外星人到达了屏幕底端'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break





