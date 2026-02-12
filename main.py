from pygame import *
from random import randint
import sounddevice as sd
import numpy as np

init()
width, height = 1200, 800
window = display.set_mode((width, height))
display.set_caption("Fluppy Bird: Voice Control")
clock = time.Clock()

# Налаштування звуку
fs = 16000
block = 256
mic_level = 0.0

def callback(indata, frames, time, status):
    global mic_level
    if status:
        print(status)
    sc = float(np.sqrt(np.mean(indata**2)))
    mic_level = 0.70 * mic_level + 0.30 * sc

# Створення гравця
player_rect = Rect(150, height // 2 - 50, 60, 60) 

def generate_pipe(count, start_x_offset=width):
    pipes = []
    pipe_width = 100
    gap = 250
    distance = 500
    start_x = start_x_offset
    
    for i in range(count):
        height_top = randint(100, 450)
        top_pipe = Rect(start_x, 0, pipe_width, height_top)
        bottom_pipe = Rect(start_x, height_top + gap, pipe_width, height - (height_top + gap))
        pipes.append(top_pipe)
        pipes.append(bottom_pipe)
        start_x += distance
    return pipes

# Стан гри
pipes = generate_pipe(5)
main_font = font.SysFont("Arial", 70)
hint_font = font.SysFont("Arial", 28)
score = 0
lose = False

# Фізика
y_vel = 0.0
base_gravity = 0.6
current_gravity = base_gravity
thresh = 0.03      # Поріг для стрибка 
impulse = -10.0    # Сила стрибка
restart_thresh = 0.05
lose_time = 0
restart_delay = 60

# Запуск мікрофона
with sd.InputStream(callback=callback, samplerate=fs, blocksize=block, channels=1):
    while True:
        for e in event.get():
            if e.type == QUIT:
                exit()

        window.fill("skyblue")

        if not lose:
            # Логіка стрибка
            if mic_level > thresh:
                y_vel = impulse
            
            y_vel += current_gravity
            player_rect.y += int(y_vel)

            # Обмеження екрану
            if player_rect.top <= 0:
                player_rect.top = 0
                y_vel = 0
            if player_rect.bottom >= height:
                lose = True

            # Рух труб та колізії
            for pipe in pipes[:]:
                pipe.x -= 5
                draw.rect(window, "green", pipe)

                if pipe.colliderect(player_rect):
                    lose = True

                if pipe.right < 0:
                    pipes.remove(pipe)
                    score += 0.5 

            if len(pipes) < 6:
                last_pipe_x = pipes[-1].x if pipes else width
                pipes.extend(generate_pipe(5, start_x_offset=last_pipe_x + 500))

        else:
            # Екран програшу
            lose_time += 1
            lose_text = main_font.render("GAME OVER", True, "red")
            hint_text = hint_font.render(f"Shout to restart! (Vol: {round(mic_level, 3)})", True, "black")
            
            window.blit(lose_text, (width // 2 - lose_text.get_width() // 2, height // 2 - 50))
            window.blit(hint_text, (width // 2 - hint_text.get_width() // 2, height // 2 + 50))

            # Рестарт голосом
            if lose_time >= restart_delay and mic_level > restart_thresh:
                lose = False
                lose_time = 0
                score = 0
                pipes = generate_pipe(5)
                player_rect.y = height // 2 - 50
                y_vel = 0
                current_gravity = base_gravity

        # Малювання гравця та рахунку
        draw.rect(window, "yellow", player_rect)
        score_display = main_font.render(str(int(score)), True, "white")
        window.blit(score_display, (width // 2, 50))

        display.update()
        clock.tick(60)
