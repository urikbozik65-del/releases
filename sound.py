from pygame import *
import sounddevice as sd

fs = 44100 #частота дискретизації, поділ сигналу
buffer = 1024 #розмір буфера, скільки беремо точок за один раз

width, height = 600, 400

init()
screen = display.set_mode((width, height))
display.set_caption('Micro')
clock = time.Clock()

data = [0.0] * buffer

def callback(indata, frames, time, status):
    global data
    if status:
        print(status)
    data = [sample * (height // 2) for sample in indata[:, 0].tolist()]
    
stream = sd.InputStream(
    callback = callback, #функція, яка буде викликатися при отриманні нових даних
    channels = 1, #правий, моно
    samplerate = fs, #частота дискретизації
    blocksize = buffer, #розмір блоку
    dtype = 'float32' #тип даних (-1.0 до 1.0)
)
stream.start()

running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
    screen.fill((0, 0, 0))
    
    #частота, амплітуда(x, y)
    points = []
    for i, sample in enumerate(data):
        x = int(i * (width / buffer))
        y = int((height // 2) - sample)
        points.append((x, y))
    #малювання
    if len(points) > 1:
        draw.lines(screen, (0, 255, 0), False, points, 2)
    display.update()
    clock.tick(60)
stream.stop()
quit()