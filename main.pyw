import pygame as pg
from pygame_addiction import Root, Key, Button
from colors import colors
import os
import json
from random import randint, shuffle, choice
import time 
import signal

signal.signal(signal.SIGINT, signal.SIG_IGN)

pg.init()
pg.mixer.init()
pg.mouse.set_visible(False)

with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

VIRTUAL_W, VIRTUAL_H = 1000, 1000
VIRTUAL_SIZE = (VIRTUAL_W, VIRTUAL_H)
W, H = data["size"][0], data["size"][1]
SIZE = (W, H)
seek_base = 0

cursor_static_screen = pg.transform.scale(pg.image.load("cursor_static.png"), (20, 20))
cursor_load_screen = pg.transform.scale(pg.image.load("cursor_load.png"), (20, 20))

path = data["path"] + "/"
is_rendering = True

index_playlist = 0
index_music = 0
current_position = 0
total_duration = 1

repeat_mode = "no repeat"

time_star = time.time()

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
        _text_cache[key] = font.render(text, True, color)
    return _text_cache[key]

def update_playlist(is_start = False):
    global full_playlists, index_playlist
    if os.path.exists(path):
        try:
            full_playlists = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
            full_playlists.sort()
            if is_start:
                index_playlist = full_playlists.index(data["last_playlist"])
        except (PermissionError, FileNotFoundError):
            full_playlists = []
        except ValueError:
            pass
    else:
        full_playlists = []


def update_music_list(is_start = False):
    global full_musics, index_music
    update_playlist(is_start)
    if full_playlists:
        try:
            full_musics = [f for f in os.listdir(path + full_playlists[index_playlist]) if f.endswith(('.mp3', '.wav', '.ogg'))]
            full_musics.sort()
            if is_start:
                index_music = full_musics.index(data["last_music"])
        except (PermissionError, FileNotFoundError):
            full_musics = []
        except ValueError:
            pass
    else:
        full_musics = []

update_music_list(data["last_playlist"] and data["last_music"])

key_need = Key(data["keys"]["need"])
key_volume_up = Key(data["keys"]["volume up"])
key_volume_down = Key(data["keys"]["volume down"])
key_music_forward = Key(data["keys"]["music forward"])
key_music_back = Key(data["keys"]["music back"])
key_playlist_forward = Key(data["keys"]["playlist forward"])
key_playlist_back = Key(data["keys"]["playlist back"])
key_seek_forward = Key(data["keys"]["seek forward"])
key_seek_back = Key(data["keys"]["seek back"])
key_stop = Key(data["keys"]["pause"])
key_repeat = Key(data["keys"]["repeat"])
key_shuffle = Key(data["keys"]["shuffle"])

current_volume = 0.5
is_playing = False
music_loaded = False

pos_in_button = False

error_text = ""

def load_and_play():
    global music_loaded, is_playing, current_position, total_duration, seek_base, error_text
    if full_playlists and full_musics:
        try:
            error_text = ""
            pg.mixer.music.stop()
            music_path = os.path.join(path, full_playlists[index_playlist], full_musics[index_music])
            pg.mixer.music.load(music_path)
            pg.mixer.music.set_volume(current_volume)
            pg.mixer.music.play()
            music_loaded = True
            is_playing = True
            current_position = 0
            seek_base = 0   
            total_duration = pg.mixer.Sound(music_path).get_length()
            if total_duration <= 0:
                total_duration = 1

            data["last_playlist"] = full_playlists[index_playlist]
            data["last_music"] = full_musics[index_music]
        except Exception as e:
            error_text = str(e)
            music_loaded = False
            is_playing = False

def seek(position_seconds):
    global current_position, seek_base, is_playing, error_text
    
    if not all([full_musics, music_loaded]):
        return
    
    position_seconds = max(0, min(position_seconds, total_duration))
    
    try:
        error_text = ""
        music_path = os.path.join(path, full_playlists[index_playlist], full_musics[index_music])
        pg.mixer.music.load(music_path)
        pg.mixer.music.play(start=position_seconds)
        pg.mixer.music.set_volume(current_volume)
        current_position = position_seconds
        seek_base = position_seconds  
        is_playing = True
    except Exception as e:
        error_text = str(e)

def draw_progress_bar(screen, rect, progress):
    x, y, w, h = rect.x, rect.y, rect.w, rect.h
    pg.draw.rect(screen, colors.dark_blue(), (x, y, w, h), border_radius=20)
    pg.draw.rect(screen, colors.light_blue(), (x, y, w * progress, h), border_radius=20)
    pg.draw.rect(screen, colors.dark_gray_blue(), (x, y, w, h), 5, border_radius=20)

def handle_action(action):
    global index_playlist, index_music, current_volume, is_playing, music_loaded, current_position, total_duration, repeat_mode
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
            load_and_play()
        case "music down":
            index_music = (index_music - 1) % len(full_musics)
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
        case "seek up":
            seek(current_position + data["seek step"])
        case "seek down":
            seek(current_position - data["seek step"])
        case "repeat":
            if repeat_mode == "no repeat":repeat_mode = "music repeat"
            elif repeat_mode == "music repeat":repeat_mode = "playlist repeat"
            else:repeat_mode = "no repeat"
        case "shuffle":
            shuffle(full_musics)       
            load_and_play()

def update_gui():
    global stars, background, buttons, small_font, font, progress_bar_rect
    update_stars()

    progress_bar_rect = pg.Rect(Vx(93), Vy(472), Vx(814), Vy(67))

    background = pg.Surface(SIZE)

    buttons = []
    btn_width = Vx(63)
    btn_height = Vy(63)
    size = max(20, Vx(20))

    buttons.append(Button(Vx(443), Vy(645), Vx(114), btn_height, "pause", size=size))
    buttons.append(Button(Vx(433), Vy(342), btn_width, btn_height, "<", size=size))
    buttons.append(Button(Vx(504), Vy(342), btn_width, btn_height, ">", size=size))
    buttons.append(Button(Vx(590), Vy(566), btn_width, btn_height, "+", size=size))
    buttons.append(Button(Vx(360), Vy(566), btn_width, btn_height, "-", size=size))
    buttons.append(Button(Vx(576), Vy(342), btn_width, btn_height, ">>", size=size))
    buttons.append(Button(Vx(361), Vy(342), btn_width, btn_height, "<<", size=size))
    buttons.append(Button(Vx(443), Vy(750), Vx(114), btn_height, "repeat", size=size))
    buttons.append(Button(Vx(443), Vy(855), Vx(114), btn_height, "shuffle", size=size))

    font = pg.font.Font(None, Vy(89))
    small_font = pg.font.Font(None, Vy(58))

def update():
    global is_playing, index_music, W, H, SIZE, current_position, is_rendering, star_surface, time_star, progress_bar_rect, full_playlists

    for key in [key_volume_up, key_volume_down, key_music_back,
                key_music_forward, key_playlist_forward, 
                key_playlist_back, key_seek_forward, key_seek_back,
                key_stop, key_need, key_repeat, key_shuffle]:
        key.update()

    is_active = key_need.press or pg.key.get_focused()

    if is_active:
        if key_volume_up.down:
            handle_action("vol up")
        if key_volume_down.down:
            handle_action("vol down")
        if key_stop.down:
            handle_action("pause")
        if key_music_forward.down and full_musics:
            handle_action("music up")
        if key_music_back.down and full_musics:
            handle_action("music down")
        if key_playlist_forward.down and full_playlists:
            handle_action("playlist up")
        if key_playlist_back.down and full_playlists:
            handle_action("playlist down")
        if key_seek_forward.down and full_playlists:
            handle_action("seek up")
        if key_seek_back.down and full_playlists:
            handle_action("seek down")
        if key_repeat.down and full_playlists:
            handle_action("repeat")    
        if key_shuffle.down and full_playlists:
            handle_action("shuffle")

    if music_loaded and is_playing and not pg.mixer.music.get_busy():
        is_playing = False
        #current_position = total_duration
        if full_musics and repeat_mode == "no repeat":
            index_music = (index_music + 1)
            if index_music > len(full_musics)-1:
                index_music = 0
                handle_action("playlist up")
        elif full_musics and repeat_mode == "music repeat":
            pass
        elif full_playlists and repeat_mode == "playlist repeat":
            index_music = (index_music + 1) % len(full_musics)
        load_and_play()

    if is_playing:
        pos = max(0, pg.mixer.music.get_pos() / 1000)
        current_position = min(pos + seek_base, total_duration)
    
    for event in root.events:
        if event.type == pg.QUIT:
            root.Stop()
            return

        if event.type == 32779: #свернуть
            is_rendering = False
        elif event.type == 32781:#gjrfpf показать
            is_rendering = True

        if event.type == pg.VIDEORESIZE:
            W, H = SIZE = event.size
            update_gui()

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and is_rendering:
            if progress_bar_rect.collidepoint(event.pos):
                click_x = event.pos[0] - progress_bar_rect.x
                seek((click_x / progress_bar_rect.width) * total_duration)

        if event.type == pg.MOUSEMOTION:
            if progress_bar_rect.collidepoint(event.pos):
                pass

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
            handle_action("repeat")

        if buttons[8].handle_event(event) and full_playlists:
            handle_action("shuffle")

    minutes = int(current_position // 60)
    seconds = int(current_position % 60)
    vol_text = f"{int(current_volume * 100)}%"

    """
    render_text(small_font, full_playlists[index_playlist], (100, 200, 255))
    render_text(font, "no playlist", (255, 100, 100))
    render_text(font, full_musics[index_music].rsplit(".", 1)[0], (255, 255, 255))
    render_text(small_font, f"{minutes:02d}:{seconds:02d}", (200, 200, 200))
    render_text(small_font, f"{minutes:02d}:{seconds:02d}", (200, 200, 200))
    render_text(font, vol_text, (200, 255, 200))
    """

    root.fps = data["fps"]
    if not is_active:
        root.fps = data["unfocused_fps"]

    root.need_flips = is_rendering
    if not is_rendering:
        root.fps = data["minimized_fps"]
        return
    
    root.screen.blit(background, (0, 0))
    root.screen.blit(star_surface, (0, 0))
    if root.time - time_star > data["star_update_interval"]:
        star_surface = choice(star_surfaces)
        time_star = root.time
        
    if full_playlists:
        text = render_text(small_font, full_playlists[index_playlist], colors.light_blue())
        x_playlist = (W - small_font.size(full_playlists[index_playlist])[0]) // 2
        root.screen.blit(text, (x_playlist, Vy(145)))
    else:
        text = render_text(font, "no playlist", colors.light_red())
        x_playlist = (W - font.size("no playlist")[0]) // 2
        root.screen.blit(text, (x_playlist, Vy(211)))
        return
    
    if full_musics:
        text = render_text(font, full_musics[index_music].rsplit(".", 1)[0], colors.white())
        x_music = (W - font.size(full_musics[index_music].rsplit('.', 1)[0])[0]) //2
        root.screen.blit(text, (x_music, Vy(211)))
        
        vol_text = f"{int(current_volume * 100)}%"
        text = render_text(font, vol_text, colors.light_green())
        x_vol = (W - font.size(vol_text)[0]) // 2
        root.screen.blit(text, (x_vol, Vy(566)))

        progress = current_position / total_duration if total_duration > 0 else 0
        draw_progress_bar(root.screen, progress_bar_rect, min(progress, 1.0))
        
        time_text = render_text(small_font, f"{minutes:02d}:{seconds:02d}", colors.light_gray())
        root.screen.blit(time_text, (Vx(93), Vy(426)))

        minutes = int(total_duration // 60)
        seconds = int(total_duration % 60)
        total_time_text = render_text(small_font, f"{minutes:02d}:{seconds:02d}", colors.light_gray())
        root.screen.blit(total_time_text, (W - Vx(150), Vy(426)))
    else:
        text = render_text(font, "no music", colors.light_yellow())
        x_music = (W - font.size("no music")[0]) // 2
        root.screen.blit(text, (x_music, Vy(211)))
    
    pos_in_button = False
     
    buttons[0].text = "unpause" if not is_playing else "pause"
    for btn in buttons:
        btn.draw(root.screen)
        if btn.rect.collidepoint(pg.mouse.get_pos()):
            pos_in_button = True

    if pg.mouse.get_focused():
        if pos_in_button or progress_bar_rect.collidepoint(root.mouse):
            root.screen.blit(cursor_load_screen, pg.mouse.get_pos())
        else:
            root.screen.blit(cursor_static_screen, pg.mouse.get_pos())
    
    root.screen.blit(render_text(font, f"debug: {error_text if error_text else None}", colors.white())) #для откладки при комитк убрат
    
update_gui()
if __name__ == "__main__":
    if full_musics:
        load_and_play()

    root = Root(main=update, size=SIZE, fps=data["fps"])

    if err:=root.Start():
        raise err
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
