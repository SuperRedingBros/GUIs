#import imageio as iio
import pygame
from moviepy.editor import VideoFileClip
#from playsound import playsound

import threading
import time

import numpy as np
import pygame as pg

from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip


pg.init()
pg.display.set_caption("MoviePy")


def imdisplay(imarray, screen=None):
    """Splashes the given image array on the given pygame screen."""
    a = pg.surfarray.make_surface(imarray.swapaxes(0, 1))
    if screen is None:
        screen = pg.display.set_mode(imarray.shape[:2][::-1])
    screen.blit(a, (0, 0))
    pg.display.flip()

def frame(t,screen,clip,t0):
    img = clip.get_frame(t)

    t1 = time.time()
    time.sleep(max(0, t - (t1 - t0)))
    imdisplay(img, screen)

def mypreview(
        clip,
        fps=15,
        audio=True,
        audio_fps=22050,
        audio_buffersize=3000,
        audio_nbytes=2,
        surface=None
        ):
    if surface == None:
        return None
    screen = surface

    audio = audio and (clip.audio is not None)

    if audio:
        # the sound will be played in parallel. We are not
        # parralellizing it on different CPUs because it seems that
        # pygame and openCV already use several cpus it seems.

        # two synchro-flags to tell whether audio and video are ready
        video_flag = threading.Event()
        audio_flag = threading.Event()
        # launch the thread
        audiothread = threading.Thread(
            target=clip.audio.preview,
            args=(audio_fps, audio_buffersize, audio_nbytes, audio_flag, video_flag),
        )
        audiothread.start()

    img = clip.get_frame(0)
    #imdisplay(img, screen)
    if audio:  # synchronize with audio
        video_flag.set()  # say to the audio: video is ready
        audio_flag.wait()  # wait for the audio to be ready

    result = []

    t0 = time.time()
    return np.arange(1.0 / fps, clip.duration - 0.001, 1.0 / fps)


pygame.init()

usefull = False

clock = pygame.time.Clock()

vclip = VideoFileClip('guis/assets/087 DIVE Algebra 2 3rd Edition R2.mp4')
looping = True
#print(soundclip)
inc=0
dw = vclip.w
dh = vclip.h
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
out = mypreview(vclip, fps=15, audio=True, audio_fps=22050, audio_buffersize=3000, audio_nbytes=2, surface=gameDisplay)
print(out)
t0 = time.time()
for t in out:
    frame(t,gameDisplay,vclip,t0)
