from pygame import mixer

def load_sound(keys):
    sound = {}
    for key, filename in keys.items():
        sound[key] = mixer.Sound()
    return sound