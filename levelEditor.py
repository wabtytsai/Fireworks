# lever editer
from pygame import *

" this program creates a text file with all the infomation to a level"
" so later on we can load that file in our main program"
def qa():
    global fnt,cas
    quit()
    del fnt,cas



def run():
    " first page"
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
    " bliting a picture in the center"
    pos=pic.get_rect()
    pos.center=600,y
    screen.blit(pic,pos[0:2])

def save():
    " second page"
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
    return 1
    

def name():
    " third page"
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

def main():
    " main program/function"
    global clicked,mx,my,colours1,pos,colour,saveBox,pageNum,rects,out,blocks,fnt,ftime,white,left,right,picRect,mp,colours,valid,rects2,items,word,cap
    global green,screen,nextBoxRect,textX,nextBox
    size=w,h=1200,768
    screen=display.set_mode(size)
    init()
    fnt=font.SysFont("Courier",20)
    cas=font.SysFont("casual",24)
    green=0 # if there are any green blocks 
    clicked=0 # if the mouse is clicked or not
    mx,my=0,0 # position of the mouse
    colours1=[(30,144,255),(0,0,0),(0,255,0),(100,100,100),(255,50,50),(139,69,19)\
,(192,192,192),(225,225,0)] # colours of all the blocks
    pos=0 # position of the current block
    colour=colours1[pos] # the current colours
    
    nextBox=cas.render("Next Page",1,(255,255,255)) # picture showing "next page"
    nextBoxRect=nextBox.get_rect()  # position of the picture
    nextBoxRect.topleft=965,708 
    screen.blit(nextBox,nextBoxRect[0:2])

    pageNum=0 # the current page number

    #drawing a grid system
    rects=[] # all the position of each rectangles
    out=[] # all the colours in each rectangles
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

    blocks=[] # final output for the blocks

    ftime=150 # time limit
    white=255,255,255 
    left=right=0 # left and right button to set the time (increase decrease)
    picRect=Rect(0,0,0,0) 
    mp=0,0 # position of the mouse
    colours=[(255,255,0),(255,0,255),(0,255,255),(255,50,50),(50,255,50),\
             (255,255,255),(200,200,200),(169,69,19),(50,10,176)] # colours of all the effects
    valid=[0]*len(colours) # if the effects are selected or not
    rects2=[0]*len(colours) # position of each effect
    textX=401 # x value of where to blit the text on the last page

    items=[] # final output for the items
    word="" # file name
    cap=0 # caps on or not
    while True:
        if pageNum==0:
            while run():
                # this allows the user to select a type a block and put it on a
                # grid system
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
                # this allows the user to set the time and choose the effects
                screen.fill((0,0,0))
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
            while name():
                # finally the user will enter the file name 
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
