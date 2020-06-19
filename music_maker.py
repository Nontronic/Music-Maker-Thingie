import pygame as pg, sys
import time

pg.init()

pg.mixer.init()

size = width, height = 910, 750
black = 0, 0, 0
green = 111, 237, 145
blue = 66, 138, 245

screen = pg.display.set_mode(size)
screen.fill(black)
background = pg.Surface(size)

allSprites = pg.sprite.RenderPlain()
playSprites = pg.sprite.RenderPlain()

class button(pg.sprite.Sprite):
     def __init__(self, x, y, w, h, color, sound):
       pg.sprite.Sprite.__init__(self)
       self.image = pg.Surface([w, h])
       self.image.fill(color)
       self.rect = self.image.get_rect()
       self.sound = pg.mixer.Sound(sound)
       self.rect.x = x
       self.rect.y = y
       self.on = 0

def drawButtons():
    tracker = 0
    tracker2 = 0
    for i in range(0, 99):
        sound = "bruh.mp3"
        color = blue
        w = 50
        h = 50
        
        y = 110 + (tracker*80)
        tracker += 1
        if(i%8 == 0):
            tracker = 0

        if i%9 == 0:
            tracker2 = i/9
        x = 30 + (tracker2*80)
        
        Button = button(x, y, w, h, color, sound)
        allSprites.add(Button)

drawButtons()

playButton  = button(355, 30, 200, 50, blue, "bruh.mp3")
playSprites.add(playButton)


while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for buttons in allSprites:
                if buttons.rect.collidepoint(event.pos):
                     if buttons.on == 0:
                        buttons.on += 1
                        buttons.image.fill(green)
                     elif buttons.on%2 != 0:
                        buttons.on += 1
                        buttons.image.fill(blue)
                     elif buttons.on%2 == 0:
                        buttons.on += 1
                        buttons.image.fill(green)
                        
    screen.blit(background, (0, 0))
    allSprites.draw(screen)
    playSprites.draw(screen)
    pg.display.flip()
