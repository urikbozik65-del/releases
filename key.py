from pygame import *
from effect import *

def draw_key(screen, keys_rect, pressed_keys):
    for i, rect in enumerate(keys_rect):
        is_pressed = i in pressed_keys
        draw_effect(screen, rect, is_pressed)
def draw_rect(num_keys, start_x = 50, start_y = 100, width = 100, height = 300):
    keys = []
    for i in range(num_keys):
        x = start_x + i * width # 0, -50, 1 - 150, 2 - 250
        keys.append(Rect(x, start_y, width, height))
    return keys
