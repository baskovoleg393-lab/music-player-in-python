import pygame as pg
from pygame_addiction import Root, Key, Button
from colors import colors
import os
import json
from random import randint, shuffle, choice

pg.init()
pg.mixer.init()
pg.mouse.set_visible(False)

with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

VIRTUAL_W, VIRTUAL_H = 1000, 1000
VIRTUAL_SIZE = (VIRTUAL_W, VIRTUAL_H)
W, H = data["size"][0], data["size"][1]
SIZE = (W, H)

cursor_static_screen = pg.transform.scale(pg.image.load("cursor_static.png"), (20, 20))
cursor_load_screen = pg.transform.scale(pg.image.load("cursor_load.png"), (20, 20))

path = data["path"] + "/"
is_rendering = True

index_playlist = 0
index_music = 0
current_position = 0
total_duration = 1

def Vx(x):
    return int(W * x / VIRTUAL_W)
def Vy(y):
    return int(H * y / VIRTUAL_H)

star_surfaces = []
def update_stars():
    global star_surfaces, star_surface
    star_surfaces = []
    
    stars = []
    for _ in range(W//10 + H//10):
        stars.append([randint(0, W), randint(0, H)])
    
    for i in range(20):
        surface = pg.Surface(SIZE)
        for pos in stars:
            pg.draw.circle(surface, colors.white(), pos, randint(1, 3))
        star_surfaces.append(surface)
    star_surface = choice(star_surfaces)
    
    
_text_cache = {}
def render_text(font, text, color):
    key = (id(font), text, color)
    if key not in _text_cache:
        print(key)
        _text_cache[key] = font.render(text, True, color)
    return _text_cache[key]

def update_playlist():
    global full_playlists
    if os.path.exists(path):
        full_playlists = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        full_playlists.sort()
    else:
        full_playlists = []
    full_playlists.sort()

update_playlist()

def update_music_list():
    global full_musics
    update_playlist()
    if full_playlists:
        try:
            full_musics = [f for f in os.listdir(path + full_playlists[index_playlist]) if f.endswith(('.mp3', '.wav', '.ogg'))]
            full_musics.sort()
        except PermissionError:
            full_musics = []
    else:
        full_musics = []

update_music_list()

key_need = Key(data["keys"]["need"])
key_plus_volume = Key(data["keys"]["plus volume"])
key_minus_volume = Key(data["keys"]["minus volume"])
key_plus_music = Key(data["keys"]["plus music"])
key_minus_music = Key(data["keys"]["minus music"])
key_plus_playlist = Key(data["keys"]["plus playlist"])
key_minus_playlist = Key(data["keys"]["minus playlist"])
key_stop = Key(data["keys"]["stop"])
key_fixed = Key(data["keys"]["fixed"])
key_shuffle = Key(data["keys"]["shuffle"])

current_volume = 0.5
is_playing = False
music_loaded = False
fixed = False
pos_in_button = False

def load_and_play():
    global music_loaded, is_playing, current_position, total_duration
    if full_playlists and full_musics:
        try:
            music_path = os.path.join(path, full_playlists[index_playlist], full_musics[index_music])
            pg.mixer.music.load(music_path)
            pg.mixer.music.set_volume(current_volume)
            pg.mixer.music.play()
            music_loaded = True
            is_playing = True
            current_position = 0
            total_duration = pg.mixer.Sound(music_path).get_length()
            if total_duration <= 0:
                total_duration = 1
        except Exception as e:
            print(f"Error: {e}")
            music_loaded = False
            is_playing = False

def draw_progress_bar(screen, x, y, w, h, progress):
    pg.draw.rect(screen, (30, 30, 50), (x, y, w, h), border_radius=10)
    pg.draw.rect(screen, (0, 200, 255), (x, y, w * progress, h), border_radius=10)
    pg.draw.rect(screen, (100, 100, 150), (x, y, w, h), 2, border_radius=10)

def handle_action(action):
    global index_playlist, index_music, current_volume, is_playing, music_loaded, current_position, fixed, total_duration
    match action:
        case "vol up":
            current_volume = min(1.0, current_volume + 0.1)
            pg.mixer.music.set_volume(current_volume)
        case "vol down":
            current_volume = max(0.0, current_volume - 0.1)
            pg.mixer.music.set_volume(current_volume)
        case "pause":
            if is_playing:
                pg.mixer.music.pause()
                is_playing = False
            else:
                pg.mixer.music.unpause()
                is_playing = True
        case "music up":
            index_music = (index_music + 1) % len(full_musics)
            fixed = False
            load_and_play()
        case "music down":
            index_music = (index_music - 1) % len(full_musics)
            fixed = False
            load_and_play()
        case "playlist up":
            index_playlist = (index_playlist + 1) % len(full_playlists)
            index_music = 0
            update_music_list()
            if full_musics:
                load_and_play()
        case "playlist down":
            index_playlist = (index_playlist - 1) % len(full_playlists)
            index_music = 0
            update_music_list()
            if full_musics:
                load_and_play()
        case "fixed":
            fixed = not fixed    
        case "shuffle":
            shuffle(full_musics)       
            load_and_play()

def update_gui():
    global stars, background, buttons, small_font, font
    update_stars()

    background = pg.Surface(SIZE)
    pg.draw.rect(background, (0, 0, 0, 50), (Vx(43), Vy(79), Vx(914), Vy(870)), border_radius=50)
    pg.draw.rect(background, (100, 100, 150), (Vx(43), Vy(79), Vx(914), Vy(870)), 2, border_radius=50)

    buttons = []
    btn_width = Vx(63)
    btn_height = Vy(63)

    buttons.append(Button(Vx(443), Vy(645), Vx(114), Vy(63), "pause"))
    buttons.append(Button(Vx(433), Vy(342), btn_width, btn_height, "<"))
    buttons.append(Button(Vx(504), Vy(342), btn_width, btn_height, ">"))
    buttons.append(Button(Vx(590), Vy(566), btn_width, btn_height, "+"))
    buttons.append(Button(Vx(360), Vy(566), btn_width, btn_height, "-"))
    buttons.append(Button(Vx(576), Vy(342), btn_width, btn_height, ">>"))
    buttons.append(Button(Vx(361), Vy(342), btn_width, btn_height, "<<"))
    buttons.append(Button(Vx(443), Vy(750), Vx(114), Vy(63), "fixed"))
    buttons.append(Button(W-Vx(160), Vy(110), Vx(71), Vy(79), "-"))
    buttons.append(Button(Vx(443), Vy(855), Vx(114), Vy(63), "shuffle"))

    font = pg.font.Font(None, Vy(89))
    small_font = pg.font.Font(None, Vy(58))

def update():
    global is_playing, index_music, W, H, SIZE, current_position, background, is_rendering, star_surface

    for key in [key_plus_volume, key_minus_volume, key_minus_music,
                key_plus_music, key_minus_playlist, key_plus_playlist,
                key_stop, key_need, key_fixed, key_shuffle]:
        key.update()

    is_active = key_need.press or pg.key.get_focused()
    
    if key_plus_volume.down and is_active:
        handle_action("vol up")
    if key_minus_volume.down and is_active:
        handle_action("vol down")
    if key_stop.down and is_active:
        handle_action("pause")
    if key_plus_music.down and full_musics and is_active:
        handle_action("music up")
    if key_minus_music.down and full_musics and is_active:
        handle_action("music down")
    if key_plus_playlist.down and full_playlists and is_active:
        handle_action("playlist up")
    if key_minus_playlist.down and full_playlists and is_active:
        handle_action("playlist down")
    if key_fixed.down and full_playlists and is_active:
        handle_action("fixed")    
    if key_shuffle.down and full_playlists and is_active:
        handle_action("shuffle")

    if music_loaded and is_playing and not pg.mixer.music.get_busy():
        is_playing = False
        current_position = total_duration
        if full_musics and not fixed:
            index_music = (index_music + 1) % len(full_musics)
        load_and_play()
    
    if is_playing:
        pos = max(0, pg.mixer.music.get_pos() / 1000)
        current_position = min(pos, total_duration)
    
    for event in root.events:
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        if event.type == 32779: #свернуть
            is_rendering = False
        elif event.type == 32781:#gjrfpf показать
            is_rendering = True

        if event.type == pg.VIDEORESIZE:
            W, H = SIZE = event.size
            update_gui()

        if buttons[0].handle_event(event):
            handle_action("pause")
        
        if buttons[1].handle_event(event) and full_musics:
            handle_action("music down")
            
        if buttons[2].handle_event(event) and full_musics:
            handle_action("music up")

        if buttons[3].handle_event(event):
            handle_action("vol up")
        
        if buttons[4].handle_event(event):
            handle_action("vol down")
        
        if buttons[5].handle_event(event) and full_playlists:
            handle_action("playlist up")        

        if buttons[6].handle_event(event) and full_playlists:
            handle_action("playlist down")

        if buttons[7].handle_event(event) and full_playlists:
            handle_action("fixed")

        if buttons[8].handle_event(event):
            pg.display.iconify()

        if buttons[9].handle_event(event) and full_playlists:
            handle_action("shuffle")

    """
    render_text(small_font, full_playlists[index_playlist], (100, 200, 255))
    render_text(font, "no playlist", (255, 100, 100))
    render_text(font, full_musics[index_music].rsplit(".", 1)[0], (255, 255, 255))
    render_text(small_font, f"{minutes:02d}:{seconds:02d}", (200, 200, 200))
    render_text(small_font, f"{minutes:02d}:{seconds:02d}", (200, 200, 200))
    render_text(font, vol_text, (200, 255, 200))
    """

    root.need_flips = is_rendering
    root.fps = data["fps"]
    if not is_active:
        root.fps = data["unfocused_fps"]
    if not is_rendering:
        return

    minutes = int(current_position // 60)
    seconds = int(current_position % 60)
    vol_text = f"{int(current_volume * 100)}%"
    
    root.screen.blit(background, (0, 0))
    root.screen.blit(star_surface, (0, 0))
    if root.time % 15 == 0:star_surface = choice(star_surfaces)
        
    if full_playlists:
        text = render_text(small_font, full_playlists[index_playlist], (100, 200, 255))
        x_playlist = (W - small_font.size(full_playlists[index_playlist])[0]) // 2
        root.screen.blit(text, (x_playlist, Vy(145)))
    else:
        text = render_text(font, "no playlist", (255, 100, 100))
        x_playlist = (W - font.size("no playlist")[0]) // 2
        root.screen.blit(text, (x_playlist, Vy(211)))
        return
    
    if full_musics:
        text = render_text(font, full_musics[index_music].rsplit(".", 1)[0], (255, 255, 255))
        x_music = (W - font.size(full_musics[index_music].rsplit('.', 1)[0])[0]) //2
        root.screen.blit(text, (x_music, Vy(211)))
        
        vol_text = f"{int(current_volume * 100)}%"
        text = render_text(font, vol_text, (200, 255, 200))
        x_vol = (W - font.size(vol_text)[0]) // 2
        root.screen.blit(text, (x_vol, Vy(566)))

        progress = current_position / total_duration if total_duration > 0 else 0
        draw_progress_bar(root.screen, Vx(93), Vy(487), Vx(814), Vy(37), min(progress, 1.0))
        
        time_text = render_text(small_font, f"{minutes:02d}:{seconds:02d}", (200, 200, 200))
        root.screen.blit(time_text, (Vx(93), Vy(426)))

        minutes = int(total_duration // 60)
        seconds = int(total_duration % 60)
        total_time_text = render_text(small_font, f"{minutes:02d}:{seconds:02d}", (200, 200, 200))
        root.screen.blit(total_time_text, (W - Vx(150), Vy(426)))
    else:
        text = render_text(font, "no music", (255, 200, 100))
        x_music = (W - font.size("no music")[0]) // 2
        root.screen.blit(text, (x_music, Vy(211)))
    
    pos_in_button = False
    buttons[7].text = "fixed" if not fixed else "unfixed"   
    buttons[0].text = "unpause" if not is_playing else "pause"
    for btn in buttons:
        btn.draw(root.screen)
        if btn.rect.collidepoint(pg.mouse.get_pos()):
            pos_in_button = True

    if pg.mouse.get_focused():
        if pos_in_button:
            root.screen.blit(cursor_load_screen, pg.mouse.get_pos())
        else:
            root.screen.blit(cursor_static_screen, pg.mouse.get_pos())
update_gui()
if __name__ == "__main__":
    if full_musics:
        load_and_play()

    root = Root(main=update, size=SIZE, fps=data["fps"])

    if err:=root.Start():
        print(err.args)