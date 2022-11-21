import sys
import pygame
from pygame.locals import *

# 색상 세팅(RGB코드)
RED = (255, 0, 0)
ORANGE = (255, 153, 51)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
SEAGREEN = (60, 179, 113)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
VIOLET = (204, 153, 255)
PINK = (255, 153, 153)


FPS = 30
fpsClock = pygame.time.Clock()

pygame.init()


screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
screen.fill(WHITE)

pygame.display.set_caption('Pygame Window')


# 폰트 설정
font = pygame.font.SysFont('Tahoma', 60)  # 기본 폰트 및 사이즈 설정(폰트1)
small_font = pygame.font.SysFont('Malgun Gothic', 20)  # 작은 사이즈 폰트(폰트2)
game_over = font.render("Press R to restart", True, BLACK)  # 게임 종료시 문구

imgActive = pygame.image.load('./res/800/imgActive.png')  # Normal Image
imgNormal = pygame.image.load('./res/800/imgNormal.png')  # Grayscale image

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # if ESC key is pressed, exit the game
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    screen.blit(imgNormal, (0, 0))  # Grayscale image

    # print fps round 0.00
    fps = font.render(str(round(fpsClock.get_fps(), 2)), True, BLACK)
    screen.blit(fps, (0, 0))

    pygame.display.update()
    fpsClock.tick(FPS)
