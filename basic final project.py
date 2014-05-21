#basic block breaker
################################################################################
################################################################################
################################################################################
############################ Pause Changes the Time!!! #########################
################################################################################
################################################################################
################################################################################
from pygame import *
from math import *
from random import *
from glob import *
from dis import *
from levelEditor import *
from time import clock
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '20,50' 
def qa():
    global fnt
    quit()
    del fnt
################################################################################
################################################################################
################################################################################
#################################### Set up ####################################
################################################################################
################################################################################
################################################################################
##ftime,fcolours,fblocks=map(eval,open("idc.txt").read().split("\n"))
##ftime=0
##fcolours=[]
##fblocks=[]
size=length,width=1200,768
screen=display.set_mode(size)
blockScreen=Surface(size) # subsurface to check ball collision
init()
#ball's initial position(when its on the plateform)def levelSetUp(n):
bx,by=512,738
tbx,tby=512,30
#platform position
px,py=412,748
tpx,tpy=412,0
#flags
tstarting=1
paused=leftClick=helps=select=playing=rightvalid=False
"""pause, select, helps, are variables to keep tracf of current game status.
leftClick, playing and rightvalid are checking the user's current status"""
leftvalid=starting=ballvalid=timeRenew=menu=gameMode=True
"""left valid, starting, ballvalid, timeRenew are the user's current status.
menu, gameMode is to keep track of the current game status."
"""
#initial values
fnt=font.SysFont('Courier',20) # font
user=[[0,0,0,0,[]]]
##user=[]
"""a list to keep track of all the infomation about the balls
user=[[ball x,y, change in x,y],[center of the ball from last 10 update]"""
def setUp(n):
    global ftime,fcolours,fblocks,bx,by,px,py,paused,select,playing,rightvalid
    global leftvalid,starting,ballvalid,timeRenew,user,end,items,timeChange
    global bullets,shotKey,timer,effects,choose,blocks,shotKey2,tdirect
    global tbx,tby,tpx,tpy,tl,tr,tstarting,life,life2
    ftime,fcolours,fblocks=map(eval,open(n).read().split("\n"))
    bx,by=512,738
    px,py=412,748    
    tpx,tpy=412,0
    tbx,tby=512,30
    tstarting=1
    paused=select=playing=rightvalid=False
    leftvalid=starting=ballvalid=timeRenew=True
    user=[None]
    end=int(clock())+ftime
    life=life2=2
    items=[]
    timeChange=0
    bullets=[]
    shotKey=shotKey2=0
    tdirect=1

    timer=[0]
    effects=['normal()']
    choose=[colours.index(i) for i in fcolours]
    blocks=[[] for x in range (len(blockColours))]
    for i in fblocks:
        for j in range (len(blockColours)):
            if i[0]==blockColours[j]:blocks[j].append(Rect(i[1]))    
re=[]# a list to delete elements inside another list (short for remove)
cx,cy=0,0 # ball's position
sx,sy=0,0 # ball's change in x and y
items=[] # all the power-ups that are falling on the screen
end=int(clock())+300 # playing time
radius=10 # radius of the ball
speed=1.0 # the speed of the ball
life=life2=2 # the number of lives
timeChange=0 # a flag to turn on the count down
disPage=1
bullets=[] # list of the bullets shot by "shooter"
shotKey=0  # the "w" key on the keyboard, a flag to check if it is pressed
#power effects
timer=[0] # the timer for each power
effects=['normal()'] # list that holds all the powers
blockColours=[(255,255,255),(0,255,0),(50,50,255),(255,50,50),(100,100,100)]# different block colours
colours=[(255,255,0),(255,0,255),(0,255,255),(255,50,50),(50,255,50),\
         (255,255,255),(200,200,200),(169,69,19),(50,10,176)] # all the colours for each power-up
##choose=[colours.index(i) for i in fcolours] # power-ups that can be use in the game
power=['bigball()','smallball()','addtime()','fastball()','slowball()',\
       'pause()','shield()','shooter()','multiball()'] # a list with all the power-up function
blocks=[[] for x in range (len(blockColours))]# all the blocks currently in game
blocks[0].append(123)
##for i in fblocks:
##    "takes infomation from the level file and change it into something we need"
##    "it will sort the blocks by colour according to the blockColours."
##    for j in range (len(blockColours)):
##        if i[0]==blockColours[j]:blocks[j].append(Rect(i[1]))

################################################################################
################################################################################
################################################################################
################################# Ball and Blocks ##############################
################################################################################
################################################################################
################################################################################
def drawBlock():
    "this function will take all the element in blocks and draw it onto"
    "the back surfact - blockScreen"
    blockScreen.fill((0,0,0))
    for pos in range(len(blocks)):
        for each in blocks[pos]:draw.rect(blockScreen,blockColours[pos],each)
##drawBlock()

points=[(-1,1),(1,-1),(-1,1),(1,-1)]
##points=[(-1,1),(-1,-1),(1,-1),(-1,-1),(-1,1),(-1,-1),(1,-1),(-1,-1)]

def boundary(gameMode):
    draw.rect(screen,(0,0,255),(0,0,20,768))
    draw.rect(screen,(0,0,255),(1004,0,20,768))
    if gameMode!="2-Player Game":
        draw.rect(screen,(0,0,255),(0,0,1024,20))

def checkValid(pos):
    "check if the ball is inside each wall, if it is, move it out"
    cx,cy,sx,sy,ballPoint=user[pos]
    if cx-radius<20:cx,sx=21+radius,sx*-1
    elif cx+radius>1004:cx,sx=1003-radius,sx*-1
    elif cy-radius<20 and gameMode!="2-Player Game":sy,cy=sy*-1,21+radius
    user[pos]=cx,cy,sx,sy,ballPoint

def drawBall():
    "draws every single ball"
    for i in user:
        if i!=None:
            a,b,c,d,p=i
            draw.circle(screen,(255,0,0),(a,b),radius)
        
def tick():
    "the time count down function"
    pic=fnt.render(str(end-int(clock())),1,(0,255,0))
    screen.blit(pic,(980,0))
    
def movePlat():
    "moves the plateform when the user input from keyboard"
    # moves the platform
    global px,bx
    draw.rect(screen,(0,0,255),(px,py,200,20))
    if lets[97]==1 and px>20:
        px-=4
        if starting:bx-=4
    elif lets[100]==1 and px<804:
        px+=4
        if starting:bx+=4
        
def movePlat2():
##    27 3up 4down 6left 5right
    global tpx,tbx
    draw.rect(screen,(0,0,255),(tpx,tpy,200,20))
    if lets[276] and tpx>20:
        tpx-=4
        if tstarting:tbx-=4
    elif lets[275] and tpx<804:
        tpx+=4
        if tstarting:tbx+=4

def fire():
    "when the ball is still on the plateform, the ball will move right and left"
    "when the user hit 'w' the ball will leave the plateform"
    "this function takes care of that"
    # fires the ball and starts the game
    global leftvalid,rightvalid,starting,playing,dist,ang,ballvalid,ballAdd
    global timeRenew,bx,by,user,tbx,tby,timeChange
    if leftvalid:
        bx-=1
        if bx<=px+50:leftvalid,rightvalid=0,1
    elif rightvalid:
        bx+=1
        if bx>=px+150:rightvalid,leftvalid=0,1
    if shotKey:#lets[119]==1:
        starting=ballvalid=timeRenew=0
        playing=True
        cx,cy=bx,by
        dist=hypot(px+100-bx,py-by)
        ang=acos((px+100-bx)/dist)
        sx,sy=-cos(ang)*2,-sin(ang)*2
        user.append([cx,cy,sx,sy,[]])
def fire2():
    global tdirect,tstarting,playing,tbx,tby,user
    if tdirect:
        tbx-=1
        if tbx<=tpx+50:tdirect=0
    else:
        tbx+=1
        if tbx>=tpx+150:tdirect=1
    if shotKey2:
        tstarting=0
        playing=1
        cx,cy=tbx,tby
        dist=hypot(tpx+100-tbx,tpy-tby)
        ang=acos((tpx+100-tbx)/dist)
        sx,sy=-cos(ang)*2,sin(ang)*2
        user.append([cx,cy,sx,sy,[]])
            
def balls(pos):
    "control the movement of the ball"
    cx,cy,sx,sy,ballPoint=user[pos]
    # the movement of the balls
    global dist,ang,radius,po
    cx+=sx*speed
    cy+=sy*speed
    po=range(px-radius/2,px+200+radius/2)
    if (int(cy)in range(748-radius,752-radius) and int(cx) in po):
        "this is to reset the angle of the ball when the ball hits the paddle"
        sx,sy=findAng(px,py,cx,cy,1)
    elif gameMode=="2-Player Game":
        po=range(tpx-radius/2,tpx+200+radius/2)
        if (int(cy) in range (16+radius,20+radius) and int(cx) in po):
            sx,sy=findAng(tpx,tpy,cx,cy,0)
    user[pos]=cx,cy,sx,sy,ballPoint

def findAng(bx,by,cx,cy,v):
    dist=hypot(bx+100-cx,by-cy)
    ang=acos((bx+100-cx)/dist)
    sx=(-cos(ang)*2)
    if v:return -cos(ang)*2,-sin(ang)*2
    else:return -cos(ang)*2,sin(ang)*2

def block(pos):
    "Checks collision between the ball and a block"
    cx,cy,sx,sy,ballPoint=user[pos]
    cpoints=[(cos(radians(i))*radius+cx+1,sin(radians(i))*radius+cy+1) for \
             i in range (0,360,90)] # all the points from the ball
    for i in range (0,360,30):
        if i%90!=0:cpoints.append((cos(radians(i))*radius+cx+1,sin(radians(i))*radius+cy+1))
    for point in range(len(cpoints)):
        if cpoints[point][1]<764:
            if blockScreen.get_at(cpoints[point])!=(0,0,0):
                "if the colour at that pixel is not black"
                "I know the ball is colliding with a block"
                colourPos=blockScreen.get_at(cpoints[point])
                colourPos=blockColours.index(colourPos) # get the index of the colour at the pixel in blockColours
                if point in [0,1,2,3]:
                    sx*=points[point][0]
                    sy*=points[point][1]
                    findPos(cpoints[point],colourPos,sx,sy,0)
                    break
                else:
##                    sx,sy=findPos(cpoints[point],colourPos,sx,sy,1)
                    sx,sy,cx,cy=findPos(cpoints[point],colourPos,sx,sy,1)
                    break
    user[pos]=cx,cy,sx,sy,ballPoint

    
def findPos(p,c,sx,sy,valid):
    " find out which type of block it colliding with the ball"
    global blocks
    for block in range(len(blocks)):
        for each in blocks[block]:
            if each.collidepoint(p):
                blockEffect(c,each,block)
                ox,oy=each[0]+each[2]/2.0,each[1]+each[3]/2.0 # center of the block
                dx,dy=ox-p[0],oy-p[1] # center of the block - point of collision
                if valid:
                    a=atan(sy/sx)
                    x,y=radius*cos(a)+1,radius*sin(a)+1
##                    a=(atan2(sy,sx)+2*pi)%(pi/2)
                    if dx<0:
                        if dy<0:
                            "br"
##                            print "br"
                            cx,cy=each[0]+each[2]+radius+1,each[1]+each[3]+radius+1
##                            cx,cy=each[0]+each[2]-sy+1,each[1]+each[3]-sx+1
##                            cx,cy=each[0]+each[2]+cos(a)*radius+1,each[1]+each[3]+sin(a)*radius+1
                            return -sy,-sx,cx,cy
                        elif dy>0:
                            "tr"
##                            print "tr"
                            cx,cy=each[0]+each[2]+radius+1,each[1]-radius-1
##                            cx,cy=each[0]+each[2]+sy+1,each[1]+sx-1
##                            cx,cy=each[0]+each[2]+cos(a)*radius+1,each[1]-sin(a)*radius-1
                            return sy,sx,cx,cy
                    elif dx>0:
                        if dy>0:
                            "tl"
##                            print "tl"
                            cx,cy=each[0]-radius-1,each[1]-radius-1
##                            cx,cy=each[0]-sy-1,each[1]-sx-1
##                            cx,cy=each[0]-cos(a)*radius-1,each[1]-sin(a)*radius-1
                            return -sy,-sx,cx,cy
                        elif dy<0:
                            "bl"
##                            print "bl"
                            cx,cy=each[0]-radius-1,each[1]+each[3]+radius+1
##                            cx,cy=each[0]+sy-1,each[1]+each[3]+sx+1
##                            cx,cy=each[0]-cos(a)*radius-1,each[1]+each[3]+sin(a)*radius+1
                            return sy,sx,cx,cy
                
def blockEffect(col,block,pos):
    "each type of blocks has different effects on the gameplay."
    re=[]
    if col==0:re.append((pos,block))
        #white will be eraced after one collision
    elif col==1 and len(choose)!=0:
        #green is like white, but will drop a power-up
        num=choice(choose)
        if gameMode=="2-Player Game":
            direction=choice([-1,1])
        else:
            direction=1
        items.append([[block[0]+35,block[1]],num,direction])
        re.append((pos,block))
    elif col==2 or col==3:
        #blue will change into white after one collision
        blocks[0].append(block)
        re.append((pos,block))
    for i in re:
        pos,stuff=i
        blocks[pos].remove(stuff)
    drawBlock()

def item():
    "After a green block is hit, it will drop a power-up"
    "this function will randomly generate a power-up and controls all the"
    "movement of each power-up"
    re=[]
    for i in range(len(items)):
        center,num,direction=items[i]
        draw.circle(screen,colours[num],center,5)
        items[i][0]=items[i][0][0],items[i][0][1]+direction
        if items[i][0][1]>760:
            re.append(items[i])
            if items[i][0][0] in range(px,px+200) :
                "if the power-up landed on the paddle, the effect will apply"
                "to the user"
                if num not in [2,8]:
                    if num in [5]:
                        if power[num] in effects:
                            pos=effects.index(power[num])
                            timer[pos][1]=timer[pos][0]+5
                        else:
                            effects.append(power[num])
                            timer.append(\
                                [int(clock()),int(clock())+5,colours[num]])
                    else:
                        if power[num] in effects:
                            pos=effects.index(power[num])
                            timer[pos][1]=timer[pos][0]+10
                        else:
                            effects.append(power[num])
                            timer.append(\
                                [int(clock()),int(clock())+10,colours[num]])
                else:eval(power[num])
        elif items[i][0][1]<16:
            re.append(items[i])
            if items[i][0][0] in range (tpx,tpx+200):
                if num not in [2,8]:
                    if num in [5]:
                        if power[num] in effects:
                            pos=effects.index(power[num])
                            timer[pos][1]=timer[pos][0]+5
                        else:
                            effects.append(power[num])
                            timer.append(\
                                [int(clock()),int(clock())+5,colours[num]])
                    else:
                        if power[num] in effects:
                            pos=effects.index(power[num])
                            timer[pos][1]=timer[pos][0]+10
                        else:
                            effects.append(power[num])
                            timer.append(\
                                [int(clock()),int(clock())+10,colours[num]])

                else:eval(power[num])
    for i in re:items.remove(i)

def showeffect():
    " return infomation about each effect (time left, types of effect)"
    " and apply each effect to the game play"
    re=[]
    rt=[]
    for i in range(1,len(timer)):
        # blits on the timer for each effect
        pic=fnt.render(str(timer[i][1]-timer[i][0]),1,timer[i][2])
        screen.blit(pic,(50*(i-1),0))
    for i in effects:eval(i)
        # running each function
    for i in range(1,len(timer)):
        # if the timer is 0, delete it
        timer[i][0]=int(clock())
        if timer[i][0]==timer[i][1]:
            re.append(effects[i])
            rt.append(timer[i])
            if effects[i]=='shooter()':
                global bullets
                bullets=[]
    # deleting
    for i in re:effects.remove(i)
    for i in rt:timer.remove(i)

################################################################################
################################################################################
################################################################################
################################# Effect Function ##############################
################################################################################
################################################################################
################################################################################
def multiball():
    " adds 11 balls to the game going in 11 different directions"
    global starting,ballAdd
    if len(user)<50:
        cx,cy,sx,sy,ballPoint=user[1]
        startAng=degrees(atan2(sy,sx))  
        r=hypot(sx,sy)
        for i in range (startAng,360+startAng,30):
            nx,ny=cos(radians(i))*r,sin(radians(i))*r
            user.append([cx,cy,nx,ny,[]])
def bigball():
    " makes the ball bigger"
    global radius
    radius=15
def smallball():
    " makes the ball smaller"
    global radius
    radius=5
def addtime():
    " adds 10 seconds to the clock"
    global end
    end+=10
def fastball():
    " makes the ball move faster"
    global speed
    speed=1.5
def slowball():
    " makes the ball move slower"
    global speed
    speed=0.5
def pause():
    " stops the ball but keep the time moving"
    global speed
    speed=0
def shield():
    " creates a shield at the bottom of the screen to prevent the ball from"
    " falling"
    global cx,cy,sx,sy
    draw.line(screen,(0,255,255),(0,748),(1024,748),3)
    if int(cy) in range(748-radius,752-radius) and int(cx) not in po:sy*=-1
    
def shooter():
    global bullets
    if shotKey and len(bullets)<10:
        bullets.append([[px+90,728,3,3],1])
    if gameMode=="2-Player Game" and shotKey2 and len(bullets)<20:
        bullets.append([[tpx+90,40,3,3],-1])
    re=[]
    for i in range (len(bullets)):
        draw.rect(screen,(255,255,0),bullets[i][0])
##        draw.rect(screen,(169,69,19),bullets[i][0])
        direction=bullets[i][-1]
        bullets[i][0][1]-=direction
        x,y,l,w=bullets[i][0]
        if blockScreen.get_at((x,y))!=(0,0,0):
            colourPos=blockScreen.get_at((x,y))
            colourPos=blockColours.index(colourPos)
            findPos((x,y),colourPos,0,0,0)
            re.append(bullets[i])
        elif blockScreen.get_at((x+l,y))!=(0,0,0):
            colourPos=blockScreen.get_at((x+l,y))
            colourPos=blockColours.index(colourPos)
            findPos((x+l,y),colourPos,0,0,0)
            re.append(bullets[i])
        elif y<21:re.append(bullets[i])
        elif y>749:re.append(bullets[i])
    for i in re:bullets.remove(i)
        
                    
            
##    " creates a device that will help the user win the game"
##    " it will shoot up bullets, which will act as a ball but going striaght up"
                
def normal():
    " returns everything back to normal"
    global radius,speed,shots,heights,bullets
    radius=10
    shots=[]
    heights=[]
    speed=1.0
    
################################################################################
################################################################################
################################################################################
#################################### Game play #################################
################################################################################
################################################################################
################################################################################    

def updateScreen():
##    #blocks
    for pos in range(0,len(blocks)-2):
        for each in blocks[pos]:draw.rect(screen,blockColours[pos],each)
    for each in blocks[-1]:draw.rect(screen,blockColours[-1],each)
    #boundaries
    boundary(gameMode)        
    #platform
    movePlat()
    if gameMode=="2-Player Game":movePlat2()
    #ball
    if starting:draw.circle(screen,(255,0,0),(bx,by),radius)
    if tstarting and gameMode=="2-Player Game":
        draw.circle(screen,(255,0,0),(tbx,tby),radius)
    drawBall()

def gameover(n):
    screen.fill((0,0,0))
    pic=fnt.render(n,1,(255,255,255))
    screen.blit(pic,(480,370))
    display.flip()
    time.wait(1000)
    return 0

quiting=0
        
def run():
    " main event"
    global shotKey,user,leftClick,paused,bullets
    global life,timer,effects,starting,playing,ballvalid,shotKey2
    global px,py,keyvalid,levels,bx,by,items,disPage,levels
    global tpx,tpy,tbx,tby,life2,tdirect,tstarting
    leftClick=0
    keyvalid=False
    shotKey=shotKey2=0
    for evt in event.get():
        if evt.type==QUIT:return 0
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==1:clicked=1
        if evt.type==KEYDOWN:
            keyvalid=True
            if evt.key==27:return 0
            if evt.key==119:shotKey=1
            if evt.key==273:shotKey2=1
            if evt.key==112:paused=1
    if len(user)==1 and playing:
        if life==0:return gameover('Game Over')
        else:
            if gameMode!="2-Player Game":
                normal()
                life-=1
                timer=[0]
                items=[]
                effects=['normal()']
                starting=menu=ballvalid=timeRenew=leftvalid=1
                playing=paused=startGame=helps=rightvalid=select=False
                px=412
                py=748
                bx,by=512,738
                user=[None]
                bullets=[]
            else:
                if starting==0 and tstarting==0:
                    life2-=1
                    tpx=412
                    tpy=0
                    tbx,tby=512,radius+20
                    tdirect=tstarting=1
                    normal()
                    life-=1
                    timer=[0]
                    items=[]
                    effects=['normal()']
                    starting=menu=ballvalid=timeRenew=leftvalid=1
                    playing=paused=startGame=helps=rightvalid=select=False
                    px=412
                    py=748
                    bx,by=512,738
                    user=[None]
                    bullets=[]
    if end-int(clock())<0:return gameover('Time\'s Up')
    valid=1
    for i in blocks[:-2]:
        if len(i)!=0:valid=0
    if valid:
        if gameMode!="1-Player Game":return gameover('Winning')
        else:
            levels+=1
            disPage=1
    return 1

def menuRun():
    "the menu page in the beginning of the screen"
    global menu,select,leftClick,mx,my,mp,helps,pageStatus,quiting
    leftClick=0
    for evt in event.get():
        if evt.type==QUIT:menu,quiting=0,1
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==1:leftClick=1
        if evt.type==KEYDOWN:
            if evt.key==27:menu,quiting=0,1
    mx,my=mp=mouse.get_pos()
    screen.fill((0,0,0))
    startRect=fnt.render("Start",1,(255,255,255)).get_rect()
    startRect.center=512,250
    screen.blit(fnt.render("Start",1,(255,255,255)),\
                (startRect[0],startRect[1]))
    helpRect=fnt.render("Help",1,(255,255,255)).get_rect()
    helpRect.center=512,350
    screen.blit(fnt.render("Help",1,(255,255,255)),\
                (helpRect[0],helpRect[1]))
    if startRect.collidepoint(mp) and leftClick:select,menu=1,0
    elif helpRect.collidepoint(mp) and leftClick:menu,helps=0,1
    display.flip()

def helpRun():
    " the help page"
    global leftClick,mx,my,mp,menu,helps,quiting
    leftClick=0
    for evt in event.get():
        if evt.type==QUIT:helps,quiting=0,1
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==1:leftClick=1
        if evt.type==KEYDOWN:
            if evt.key==27:helps,quiting=0,1
    mx,my=mp=mouse.get_pos()
    screen.fill((0,0,0))
    helpPage="""
This is a Help Page
you move with WASD
The rest you can figure it out

Back
"""
    for i in range(len(helpPage.split("\n"))):
        text=helpPage.split("\n")[i]
        back=fnt.render(text,1,(255,255,255))
        backRect=back.get_rect()
        backRect.center=512,300+i*40
        screen.blit(back,(backRect[0],backRect[1]))
    if leftClick:helps,menu=0,1
    display.flip()

def selectRun():
    " the selecting game mode page"
    global leftClick,select,mx,my,mp,menu,gameMode,quiting
    leftClick=0
    for evt in event.get():
        if evt.type==QUIT:select,quiting=0,1
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==1:leftClick=1
        if evt.type==KEYDOWN:
            if evt.key==27:select,quiting=0,1
    mx,my=mp=mouse.get_pos()
    screen.fill((0,0,0))
    selection="""1-Player Game
2-Player Game
Custom Levels

Back"""
    selectionPage=selection.split('\n')
    for i in range (len(selectionPage)):
        pic=fnt.render(selectionPage[i],1,(255,255,255))
        picRect=pic.get_rect()
        picRect.center=512,300+i*40
        screen.blit(pic,(picRect[0],picRect[1]))
        if leftClick and picRect.collidepoint(mp):
            if selectionPage[i]=="Back":select,menu=0,1
            else:gameMode,select=selectionPage[i],0
    display.flip()

levelEdit=0

def customRun():
    global leftClick,gameMode,select,mx,my,mp,quiting
    leftClick=0
    for evt in event.get():
        if evt.type==QUIT:select,gameMode,quiting=1,0,1
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==1:leftClick=1
        if evt.type==KEYDOWN:
            if evt.key==27:select,gameMode,quiting=1,0,1
    mx,my=mp=mouse.get_pos()
    screen.fill((0,0,0))
    selection="""Play
Create Levels

Back"""
    selectionPage=selection.split('\n')
    for i in range (len(selectionPage)):
        pic=fnt.render(selectionPage[i],1,(255,255,255))
        picRect=pic.get_rect()
        picRect.center=512,300+i*40
        screen.blit(pic,(picRect[0],picRect[1]))
        if leftClick and picRect.collidepoint(mp):
            if selectionPage[i]=="Back":select,gameMode=1,0
            else:gameMode=selectionPage[i]
    display.flip()

def gamePause():
    "pausing the game while in game"
    global paused,timeChange,end,mx,my,quiting
    for evt in event.get():
        if evt.type==QUIT:paused=0
        if evt.type==KEYDOWN:
            if evt.key==112:paused=0
    mp=mouse.get_pos()
    mouse.set_visible(0)
    screen.fill((0,0,0))
    pic=fnt.render("Paused",1,(0,255,255))
    screen.blit(pic,mp)
    if timeChange!=int(clock()):
        end+=1
        timeChange=int(clock())
    display.flip()

levels=1

while run():
    mx,my=mp=mouse.get_pos()
    mb=mouse.get_pressed()
    lets=key.get_pressed()
    screen.fill((0,0,0))
    # blocks
##    screen.blit(blockScreen,(0,0))
##    for pos in range(0,len(blocks)-2):
##        for each in blocks[pos]:draw.rect(screen,blockColours[pos],each)
##    for each in blocks[-1]:draw.rect(screen,blockColours[-1],each)
    if quiting:break
    while menu:menuRun()
    while select:selectRun()    
    while helps:helpRun()
    while gameMode=="Custom Levels":customRun()

    if gameMode=="1-Player Game":
        if disPage:
            disPage=0
            setUp("1p\\level "+str(levels)+".txt")
            drawBlock()
        updateScreen()
        for i in range (life):draw.circle(screen,(255,0,0),(10,30+25*i),10)
        if ballvalid and timeRenew:end=int(clock())+ftime
        tick()

        re=[]
        if playing:showeffect()
        item()
        if starting:fire()
        for pos in range(len(user)):
            if user[pos]!=None:
                checkValid(pos)
                if playing:
                    balls(pos)
                    block(pos)
                cx,cy,sx,sy,ballPoint=user[pos]
                if int(cy)>768-radius and starting==0:re.append(user[pos])
        for i in re:user.remove(i)
    elif gameMode=="Play":
        while disPage:
            disPage=0
            level=displayMenu()
            setUp(level)
            drawBlock()
            
        "main game"
        mouse.set_visible(0)
        while paused:gamePause()

        updateScreen()            

        #lives
        for i in range (life):draw.circle(screen,(255,0,0),(10,30+25*i),10)
        #time
        if ballvalid and timeRenew:end=int(clock())+ftime
        tick()
        
        
        re=[] # lsit for removing elements from a list

        # in game stuff
        if playing:showeffect()
        item()
        if starting:fire()
        for pos in range(len(user)):
            if user[pos]!=None:
                checkValid(pos)
                if playing:
                    balls(pos)
                    block(pos)
                cx,cy,sx,sy,ballPoint=user[pos]
                if int(cy)>768-radius and starting==0:re.append(user[pos])
        for i in re:user.remove(i)
    elif gameMode=="2-Player Game":
        while disPage:
            disPage=0
            level=displayMenu()
            setUp(level)
            drawBlock()
        updateScreen()
        for i in range (life):draw.circle(screen,(255,0,0),(10,30+25*i),10)
        for i in range (life2):draw.circle(screen,(0,255,0),(10,500+25*i),10)
        re=[]
        if playing:showeffect()
        item()
        if starting:fire()
        if tstarting:fire2()
        for pos in range (len(user)):
            if user[pos]!=None:
                checkValid(pos)
                if playing:
                    balls(pos)
                    block(pos)
                cx,cy,sx,sy,ballPoint=user[pos]
                if int(cy)>768-radius and playing:re.append(user[pos])
                elif int(cy)<radius and playing:re.append(user[pos])
        for i in re:user.remove(i)  
        
    elif gameMode=="Create Levels":
        screen.fill((0,0,0))
        main()
        gameMode="Custom Levels"
    if lets[99]:
        time.Clock().tick(20)
    display.flip()
qa()

##To Do Lists:
"""
 Levels
 blob blocks
 shooter (done(?))
 Graphic
 Points (joseph)
 2P
 Put everything together(level editor/account)
 Split plateform(?)
"""
