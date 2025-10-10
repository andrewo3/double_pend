import pendulum
import pygame
import numpy as np
import os
from copy import deepcopy


def main():
    pygame.init()
    WIDTH = 720
    HEIGHT = 1280
    fWIDTH = 1080
    fHEIGHT = 1920
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    running = True

    cwidth = WIDTH
    cheight = HEIGHT
    fullscreen = False
    start = pendulum.DoublePend(50,150,1,3,0,np.pi/2,0,0)
    dp = deepcopy(start)

    sim_acc = 2
    speed = 1
    clock = pygame.time.Clock()

    lines = [(cwidth//2,cheight//2)]
    lines.append((lines[-1][0] + dp.l1*np.sin(dp.a1), lines[-1][1] - dp.l1*np.cos(dp.a1)))
    lines.append(lines[-1])
    lines.append((lines[-1][0]+dp.l2*np.sin(dp.a2), lines[-1][1] - dp.l2*np.cos(dp.a2)))

    arial = pygame.font.SysFont('Arial',20)
    while running:
        lines = [(cwidth//2,cheight//2)]
        lines.append((lines[-1][0] + dp.l1*np.sin(dp.a1), lines[-1][1] - dp.l1*np.cos(dp.a1)))
        lines.append(lines[-1])
        lines.append((lines[-1][0]+dp.l2*np.sin(dp.a2), lines[-1][1] - dp.l2*np.cos(dp.a2)))
        pygame.draw.lines(window,(255,255,255),False,lines,5)
        window.blit(arial.render(f"Total Energy: {dp.E} J",True,(255,255,255)),(0,0))
        pygame.display.update()
        ms = clock.tick(60)
        for m in range(sim_acc*speed*ms):
            dp.update(t=0.001/sim_acc)
        window.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    fullscreen ^= 1
                    if fullscreen:
                        os.environ['SDL_VIDEO_CENTERED'] = '1'
                        os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
                    window = pygame.display.set_mode((fWIDTH,fHEIGHT) if fullscreen else (WIDTH, HEIGHT),fullscreen*pygame.NOFRAME)
                    cwidth, cheight = (fWIDTH,fHEIGHT) if fullscreen else (WIDTH, HEIGHT)
                if event.key == pygame.K_r:
                    dp = deepcopy(start)
if __name__ == "__main__":
    main()
    quit()