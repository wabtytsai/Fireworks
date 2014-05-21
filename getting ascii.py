# lever editer
from pygame import *
size=w,h=1024,768
screen=display.set_mode(size)
running=1
while running:
    for i in event.get():
        if i.type==QUIT:
            running=1
            break
        if i.type==KEYDOWN:
            if i.key==27:
                running=1
                break
            else:print i.key
    display.flip()
quit()
