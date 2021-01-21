import pygame
import copy
import random

weight = 10
height = 20
cells = 35
res = 350, 700
pygame.display.set_caption('Тетрис')
programIcon = pygame.image.load('ikon.png')
pygame.display.set_icon(programIcon)

pygame.init()
screen = pygame.display.set_mode(res)
clock = pygame.time.Clock()

setka = [pygame.Rect(x * cells, y * cells, cells, cells) for x in range(weight) for y in range(height)]

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + weight // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, cells - 2, cells - 2)
zero = [[0 for i in range(weight)] for j in range(height)]

score = 0
fps = 60
limit = 2000
figure = copy.deepcopy(random.choice(figures))
score_2 = 0



def borders():
    if figure[i].x < 0 or figure[i].x > weight - 1:
        return False
    elif figure[i].y > height - 1 or zero[figure[i].y][figure[i].x]:
        return False
    return True


running = True

while running:
    dx = 0
    rotate = False
    screen.fill((40, 40, 40))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                limit = 120
            elif event.key == pygame.K_UP:
                rotate = True

    copy_figure = copy.deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not borders():
            figure = copy.deepcopy(copy_figure)
            break
    if score_2 > 10000:
        score_2 = 0
        fps += 30
    score += fps
    score_2 += fps
    if score > limit:
        score = 0
        score_2 += 1
        copy_figure = copy.deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not borders():
                for i in range(4):
                    zero[copy_figure[i].y][copy_figure[i].x] = (170, 170, 170)
                figure = copy.deepcopy(random.choice(figures))
                limit = 2000
                break

    center = figure[0]
    copy_figure = copy.deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not borders():
                figure = copy.deepcopy(copy_figure)
                break

    line = height - 1
    for row in range(height - 1, -1, -1):
        count = 0
        for i in range(weight):
            if zero[row][i]:
                count += 1
            zero[line][i] = zero[row][i]
        if count < weight:
            line -= 1

    [pygame.draw.rect(screen, (40, 40, 40), i_rect, 1) for i_rect in setka]

    for i in range(4):
        figure_rect.x = figure[i].x * cells
        figure_rect.y = figure[i].y * cells
        pygame.draw.rect(screen, (255, 165, 0), figure_rect)

        for j, raw in enumerate(zero):
            for _, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = _ * cells, j * cells
                    pygame.draw.rect(screen, col, figure_rect)

    for i in range(weight):
        if zero[0][i]:
            exit()

    pygame.display.flip()
    clock.tick(60)
