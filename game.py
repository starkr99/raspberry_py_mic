import pygame
import pyaudio
import numpy as np
import usb.core
import usb.util
from enum import Enum


class EditMode(Enum):
    NONE = 0
    EDIT_MAX_VOLUME = 1


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images
image1 = pygame.image.load('./res/imgNormal.png')
image2 = pygame.image.load('./res/imgActive.png')

# Set up pyaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1,
                rate=44100, input=True, frames_per_buffer=1024)

# Set maximum volume
MAX_VOLUME = 5000

SHOW_FPS = False

EDIT_MODE = EditMode.NONE

# FPS용
bigfont = pygame.font.Font(None, 36)
# EDIT모드 표시용
smallfont = pygame.font.Font(None, 36)

# ESC : 종료
# F1 : 전체화면
# F2 : FPS 표시


def key_down(key):
    if key == pygame.K_ESCAPE:
        running = False
    # if F1 then Fullscreen toggle
    elif key == pygame.K_F1:
        pygame.display.toggle_fullscreen()
    # if F2 then show FPS
    elif key == pygame.K_F2:
        SHOW_FPS = not SHOW_FPS
    elif key == pygame.K_F3:
        EDIT_MODE = EditMode.EDIT_MAX_VOLUME


# Initialize FPS counter
fps_counter = pygame.time.Clock()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            key_down(event.key)

    # Get volume from microphone and calculate as percentage
    data = stream.read(1024, exception_on_overflow=False)
    data = np.fromstring(data, np.int16)
    volume = np.abs(data).mean()
    print(volume)
    volume_percent = int(100 * volume / MAX_VOLUME)
    # Calculate image heights based on volume percentage
    image2_height = int(SCREEN_HEIGHT * volume_percent / 100)
    image1_height = SCREEN_HEIGHT - image2_height
    # Display images
    screen.blit(image1, (0, 0), pygame.Rect(0, 0, SCREEN_WIDTH, image1_height))
    screen.blit(image2, (0, image1_height),
                pygame.Rect(0, image1_height, SCREEN_WIDTH, image2_height))

    if SHOW_FPS:
        fps = bigfont.render(
            str(int(fps_counter.get_fps())), True, (255, 0, 0))
        screen.blit(fps, (0, 0))

    pygame.display.flip()

# Close pyaudio stream and terminate pygame
stream.stop_stream()
stream.close()
p.terminate()
pygame.quit()
