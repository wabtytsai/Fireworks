# lever editer
from pygame import *

##for x in range (0,w+1):
##    for 

def qa2():
    global fnt,cas
    quit()
    del fnt,cas



def run2():
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
    if nextBoxRect.collidepoint((mx,my)) and clicked:
        pageNum+=1
        return 0
    return 1

def blitCenter(pic,y):
    pos=pic.get_rect()
    pos.center=600,y
    screen.blit(pic,pos[0:2])

def save2():
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
    

def name2():
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

def main2():
    global clicked,mx,my,colours1,pos,colour,saveBox,pageNum,rects,out,blocks,fnt,ftime,white,left,right,picRect,mp,colours,valid,rects2,items,word,cap
    global green,screen,nextBoxRect,textX,nextBox
    size=w,h=1200,768
    screen=display.set_mode(size)
    init()
    fnt=font.SysFont("Courier",20)
    cas=font.SysFont("casual",24)
    green=0
    clicked=0
    mx,my=0,0
    colours1=[(30,144,255),(0,0,0),(0,255,0),(100,100,100),(255,50,50),(139,69,19)\
,(192,192,192),(225,225,0)]
    pos=0
    colour=colours1[pos]
    
    nextBox=cas.render("Next Page",1,(255,255,255))
    nextBoxRect=nextBox.get_rect()
    nextBoxRect.topleft=965,708
    screen.blit(nextBox,nextBoxRect[0:2])

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
            for i in range (34,1025,68):
                if i+68<991:
                    draw.rect(screen,(255,255,255),Rect(i,j,64,20),1)
                    rects.append((i,j,64,20))
                    out.append(None)

    blocks=[]

    ftime=150
    white=255,255,255
    left=right=0
    picRect=Rect(0,0,0,0)
    mp=0,0
    colours=[(255,255,0),(255,0,255),(0,255,255),(255,50,50),(50,255,50),\
             (255,255,255),(200,200,200),(169,69,19),(50,10,176)]
    valid=[0]*len(colours)
    rects2=[0]*len(colours)
    textX=401

    items=[]
    word=""
    cap=0
    while True:
        if pageNum==0:
            while run2():
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
            while save2():
                screen.fill((0,0,0))
##                pic=cas.render("Time:",1,white)
                blitCenter(cas.render("Time:",1,white),70)
                blitCenter(cas.render(str(ftime),1,white),120)
                left=cas.render("<",1,white).get_rect()
                left.topleft=(545,110)
                screen.blit(fnt.render("<",1,white),left[0:2])
                right=cas.render(">",1,white).get_rect()
                right.topleft=(645,110)
                screen.blit(fnt.render(">",1,white),right[0:2])
                blitCenter(cas.render("Effects",1,white),300)

                mx,my=mouse.get_pos()
                mp=mx,my
                if clicked:
                    if left.collidepoint(mp):
                        ftime=max(40,ftime-5)
                    elif right.collidepoint(mp):
                        ftime=min(600,ftime+5)

                for i in range (len(colours)):
                    draw.circle(screen,colours[i],(480+i*30,400),5)
                    rects2[i]=(Rect(480+i*30-10,400-10,20,20))
                    if rects2[i].collidepoint(mp) and clicked:
                        if valid[i]==0:
                            valid[i]=1
                        else:
                            valid[i]=0
                for i in range(len(valid)):
                    if valid[i]:
                        draw.rect(screen,white,rects2[i],1)
                        
                pic=cas.render("Next Page",1,white)
                picRect=pic.get_rect()
                picRect.center=600,560
                screen.blit(pic,picRect[0:2])
                display.flip()
        
        for i in range(len(valid)):
            if valid[i]:
                items.append(colours[i])
        if pageNum==2:
            while name2():
                mp=mouse.get_pos()
                screen.fill((0,0,0))
                blitCenter(cas.render("Type in your level name:",1,white),150)
                draw.rect(screen,white,(400,200,400,20))
                text=fnt.render(word,1,(0,0,0))
                if text.get_width()>400:textX=800-text.get_width()
                else:textX=401
                screen.blit(text,(textX,200))

                pic=cas.render("Save",1,white)
                saveBox=pic.get_rect()
                saveBox.center=600,300
                screen.blit(pic,saveBox[0:2])
                
                if (saveBox.collidepoint(mp) and clicked) or enter:
                    out=open(word+".txt","w")
                    out.write("""%d
%s
%s"""%(ftime,str(items),str(blocks)))
                    out.close()
                    break
                display.flip()
    ##    supposed to quit
        break

##for i in range (100):
##    print 'Hello World'
