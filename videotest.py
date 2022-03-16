import imageio as iio
import pygame



pygame.init()

usefull = False
dw = 1200
dh = 980

clock = pygame.time.Clock()


if __name__ == '__main__':
    if usefull:
        gameDisplay = pygame.display.set_mode((dw, dh), pygame.FULLSCREEN,pygame.RESIZABLE )
        s = pygame.display.get_window_size()
        dw = s[0]
        dh = s[1]
    else:
        gameDisplay = pygame.display.set_mode((dw, dh),pygame.RESIZABLE)
    s = pygame.display.get_window_size()
    dw = s[0]
    dh = s[1]
    pygame.display.set_caption('GUI Tests')

reader = iio.get_reader('imageio:cockatoo.mp4')
for i, im in enumerate(reader):
    #print(im)
    #print("#")
    gameDisplay.fill((0,0,0))
    surf = pygame.surfarray.make_surface(im)
    #print(surf)
    gameDisplay.blit(surf,surf.get_rect())
    pygame.display.flip()
    clock.tick(60)
