import pendulum
import pygame
import random
import numpy as np
import os
from copy import deepcopy

def blur_surface(surface, amount=4):
    """Fast blur by scaling down and back up."""
    if amount < 1:
        return surface

    w, h = surface.get_size()
    scaled = pygame.transform.smoothscale(surface, (w // amount, h // amount))
    return pygame.transform.smoothscale(scaled, (w, h))

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
    start = pendulum.DoublePend(133,266,1,2,0.01,0.01,0,0)
    dp = deepcopy(start)

    sim_acc = 2
    speed = 1
    clock = pygame.time.Clock()

    lines = [(cwidth//2,cheight//2)]
    lines.append((lines[-1][0] + dp.l1*np.sin(dp.a1), lines[-1][1] - dp.l1*np.cos(dp.a1)))
    lines.append(lines[-1])
    lines.append((lines[-1][0]+dp.l2*np.sin(dp.a2), lines[-1][1] - dp.l2*np.cos(dp.a2)))
    blur = True
    arial = pygame.font.SysFont('Arial',20)
    frame = pygame.Surface((cwidth,cheight),pygame.SRCALPHA)
    energy_text = True
    while running:
        lines = [(cwidth//2,cheight//2)]
        lines.append((lines[-1][0] + dp.l1*np.sin(dp.a1), lines[-1][1] - dp.l1*np.cos(dp.a1)))
        lines.append(lines[-1])
        lines.append((lines[-1][0]+dp.l2*np.sin(dp.a2), lines[-1][1] - dp.l2*np.cos(dp.a2)))
        frame.fill((220,220,220,220),special_flags=pygame.BLEND_RGBA_MULT)
        #frame = blur_surface(frame, 3)
        pygame.draw.lines(frame,(255,255,255),False,lines,5)
        if blur:
            window.blit(frame,(0,0))
        else:
            pygame.draw.lines(window,(255,255,255),False,lines,5)
        if energy_text:
            window.blit(arial.render(f"Total Energy: {dp.E} J",True,(255,255,255)),(0,0))
        pygame.display.update()
        ms = clock.tick(144)
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
                    window = pygame.display.set_mode((fWIDTH,fHEIGHT) if fullscreen else (WIDTH, HEIGHT))
                    cwidth, cheight = (fWIDTH,fHEIGHT) if fullscreen else (WIDTH, HEIGHT)
                    frame = pygame.Surface((cwidth,cheight),pygame.SRCALPHA)
                elif event.key == pygame.K_r:
                    dp = deepcopy(start)
                    dp.a1 = random.uniform(0,2*np.pi)
                    dp.a2 = random.uniform(0,2*np.pi)
                elif event.key == pygame.K_b:
                    blur ^= 1
                elif event.key == pygame.K_e:
                    energy_text ^= 1
if __name__ == "__main__":
    main()
    quit()