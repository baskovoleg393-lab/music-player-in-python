# Space Audio Player — Pygame Edition
# Copyright (c) 2026 Oleg
# Licensed under the MIT License

from typing import Any


class rgb:
    def __init__(self, r: int, g: int, b: int, name: str = "none"):
        self.red = r
        self.green = g
        self.blue = b
        self.output_color = r, g, b
        self.name = name
        self.nex_code = "#%02x%02x%02x" % self.output_color
    def __call__(self):
        return self.output_color
    def __repr__(self) -> str:
        return self.name
    def __str__(self) -> str:
        pass
class nex_code:
    def __init__(self, code:str, name="none"):
        self.code = code
        ret_code = self.code.lstrip("#")
        self.r, self.g, self.b = int(ret_code[1:3], 16), int(ret_code[3:5], 16), int(ret_code[5:7], 16)
        self.rgb = self.r, self.g, self.b
        self.name = name
    def __call__(self):
        return self.code

class colors:
    """
     -- Обычный цвет
     -- светлый цвет
     -- темный цвет
    """

    red = rgb(255, 0, 0, "red")
    light_red = rgb(255, 102, 102, "light red") 
    dark_red = rgb(139, 0, 0, "dark red")

    green = rgb(0, 128, 0, "green")
    light_green = rgb(144, 238, 144, "light green")
    dark_green = rgb(0, 100, 0, "dark green")

    blue = rgb(0, 0, 255, "blue")
    light_blue = rgb(173, 216, 230, "light blue")
    dark_blue = rgb(0, 0, 139, "dark blue")

    yellow = rgb(255, 255, 0, "yellow")
    light_yellow = rgb(255, 255, 224, "light yellow")
    dark_yellow = rgb(184, 134, 11, "dark yellow")

    pink = rgb(255, 192, 203, "pink")
    light_pink = rgb(255, 182, 193, "light pink")
    dark_pink = rgb(231, 84, 128, "dark pink")

    purple = rgb(255, 0, 255, "purple")
    light_purple = rgb(238, 130, 238, "light purple")
    dark_purple = rgb(148, 0, 211, "dark purple")

    black = rgb(0, 0, 0, "black")
    white = rgb(255, 255, 255, "white")
    gray = rgb(128, 128, 128, "gray")

    brown = rgb(150, 75, 0, "brown")
    light_brown = rgb(181, 101, 29, "light brown")
    dark_brown = rgb(101, 67, 33, "dark brown")

    orange = rgb(255, 90, 0, "orange")
    light_orange = rgb(255, 167, 86, "light orange")
    dark_orange = rgb(200, 90, 0, "dark orange")

def test_color():
    import pygame as pg
    pg.init()
    pg.font.init()
    sc = pg.display.set_mode((500, 600))

    font = pg.font.Font(None, 20)
    work = True

    sc.fill(colors.gray())
    namx, namy = 0, 0
    for obj in ([value for attr, value in colors.__dict__.items()
                            if not attr.startswith('__')]):
        pg.draw.rect(sc, obj(), pg.Rect(namx*100, namy*100, 100, 100))
        bg = colors.black()
        if obj.name == "black": #type: str
            bg = colors.white()
        sc.blit(font.render(obj.name, True, bg), (namx*100+20, namy*100+25))
        namx += 1
        if namx >= 5:
            namy += 1
            namx = 0

        pg.display.flip()

    while work:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                work = False
if __name__ == "__main__":
    test_color()
