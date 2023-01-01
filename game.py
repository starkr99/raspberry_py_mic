import pygame
import pyaudio
import numpy as np
import usb.core
import usb.util
import json
from enum import Enum


def save_settings(screen_width, screen_height, max_volume, image1Path, image2Path):
    settings_dict = {'screen_width': screen_width, 'screen_height': screen_height,
                     'max_volume': max_volume, 'image1Path': image1Path, 'image2Path': image2Path}
    # Save settings to a JSON file
    with open('settings.json', 'w') as f:
        json.dump(settings_dict, f)


def load_settings():
    try:
        # Load settings from a JSON file
        with open('settings.json', 'r') as f:
            settings_dict = json.load(f)
        return settings_dict
    except FileNotFoundError:
        # Return default settings if file not found
        return {'screen_width': 1024, 'screen_height': 768, 'max_volume': 5000, 'image1Path': './res/imgNormal.png', 'image2Path': './res/imgActive.png'}


settings = load_settings()

SCREEN_WIDTH = settings['screen_width']
SCREEN_HEIGHT = settings['screen_height']
# Set maximum volume
max_volume = settings['max_volume']
image1Path = settings['image1Path']
image2Path = settings['image2Path']

# Initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images
image1 = pygame.image.load(image1Path)
image2 = pygame.image.load(image2Path)

# Set up fonts
# FPS용
normalFont = pygame.font.Font(None, 36)
# End game 표시용
endfont = pygame.font.Font(None, 120)


class EditMode(Enum):
    NONE = 0
    EDIT_MAX_VOLUME = 1


def printGameEnd(screen):
    # Print Game End on center screen
    game_end = endfont.render("Game End", True, (255, 0, 0))
    screen.blit(game_end, (SCREEN_WIDTH / 2 - game_end.get_width() /
                2, SCREEN_HEIGHT / 2 - game_end.get_height() / 2))


# Set up pyaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1,
                rate=44100, input=True, frames_per_buffer=1024)

show_fps = False

edit_mode = 0

# Initialize FPS counter
fps_counter = pygame.time.Clock()
ongame = True
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif ongame == False and event.type == pygame.MOUSEBUTTONUP:
            ongame = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False
            # if F1 then Fullscreen toggle
            elif event.key == pygame.K_F1:
                pygame.display.toggle_fullscreen()
            # if F2 then show FPS
            elif event.key == pygame.K_F2:
                show_fps = not show_fps
            # if F3 then edit max volume
            elif event.key == pygame.K_F3:
                # move to edit_mode to next enum
                edit_mode = edit_mode + 1
                # if edit_mode is bigger than EditMode enum size then reset to NONE
                if edit_mode >= len(EditMode):
                    edit_mode = EditMode.NONE.value
                print(edit_mode)
            elif event.key == pygame.K_F4:
                edit_mode = edit_mode - 1
                # if edit_mode is smaller than EditMode enum size then reset to Maximum enum value
                if edit_mode < 0:
                    edit_mode = (EditMode(len(EditMode) - 1)).value
            elif event.key == pygame.K_F5:
                save_settings(SCREEN_WIDTH, SCREEN_HEIGHT,
                              max_volume, image1Path, image2Path)
            elif event.key == pygame.K_F6:
                settings = load_settings()
                SCREEN_WIDTH = settings['screen_width']
                SCREEN_HEIGHT = settings['screen_height']
                # Set maximum volume
                max_volume = settings['max_volume']
                image1Path = settings['image1Path']
                image2Path = settings['image2Path']
                # Load images
                image1 = pygame.image.load(image1Path)
                image2 = pygame.image.load(image2Path)
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if edit_mode == EditMode.EDIT_MAX_VOLUME.value:
                    max_volume += 10
            elif event.key == pygame.K_DOWN:
                if edit_mode == EditMode.EDIT_MAX_VOLUME.value:
                    max_volume -= 10

    # Get volume from microphone and calculate as percentage
    data = stream.read(1024, exception_on_overflow=False)
    data = np.fromstring(data, np.int16)
    volume = np.abs(data).mean()
    volume_percent = int(100 * volume / max_volume)
    if (ongame == True):
        # Calculate image heights based on volume percentage
        image2_height = int(SCREEN_HEIGHT * volume_percent / 100)
        image1_height = SCREEN_HEIGHT - image2_height
        # Display images
        screen.blit(image1, (0, 0), pygame.Rect(
            0, 0, SCREEN_WIDTH, image1_height))
        screen.blit(image2, (0, image1_height),
                    pygame.Rect(0, image1_height, SCREEN_WIDTH, image2_height))
    else:
        screen.blit(image2, (0, 0),
                    pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        printGameEnd(screen)

    fps_counter.tick()

    if show_fps:
        fps = normalFont.render(
            str(int(fps_counter.get_fps())), True, (255, 0, 0))
        screen.blit(fps, (0, 0))

    if edit_mode == EditMode.EDIT_MAX_VOLUME.value:
        edit_max_volume = normalFont.render(
            "EDIT MAX VOLUME: " + str(max_volume) + " // Current : " + "{:.3f}".format(volume), True, (255, 0, 0))
        # print right side of screen
        screen.blit(edit_max_volume, (SCREEN_WIDTH -
                    edit_max_volume.get_width() - 10, 0))

    if volume_percent > 100:
        ongame = False
    pygame.display.flip()

# Close pyaudio stream and terminate pygame
stream.stop_stream()
stream.close()
p.terminate()
pygame.quit()
