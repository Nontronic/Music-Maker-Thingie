#Imports and Initializing
import pygame as pg, sys
import time
import threading
import concurrent.futures
import random

pg.init()
pg.mixer.init()
pg.font.init()


#Globals
size = width, height = 1395, 785

black = 0, 0, 0
green = 111, 237, 145
blue = 111, 174, 237
white = 255, 255, 255

screen = pg.display.set_mode(size)
screen.fill(black)
background = pg.Surface(size)

allSprites = pg.sprite.RenderPlain()
playSprites = pg.sprite.RenderPlain()
clearSprites = pg.sprite.RenderPlain()
octaveSprites = pg.sprite.RenderPlain()
memeSprites = pg.sprite.RenderPlain()
columns = []

executor = concurrent.futures.ThreadPoolExecutor(max_workers=7)

playCheck = False


#Button Class
class button(pg.sprite.Sprite):
     def __init__(self, x, y, w, h, color, sound, note, note2):
       pg.sprite.Sprite.__init__(self)
       self.image = pg.Surface([w, h])
       self.image.fill(color)
       self.font = pg.font.Font("VT323-Regular.ttf", 48)
       self.text = note
       self.text2 = note2
       self.rect = self.image.get_rect()
       self.sound = pg.mixer.Sound(sound)
       self.rect.x = x
       self.rect.y = y
       self.x = x
       self.y = y
       self.counter = 0
       self.on = False

#Functions for Playing Music and Drawing the Grid of Buttons
def buildButtons():
    tracker = 0
    tracker2 = 0
    newList = []
    octave = 1
    for i in range(0, 105):     
        if i%7 == 0:
             sound = "music_maker_sounds/a_Major_piano.wav"
             note = "A"
             note2 = "A+"
        elif i%7 == 1:
             sound = "music_maker_sounds/b_Major_piano.wav"
             note = "B"
             note2 = "B+"
        elif i%7 == 2:
             sound = "music_maker_sounds/c_Major_piano.wav"
             note = "C"
             note2 = "C+"
        elif i%7 == 3:
             sound = "music_maker_sounds/d_Major_piano.wav"
             note = "D"
             note2 = "D+"
        elif i%7 == 4:
             sound = "music_maker_sounds/e_Major_piano.wav"
             note = "E"
             note2 = "E+"
        elif i%7 == 5:
             sound = "music_maker_sounds/f_Major_piano.wav"
             note = "F"
             note2 = "F+"
        elif i%7 == 6:
             sound = "music_maker_sounds/g_Major_piano.wav"
             note = "G"
             note2 = "G+"

        color = blue
        w = 50
        h = 50

        y = 120 + (i%7*85)
        #print(y)
            
        x = 35 + (i//7*85)
        
        Button = button(x, y, w, h, color, sound, note, note2)
        newList.append(Button)
        if len(newList) >= 7:
             columns.append(newList)
             newList = []
          
        allSprites.add(Button)

def playSound(button):
     button.sound.set_volume(0.2)
     button.sound.play()
     print("Played" + str(button.sound))

def playMusic():
     for column in columns:
          for b in column:
               if b.on == True:
                    executor.submit(playSound, b)
          
          time.sleep(1)
          
def drawWindow():
    allSprites.draw(screen)
    for allButtons in allSprites:
          render = allButtons.font.render(allButtons.text, True, black)
          screen.blit(render, (allButtons.x+(15/(len(allButtons.text))), allButtons.y))
          
    playSprites.draw(screen)
    playRender = playButton.font.render("Play!", True, black)
    screen.blit(playRender, (playButton.x+50, playButton.y))
    
    clearSprites.draw(screen)
    clearRender = clearButton.font.render("Clear", True, black)
    screen.blit(clearRender, (clearButton.x+45, clearButton.y))

    octaveSprites.draw(screen)
    for octaves in octaveSprites:
         octaveRender = octaves.font.render("+", True, black)
         screen.blit(octaveRender, (octaves.x+10, octaves.y-5))

    memeSprites.draw(screen)
    for m in memeSprites:
         render = m.font.render(m.text, True, black)
         screen.blit(render, (m.x+5, m.y))

def switchOctave(boolean, button):
     if boolean:
          for c in columns[octaveSprites.sprites().index(button)]:
               c.text = c.text2
     elif boolean == False:
          for c in columns[octaveSprites.sprites().index(button)]:
               c.text = c.text.replace("+", "")

#Creating the Buttons  
buildButtons()

playButton = button(718.75, 35, 187.5, 50, blue, "music_maker_sounds/bruh.mp3", "bruh", "bruh")
playSprites.add(playButton)

clearButton = button(503.75, 35, 187.5, 50, blue, "music_maker_sounds/bruh.mp3", "bruh", "bruh")
clearSprites.add(clearButton)

octaveX = 42.5

for i in range(15):
     octaveButton = button(octaveX, 720, 40, 40, blue, "music_maker_sounds/bruh.mp3", "bruh", "bruh")
     octaveSprites.add(octaveButton)
     octaveX += 85

bruhButton = button(1310, 290, 50, 50, blue, "music_maker_sounds/bruh.mp3", "Br", "bruh")
oofButton = button(1310, 375, 50, 50, blue, "music_maker_sounds/oof.mp3", "Of", "oof")
naniButton = button(1310, 460, 50, 50, blue, "music_maker_sounds/Nani.mp3", "Na", "oof")
memeSprites.add(bruhButton, oofButton, naniButton)
columns.append(memeSprites.sprites())


#Game Loop
running = True

while running:
    playButton.image.fill(blue)
    clearButton.image.fill(blue)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
             running = False
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for buttons in allSprites:
                if buttons.rect.collidepoint(event.pos):
                     if buttons.counter == 0:
                        buttons.counter += 1
                        buttons.image.fill(green)
                        buttons.on = True
                     elif buttons.counter%2 != 0:
                        buttons.counter += 1
                        buttons.image.fill(blue)
                        buttons.on = False
                     elif buttons.counter%2 == 0:
                        buttons.counter += 1
                        buttons.image.fill(green)
                        buttons.on = True
                        
            for o in octaveSprites:
                 if o.rect.collidepoint(event.pos):
                      if o.counter == 0:
                           o.counter += 1
                           o.image.fill(green)
                           o.on = True
                           switchOctave(o.on, o)
                      elif o.counter%2 != 0:
                           o.counter += 1
                           o.image.fill(blue)
                           o.on = False
                           switchOctave(o.on, o)
                      elif o.counter%2 == 0:
                           o.counter += 1
                           o.image.fill(green)
                           o.on = True
                           switchOctave(o.on, o)

            for meme in memeSprites:
                if meme.rect.collidepoint(event.pos):
                     if meme.counter == 0:
                        meme.counter += 1
                        meme.image.fill(green)
                        meme.on = True
                     elif meme.counter%2 != 0:
                        meme.counter += 1
                        meme.image.fill(blue)
                        meme.on = False
                     elif buttons.counter%2 == 0:
                        meme.counter += 1
                        meme.image.fill(green)
                        meme.on = True
                           
            if playButton.rect.collidepoint(event.pos):
                 playButton.image.fill(green)
                 playCheck = True
            if clearButton.rect.collidepoint(event.pos):
                 clearButton.image.fill(green)
                 for b in allSprites:
                      b.on = False
                      if(b.counter != 0):
                           b.counter -= 1
                      b.image.fill(blue)
                        
    screen.blit(background, (0, 0))
    drawWindow()
    if(playCheck == True):
         playMusic()
         playCheck = False
                             
    pg.display.flip()
    time.sleep(0.1)

pg.quit()
