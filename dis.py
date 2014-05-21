#displaymenu.py
from glob import *
from pygame import *
def displayMenu():
    init()
    temp=glob("*.txt")
    files=[]
    for i in temp:
        if i !="accounts.txt" and i !=".txt":files.append(i)
    loading=image.load("pictures\\load.jpg")
    loadbox=Rect(176,320,48,48)
    global fnt2,bfnt,spot,show,scroll,barlen,count,dist,bartop,running
    size=length,width=1200,768
    screen=display.set_mode(size)
    if len(files)%3==0:wid2=len(files)/3*180
    else:wid2=180*(len(files)/3+1)
    wid2=max(600,wid2)
    scroll=Surface((600,wid2))
    spot=bartop=0
    barlen=600*768/wid2
    bar=Rect(1000,bartop,24,barlen)
    word=""
    #pictures
    paper=image.load("pictures\\document.png")
    #font
    fnt2=font.SysFont("Papyrus",16)
    bfnt=font.SysFont("Calibri",40)
    #flags
    startvalid=running=True
    while running:
        clicked=False
        letgo=False
        keyvalid=False
        for evt in event.get():
            if evt.type==MOUSEBUTTONDOWN:
                if evt.button==1:clicked=True
                if evt.button==5:
                    if spot<wid2-600:
                        spot=min(wid2-600,spot+15)
                        bartop+=768*15/wid2
                if evt.button==4:
                    if spot>0:
                        spot=max(0,spot-15)
                        bartop-=768*15/wid2
            if evt.type==MOUSEBUTTONUP:
                if evt.button==1:letgo=True
            if evt.type==KEYDOWN:
                keyvalid=True
                if evt.key in range(97,123):
                    if lets[303]==1 or lets[304]==1:word+=chr(evt.key-32)
                    else:word+=chr(evt.key)
                if evt.key==32:word+=" "
                if evt.key in range(40,58):
                    if evt.key==50:
                        if lets[303]==1 or lets[304]==1:word+="@"
                        else:word+="2"
                    else:word+=chr(evt.key)
                if evt.key==8:word=word[:-1]
        
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        lets=key.get_pressed()
        #sign
        stextpic=bfnt.render("Select Level",1,(189,232,76))
        screen.blit(stextpic,(100,200))
        draw.rect(screen,(255,255,255),(100,250,200,50))
        screen.blit(loading,(176,320))
        wtextpic=bfnt.render(word[-10:],1,(0,0,0))
        screen.blit(wtextpic,(100,255))
        if clicked and loadbox.collidepoint(mx,my) or lets[13]==1 and keyvalid:
            if word+".txt" in files:return word+".txt"
        #drawing on back screen
        count=0
        scroll.fill((0,255,0))
        for i in range(0,wid2,180):            
            for j in range(30,570,180):
                count+=1
                if count>len(files):break
                if Rect(j+400,i+100-spot,180,180).collidepoint(mx,my):
                    draw.rect(scroll,(255,255,0),(j,i,180,180))
                    if clicked:return files[(i+100)/180*3+(j+400)/180-2]
                scroll.blit(paper,(j,i))
                textpic=fnt2.render(files[count-1][:-4],1,(0,0,255))
                scroll.blit(textpic,(j+70,i+160))
            
        #draw scroll bar
        if mb[0]==1:        
            if bar.collidepoint(mx,my):
                if startvalid:dist,startvalid=my-bartop,0
                if my-dist>=0 and my-dist<=768-barlen:
                    bartop=my-dist
                    spot=min(wid2-600,int(wid2*bartop/768))
                    spot=max(0,spot)
        if letgo:startvalid=True
        draw.rect(screen,(0,0,255),(1000,0,24,768),1)
        draw.rect(screen,(255,0,0),(1000,bartop,24,barlen))
        bar=Rect(1000,bartop,24,230)            
        #display on main screen
        show=scroll.subsurface(Rect(0,spot,600,600))
        screen.blit(show.copy(),(400,100))
        display.flip()
        screen.fill((0,0,0))

