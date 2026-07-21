# Space Audio Player — Pygame Edition
# Copyright (c) 2026 Oleg
# Licensed under the MIT License
# https://github.com/your-username/space-audio-player

import pygame as pg
from pygame_addiction import Root, Key, Button
from colors import colors
import os
import json
from random import randint

pg.init()
pg.mixer.init()
pg.mouse.set_visible(False)

SIZE = (700, 380)

cursor_static_screen = pg.transform.scale(pg.image.load("cursor_static.png"), (20, 20))
#cursor_static_screen.set_colorkey(cursor_static_screen.get_at((0, 0)))
cursor_load_screen = pg.transform.scale(pg.image.load("cursor_load.png"), (20, 20))

background = pg.Surface(SIZE)
pg.draw.rect(background, (0, 0, 0, 50), (30, 30, 640, 320), border_radius=50)
pg.draw.rect(background, (100, 100, 150), (30, 30, 640, 320), 2, border_radius=50)

stars = []
for i in range(SIZE[0]//20+SIZE[1]//20):
    stars.append([randint(0, SIZE[0]), randint(0, SIZE[1])])

font = pg.font.Font(None, 34)
small_font = pg.font.Font(None, 22)

with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

path = data["path"] + "/"

index_playlist = 0
index_music = 0
current_position = 0
total_duration = 1

full_playlists = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
full_playlists.sort()

full_musics = []

def update_music_list():
    global full_musics
    if full_playlists:
        playlist_path = os.path.join(path, full_playlists[index_playlist])
        full_musics = [f for f in os.listdir(playlist_path) if f.endswith(('.mp3', '.wav', '.ogg'))]
        full_musics.sort()
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
btn_width = 44
btn_height = 24

buttons.append(Button(310, 245, 80, btn_height, "pause"))
buttons.append(Button(303, 130, btn_width, btn_height, "<"))
buttons.append(Button(353, 130, btn_width, btn_height, ">"))
buttons.append(Button(395, 245, btn_width, btn_height, "+"))
buttons.append(Button(261, 245, btn_width, btn_height, "-"))
buttons.append(Button(403, 130, btn_width, btn_height, ">>"))
buttons.append(Button(253, 130, btn_width, btn_height, "<<"))
buttons.append(Button(310, 285, 80, btn_height, "fixed"))

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

    root.screen.blit(background, (0, 0))
    for pos in stars:
        pg.draw.circle(root.screen, colors.white(), pos, randint(1, 2))
        
    if full_playlists:
        text = small_font.render(full_playlists[index_playlist], True, (100, 200, 255))
        root.screen.blit(text, (65, 55))
    else:
        text = font.render("нет плейлиста", True, (255, 100, 100))
        root.screen.blit(text, (65, 80))
        return
    
    if full_musics:
        text = font.render(full_musics[index_music], True, (255, 255, 255))
        root.screen.blit(text, (65, 80))
        
        text = font.render(f"{int(current_volume * 100)}%", True, (200, 255, 200))
        root.screen.blit(text, (334, 215))

        progress = current_position / total_duration if total_duration > 0 else 0
        draw_progress_bar(root.screen, 65, 185, 570, 14, min(progress, 1.0))
        
        minutes = int(current_position // 60)
        seconds = int(current_position % 60)
        time_text = small_font.render(f"{minutes:02d}:{seconds:02d}", True, (200, 200, 200))
        root.screen.blit(time_text, (65, 162))

        minutes = int(total_duration // 60)
        seconds = int(total_duration % 60)
        total_time_text = small_font.render(f"{minutes:02d}:{seconds:02d}", True, (200, 200, 200))
        root.screen.blit(total_time_text, (595, 162))
    else:
        text = font.render("нет музыки", True, (255, 200, 100))
        root.screen.blit(text, (65, 80))
    
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
    input(err.args)
