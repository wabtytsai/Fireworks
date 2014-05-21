# lever editer
from pygame import *
size=w,h=1024,768
screen=display.set_mode(size)
init()
##for x in range (0,w+1):
##    for 

def qa():
    global fnt
    quit()
    del fnt



def run():
    global clicked,colour,pos,pageNum
    clicked=0
    for evt in event.get():
        if evt.type==QUIT:return 0
        if evt.type==KEYDOWN:
            if evt.key==27:return 0 
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==1:
                clicked=1
            if evt.button==4:
                pos-=1
                if pos<0:
                    pos=len(colours1)-1
            if evt.button==5:
                pos+=1
                if pos>len(colours1)-1:
                    pos=0
    if saveBox.collidepoint((mx,my)) and clicked:
        pageNum+=1
        return 0
    return 1

def save():
    global clicked,pageNum
    clicked=0
    for evt in event.get():
        if evt.type==QUIT:
            return 0
        if evt.type==KEYDOWN:
            if evt.key==27:
                return 0
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==1:
                clicked=1

    if picRect.collidepoint(mp) and clicked:
        if green:
            if '1' in str(valid):
                pageNum+=1
                return 0
        else:
            pageNum+=1
            return 0
##        if quitValid:
##            print 1
##            text=fnt.render("Must pick at least one effect",1,(255,255,255))
##            screen.blit(text,(500,500))
##            display.flip()
    return 1
    

def name():
    global clicked,word,cap,text,enter
    clicked=0
    enter=0
    for evt in event.get():
        if evt.type==QUIT:
            return 0
        if evt.type==KEYDOWN:
            if evt.key==27:
                return 0
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==1:
                clicked=1
        if evt.type==KEYDOWN:
            if evt.key==13:
                enter=1
            if 97<=evt.key<=122:
                if cap==0:
                    word+=chr(evt.key)
                else:
                    word+=chr(evt.key-32)
            if evt.key==8:
                if cap:
                    word=""
                else:
                    if len(word)!=0:
                        word=word[:-1]
            if evt.key in [301,303,304]:
                cap=1
            if evt.key == 32:
                word+=" "
            if evt.key in range(48,58):
                if evt.key==50:
                    if cap:
                        word+="@"
                    else:
                        word+="2"
                else:
                    word+=chr(evt.key)
        if evt.type==KEYUP:
            if evt.key in [301,303,304]:
                cap=0
    return 1

clicked=0
mx,my=0,0
colours1=[(255,255,255),(0,0,0),(0,255,0),(100,100,100),(255,50,50),(50,50,255)]
pos=0
colour=colours1[pos]
#################################################
saveBox=Rect(965,708,30,30)
draw.rect(screen,(255,255,255),saveBox,1)
#################################################

pageNum=0

#drawing a grid system
rects=[]
out=[]
for j in range (100,769,48):
    if j+24<700:
        for i in range (34,1025,68):
            if i+68<991:
                draw.rect(screen,(255,255,255),Rect(i,j,64,20),1)
                rects.append((i,j,64,20))
                out.append(None)
for j in range (76,769,48):
    if j+24<700:
        for i in range (68,1025,68):
            if i+68<991:
                draw.rect(screen,(255,255,255),Rect(i,j,64,20),1)
                rects.append((i,j,64,20))
                out.append(None)

blocks=[]

fnt=font.SysFont("Courier",20)
time=40
white=255,255,255
left=right=0
picRect=Rect(0,0,0,0)
mp=0,0
colours=[(255,255,0),(255,0,255),(0,255,255),(255,50,50),(50,255,50),\
         (255,255,255),(200,200,200),(169,69,19),(50,10,176)]
valid=[0]*len(colours)
rects2=[0]*len(colours)

items=[]
word=""
cap=0
       
while True:
    if pageNum==0:
        while run():
            colour=colours1[pos]
            mx,my=mouse.get_pos()
            mb=mouse.get_pressed()
            for i in range (len(rects)):
                if Rect(rects[i]).collidepoint((mx,my)):
                    if mb[0]:
                        draw.rect(screen,colour,rects[i])
                        draw.rect(screen,(255,255,255),rects[i],1)
                        if colour!=(0,0,0):
                            out[i]=colour
                        else:
                            out[i]=None
            for i in range (len(colours1)):
                if colours1[i]!=(0,0,0):
                    draw.circle(screen,colours1[i],(20+50*i,730),5)
                else:
                    draw.circle(screen,(255,255,255),(20+50*i,730),5,1)
                box=Rect(20+50*i-15,715,30,30)
                draw.rect(screen,(0,0,0),box,1)
                if box.collidepoint((mx,my)) and clicked:
                    pos=i
                if colour==colours1[i]:
                    draw.rect(screen,(255,255,255),box,1)
            display.flip()
    green=0
    for i in range (len(out)):
        if out[i]!=None:
            blocks.append((out[i],rects[i]))
            if out[i]==(0,255,0):green=1
    if pageNum==1:
        while save():
            screen.fill((0,0,0))
            pic=fnt.render("Time:",1,white)
            screen.blit(pic,(20,20))
            pic=fnt.render(str(time),1,white)
            screen.blit(pic,(50,50))
            left=fnt.render("<",1,white).get_rect()
            left.topleft=(20,50)
            screen.blit(fnt.render("<",1,white),(20,50))
            right=fnt.render(">",1,white).get_rect()
            right.topleft=(95,50)
            screen.blit(fnt.render(">",1,white),(95,50))
            pic=fnt.render("Effects",1,white)
            screen.blit(pic,(20,150))

            mx,my=mouse.get_pos()
            mp=mx,my
            if clicked:
                if left.collidepoint(mp):
                    time=max(10,time-5)
                elif right.collidepoint(mp):
                    time=min(300,time+5)

            for i in range (len(colours)):
                draw.circle(screen,colours[i],(20+i*30,200),5)
                rects2[i]=(Rect(20+i*30-10,200-10,20,20))
                if rects2[i].collidepoint(mp) and clicked:
                    if valid[i]==0:
                        valid[i]=1
                    else:
                        valid[i]=0
            for i in range(len(valid)):
                if valid[i]:
                    draw.rect(screen,white,rects2[i],1)
                    
            pic=fnt.render("Done?",1,white)
            picRect=pic.get_rect()
            picRect.topleft=350,350
            screen.blit(pic,(350,350))
            display.flip()
    
    for i in range(len(valid)):
        if valid[i]:
            items.append(colours[i])
    if pageNum==2:
        while name():
            mp=mouse.get_pos()
            screen.fill((0,0,0))
            pic=fnt.render("Type in your level name:",1,white)
            screen.blit(pic,(100,150))
            draw.rect(screen,white,(100,190,200,20))
            text=fnt.render(word,1,(0,0,0))
            screen.blit(text,(100,190))
            pic=fnt.render("Save",1,white)
            screen.blit(pic,(300,300))
            saveBox=pic.get_rect()
            saveBox.topleft=300,300
            if (saveBox.collidepoint(mp) and clicked) or enter:
                out=open(word+".txt","w")
                out.write("""%d
%s
%s"""%(time,str(items),str(blocks)))
                out.close()
                break
            display.flip()
##    supposed to quit
    break

##for i in range (100):
##    print 'Hello World'
