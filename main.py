import pendulum
import pygame
import numpy as np


def main():
    WIDTH = 800
    HEIGHT = 600
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    running = True

    dp = pendulum.DoublePend(50,150,1,1,-0.1,0,0,0)

    clock = pygame.time.Clock()

    lines = [(WIDTH//2,HEIGHT//2)]
    lines.append((lines[-1][0] + dp.l1*np.sin(dp.a1), lines[-1][1] - dp.l1*np.cos(dp.a1)))
    lines.append(lines[-1])
    lines.append((lines[-1][0]+dp.l2*np.sin(dp.a2), lines[-1][1] - dp.l2*np.cos(dp.a2)))

    while running:
        lines = [(WIDTH//2,HEIGHT//2)]
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




if __name__ == "__main__":
    main()
    quit()