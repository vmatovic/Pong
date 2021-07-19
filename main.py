import pygame
import sys
import math


def check_limits(rect, speed):
    if rect.y >= 0 and rect.y + 35 <= 600:
        return True
    elif rect.y < 0:
        if speed > 0:
            return True
    elif rect.y + 35 > 600:
        if speed < 0:
            return True
    return False


def display_main_menu_text():
    main_menu_surface = game_font.render('Press 1 for Single-player', True, (255, 255, 255))
    screen.blit(main_menu_surface, (200, 240))
    main_menu_surface = game_font.render('Press 2 for Multiplayer', True, (255, 255, 255))
    screen.blit(main_menu_surface, (200, 260))
    main_menu_surface = game_font.render('Press ESC to exit', True, (255, 255, 255))
    screen.blit(main_menu_surface, (200, 280))


def single_play():
    global left_rect, left_speed, right_rect, right_speed, ball, ball_x_speed, ball_y_speed, left_point, right_point

    # Controls
    if check_limits(left_rect, left_speed):
        left_rect.y += left_speed
    if ball.centery > right_rect.centery:
        right_speed = 4.5
    elif ball.centery < right_rect.centery:
        right_speed = -4.5
    else:
        right_speed = 0
    right_rect.y += right_speed

    # Ball movement
    ball.centerx += ball_x_speed
    if ball.centery <= 0 or ball.centery >= 600:
        wall_hit.play()
        ball_y_speed *= -1
    ball.centery += ball_y_speed

    # Ball collision
    if ball.colliderect(left_rect):
        paddle_hit.play()
        res = ball_hit_where(left_rect, ball)
        di = eucl_dist([1, 0], [0, res])
        x_s = 1 / di
        y_s = res / di
        ball_x_speed = x_s * 5
        ball_y_speed = y_s * 5 + 3

    if ball.colliderect(right_rect):
        paddle_hit.play()
        res = ball_hit_where(right_rect, ball)
        di = eucl_dist([-1, 0], [0, res])
        x_s = -1 / di
        y_s = res / di
        ball_x_speed = x_s * 5
        ball_y_speed = y_s * 5 + 3

    if ball.centerx + 7 <= 0 or ball.centerx - 7 >= 600:
        if ball.centerx + 7 <= 0:
            right_point += 1
        else:
            left_point += 1
        point.play()
        pygame.time.delay(1000)
        ball.centerx = 297

    score_display()


def casual_play():
    global left_rect, left_speed, right_rect, right_speed, ball, ball_x_speed, ball_y_speed, left_point, right_point

    # Controls
    if check_limits(left_rect, left_speed):
        left_rect.y += left_speed
    if check_limits(right_rect, right_speed):
        right_rect.y += right_speed

    # Ball movement
    ball.centerx += ball_x_speed
    if ball.centery <= 0 or ball.centery >= 600:
        wall_hit.play()
        ball_y_speed *= -1
    ball.centery += ball_y_speed

    # Ball collision
    if ball.colliderect(left_rect):
        paddle_hit.play()
        res = ball_hit_where(left_rect, ball)
        di = eucl_dist([1, 0], [0, res])
        x_s = 1/di
        y_s = res/di
        ball_x_speed = x_s * 5
        ball_y_speed = y_s * 5 + 3

    if ball.colliderect(right_rect):
        paddle_hit.play()
        res = ball_hit_where(right_rect, ball)
        di = eucl_dist([-1, 0], [0, res])
        x_s = -1 / di
        y_s = res / di
        ball_x_speed = x_s * 5
        ball_y_speed = y_s * 5 + 3

    if ball.centerx + 7 <= 0 or ball.centerx - 7 >= 600:
        if ball.centerx + 7 <= 0:
            right_point += 1
        else:
            left_point += 1
        point.play()
        pygame.time.delay(1000)
        ball.centerx = 297
        ball_y_speed = 5
        if ball_x_speed < 0:
            ball_x_speed = -5
        else:
            ball_x_speed = 5

    score_display()


def draw_dashes():
    for i in range(0, 600, 22):
        dash.y = i
        pygame.draw.rect(screen, white, dash)


def score_display():
    left_score_surface = point_font.render(str(left_point), True, (255, 255, 255))
    left_score_rect = left_score_surface.get_rect(center=(150, 60))
    screen.blit(left_score_surface, left_score_rect)

    right_score_surface = point_font.render(str(right_point), True, (255, 255, 255))
    right_score_rect = right_score_surface.get_rect(center=(450, 60))
    screen.blit(right_score_surface, right_score_rect)


def draw_figures():
    pygame.draw.rect(screen, white, left_rect)
    pygame.draw.rect(screen, white, right_rect)
    pygame.draw.rect(screen, white, ball)
    draw_dashes()


def eucl_dist(l1, l2):
    return math.sqrt((l2[0] - l1[0])**2 + (l2[1] - l1[1])**2)


def ball_hit_where(paddle, ball):
    return abs(paddle.centery - ball.centery) / paddle.height


pygame.mixer.pre_init(frequency=48000, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
game_font = pygame.font.Font('vgafixe.ttf', 30)
point_font = pygame.font.Font('Player1UpBlack-YRDv.ttf', 100)

# Game objects
left_rect = pygame.Rect(10, 300, 7, 40)
right_rect = pygame.Rect(585, 300, 7, 40)
ball = pygame.Rect(297, 45, 7, 7)
dash = pygame.Rect(300, 0, 2, 11)

# Abstract
left_speed = 0
right_speed = 0
left_point = 0
right_point = 0
ball_x_speed = 5
ball_y_speed = -5
game_mode = 0

# Colors
white = (255, 255, 255)

# Sounds
wall_hit = pygame.mixer.Sound('SFX/wall_hit.wav')
paddle_hit = pygame.mixer.Sound('SFX/paddle_hit.wav')
point = pygame.mixer.Sound('SFX/point.wav')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                left_speed = 10
            elif event.key == pygame.K_w:
                left_speed = -10

            if event.key == pygame.K_DOWN and game_mode == 2:
                right_speed = 10
            elif event.key == pygame.K_UP and game_mode == 2:
                right_speed = -10

            if game_mode == 0 and event.key == pygame.K_2:
                game_mode = 2
            if game_mode == 0 and event.key == pygame.K_1:
                game_mode = 1
            if game_mode != 0 and event.key == pygame.K_ESCAPE:
                game_mode = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s or event.key == pygame.K_w:
                left_speed = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                right_speed = 0

    screen.fill((0, 0, 0))

    if game_mode == 0:
        left_point = 0
        right_point = 0
        display_main_menu_text()
    elif game_mode == 1:
        single_play()
        draw_figures()
    elif game_mode == 2:
        casual_play()
        draw_figures()

    pygame.display.update()
    clock.tick(60)
