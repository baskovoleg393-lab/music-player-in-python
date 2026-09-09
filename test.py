import pygame as pg
from pygame_addiction import Root, Key, Button
from colors import colors
import os
import json
import math
from random import randint

pg.init()
pg.mixer.init()
pg.mouse.set_visible(False)

W, H = 1000, 1000
SIZE = (W, H)

cursor_static_screen = pg.transform.scale(pg.image.load("cursor_static.png"), (20, 20))
cursor_load_screen = pg.transform.scale(pg.image.load("cursor_load.png"), (20, 20))

background = pg.Surface(SIZE)
pg.draw.rect(background, (0, 0, 0, 50), (int(W*0.043), int(H*0.079), int(W*0.914), int(H*0.842)), border_radius=50)
pg.draw.rect(background, (100, 100, 150), (int(W*0.043), int(H*0.079), int(W*0.914), int(H*0.842)), 2, border_radius=50)

stars = []
for i in range(W//20 + H//20):
    stars.append([randint(0, W), randint(0, H)])

font = pg.font.Font(None, int(H*0.089))
small_font = pg.font.Font(None, int(H*0.058))

with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

path = data["path"] + "/"

index_playlist = 0
index_music = 0
current_position = 0
total_duration = 1

if os.path.exists(path):
    full_playlists = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    full_playlists.sort()
else:
    full_playlists = []
full_playlists.sort()

full_musics = []

def update_music_list():
    global full_musics
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

current_volume = 0.5
is_playing = False
music_loaded = False
fixed = False
pos_in_button = False

buttons = []
btn_width = int(W*0.063)
btn_height = int(H*0.063)

buttons.append(Button(int(W*0.443), int(H*0.645), int(W*0.114), int(H*0.063), "pause"))
buttons.append(Button(int(W*0.433), int(H*0.342), btn_width, btn_height, "<"))
buttons.append(Button(int(W*0.504), int(H*0.342), btn_width, btn_height, ">"))
buttons.append(Button(int(W*0.590), int(H*0.566), btn_width, btn_height, "+"))
buttons.append(Button(int(W*0.36), int(H*0.566), btn_width, btn_height, "-"))
buttons.append(Button(int(W*0.576), int(H*0.342), btn_width, btn_height, ">>"))
buttons.append(Button(int(W*0.361), int(H*0.342), btn_width, btn_height, "<<"))
buttons.append(Button(int(W*0.443), int(H*0.750), int(W*0.114), int(H*0.063), "fixed"))
buttons.append(Button(W-int(W*0.071), int(H*0.079), int(W*0.071), int(H*0.079), "-"))

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

def main():
    global index_playlist, index_music, current_volume, is_playing, music_loaded, current_position, fixed, total_duration

    for key in [key_plus_volume, key_minus_volume, key_minus_music,
                key_plus_music, key_minus_playlist, key_plus_playlist,
                key_stop, key_need, key_fixed]:
        key.update()
    
    if key_plus_volume.down and key_need.press:
        current_volume = min(1.0, current_volume + 0.1)
        pg.mixer.music.set_volume(current_volume)
    
    if key_minus_volume.down and key_need.press:
        current_volume = max(0.0, current_volume - 0.1)
        pg.mixer.music.set_volume(current_volume)

    if key_stop.down and key_need.press:
        if is_playing:
            pg.mixer.music.pause()
            is_playing = False
            buttons[0].text = "unpause"
        else:
            pg.mixer.music.unpause()
            is_playing = True
            buttons[0].text = "pause"
    
    if key_plus_music.down and full_musics and key_need.press:
        index_music = (index_music + 1) % len(full_musics)
        fixed = False
        load_and_play()
    
    if key_minus_music.down and full_musics and key_need.press:
        index_music = (index_music - 1) % len(full_musics)
        fixed = False
        load_and_play()
    
    if key_plus_playlist.down and full_playlists and key_need.press:
        index_playlist = (index_playlist + 1) % len(full_playlists)
        index_music = 0
        update_music_list()
        if full_musics:
            load_and_play()
    
    if key_minus_playlist.down and full_playlists and key_need.press:
        index_playlist = (index_playlist - 1) % len(full_playlists)
        index_music = 0
        update_music_list()
        if full_musics:
            load_and_play()

    if key_fixed.down and full_playlists and key_need.press:
        fixed = not fixed
        buttons[7].text = "fixed" if not fixed else "unfixed"
    
    if music_loaded and is_playing and not pg.mixer.music.get_busy():
        is_playing = False
        current_position = total_duration
        if full_musics and not fixed:
            index_music = (index_music + 1) % len(full_musics)
        load_and_play()
    
    if is_playing:
        pos = pg.mixer.music.get_pos() / 1000
        if pos < 0:
            pos = 0
        current_position = min(pos, total_duration)
    
    for event in root.events:
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        if buttons[0].handle_event(event):
            if is_playing:
                buttons[0].text = "unpause"
                pg.mixer.music.pause()
                is_playing = False
            else:
                buttons[0].text = "pause"
                pg.mixer.music.unpause()
                is_playing = True
        
        if buttons[1].handle_event(event) and full_musics:
            index_music = (index_music - 1) % len(full_musics)
            fixed = False
            load_and_play()
        
        if buttons[2].handle_event(event) and full_musics:
            index_music = (index_music + 1) % len(full_musics)
            fixed = False
            load_and_play()
        
        if buttons[3].handle_event(event):
            current_volume = min(1.0, current_volume + 0.1)
            pg.mixer.music.set_volume(current_volume)
        
        if buttons[4].handle_event(event):
            current_volume = max(0.0, current_volume - 0.1)
            pg.mixer.music.set_volume(current_volume)
        
        if buttons[5].handle_event(event) and full_playlists:
            index_playlist = (index_playlist + 1) % len(full_playlists)
            fixed = False
            index_music = 0
            update_music_list()
            if full_musics:
                load_and_play()
        
        if buttons[6].handle_event(event) and full_playlists:
            index_playlist = (index_playlist - 1) % len(full_playlists)
            fixed = False
            index_music = 0
            update_music_list()
            if full_musics:
                load_and_play()

        if buttons[7].handle_event(event) and full_playlists:
            fixed = not fixed
            buttons[7].text = "fixed" if not fixed else "unfixed"

        if buttons[8].handle_event(event):
            pg.display.iconify()

    root.screen.blit(background, (0, 0))
    for pos in stars:
        pg.draw.circle(root.screen, colors.white(), pos, randint(1, 2))
        
    if full_playlists:
        text = small_font.render(full_playlists[index_playlist], True, (100, 200, 255))
        x_playlist = int(W*0.093) + (int(W*0.814) - small_font.size(full_playlists[index_playlist])[0]) // 2
        root.screen.blit(text, (x_playlist, int(H*0.145)))
    else:
        text = font.render("no playlist", True, (255, 100, 100))
        x_playlist = (W - font.size("no playlist")[0]) // 2
        root.screen.blit(text, (x_playlist, int(H*0.211)))
        return
    
    if full_musics:
        text = font.render(full_musics[index_music], True, (255, 255, 255))
        x_music = int(W*0.093) + (int(W*0.814) - font.size(full_musics[index_music])[0]) // 2
        root.screen.blit(text, (x_music, int(H*0.211)))
        
        vol_text = f"{int(current_volume * 100)}%"
        text = font.render(vol_text, True, (200, 255, 200))
        x_vol = (W - font.size(vol_text)[0]) // 2
        root.screen.blit(text, (x_vol, int(H*0.566)))

        progress = current_position / total_duration if total_duration > 0 else 0
        draw_progress_bar(root.screen, int(W*0.093), int(H*0.487), int(W*0.814), int(H*0.037), min(progress, 1.0))
        
        minutes = int(current_position // 60)
        seconds = int(current_position % 60)
        time_text = small_font.render(f"{minutes:02d}:{seconds:02d}", True, (200, 200, 200))
        root.screen.blit(time_text, (int(W*0.093), int(H*0.426)))

        minutes = int(total_duration // 60)
        seconds = int(total_duration % 60)
        total_time_text = small_font.render(f"{minutes:02d}:{seconds:02d}", True, (200, 200, 200))
        root.screen.blit(total_time_text, (W - int(W*0.15), int(H*0.426)))
    else:
        text = font.render("no music", True, (255, 200, 100))
        x_music = (W - font.size("no music")[0]) // 2
        root.screen.blit(text, (x_music, int(H*0.211)))
    
    pos_in_button = False
    for btn in buttons:
        btn.draw(root.screen)
        if btn.rect.collidepoint(pg.mouse.get_pos()):
            pos_in_button = True

    if pg.mouse.get_focused():
        if pos_in_button:
            root.screen.blit(cursor_load_screen, pg.mouse.get_pos())
        else:
            root.screen.blit(cursor_static_screen, pg.mouse.get_pos())

if full_musics:
    load_and_play()

root = Root(main=main, size=SIZE, fps=data["fps"])

if (err:=root.Start()) != None:
    print(err.args)