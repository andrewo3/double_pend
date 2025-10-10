import pendulum
import pygame
import numpy as np
import os


def main():
    WIDTH = 720
    HEIGHT = 1280
    fWIDTH = 1080
    fHEIGHT = 1920
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    running = True

    cwidth = WIDTH
    cheight = HEIGHT
    fullscreen = False
    dp = pendulum.DoublePend(200,200,1,1,-0.5,0,0,0)

    clock = pygame.time.Clock()

    lines = [(cwidth//2,cheight//2)]
    lines.append((lines[-1][0] + dp.l1*np.sin(dp.a1), lines[-1][1] - dp.l1*np.cos(dp.a1)))
    lines.append(lines[-1])
    lines.append((lines[-1][0]+dp.l2*np.sin(dp.a2), lines[-1][1] - dp.l2*np.cos(dp.a2)))

    while running:
        lines = [(cwidth//2,cheight//2)]
        lines.append((lines[-1][0] + dp.l1*np.sin(dp.a1), lines[-1][1] - dp.l1*np.cos(dp.a1)))
        lines.append(lines[-1])
        lines.append((lines[-1][0]+dp.l2*np.sin(dp.a2), lines[-1][1] - dp.l2*np.cos(dp.a2)))
        pygame.draw.lines(window,(255,255,255),False,lines,5)
        pygame.display.update()
        ms = clock.tick(60)
        for m in range(ms):
            dp.update(t=0.001)
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

if __name__ == "__main__":
    main()
    quit()