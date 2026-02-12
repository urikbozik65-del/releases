from pygame import *
from setting import *
def draw_effect(screen, rect, is_pressed = False):
    base_color = WHITE if not is_pressed else GRAY
    border_color = BLACK
    
    draw.rect(screen, base_color, rect)
    draw.rect(screen, border_color, rect, 2)
    