"""
By: Edward Tsai and Joseph Zhou

This is our Final Project
We created and programmed a game that is similar to the game "breakout" or "DX-
Ball"
The object of the game is to clear all the blocks on the screen
It has some other features such as level editor, 2-Player mode and other cool
stuff
So enjoy...
"""
from pygame import *
from math import *
from random import *
from glob import *
from dis import *
from levelEditor import *
from levelEditor2 import *
from time import clock
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '20,50'

def qa():
    global fnt,cas
    quit()
    del fnt,cas
    
################################################################################
#################################### Set up ####################################
################################################################################

size=length,width=1200,768
screen=display.set_mode(size)
blockScreen=Surface(size) # subsurface to check ball collision
init()
mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
setBg=image.load('graphic\\backGround.jpg') # backgroun picture
titles=[image.load(i) for i in glob("graphic\\title\\*.png")] # pictures for title
currentTitle=0 # animation for the title

######################################ACCOUNT###################################
def entering(val1,val2):
    # able to type
    val1,val2=False, True
    return val1, val2
def typing(word,length):
    # getting inputing and convert it to output
    if evt.type==KEYDOWN and keyvalid:
        if evt.key in range(97,123):
            if lets[303]==1 or lets[304]==1:
                word+=chr(evt.key-32)
            else:
                word+=chr(evt.key)
        if evt.key==32:
            word+=" "
        if evt.key in range(40,58):
            if evt.key==50:
                if lets[303]==1 or lets[304]==1:
                    word+="@"
                else:
                    word+="2"
            else:
                word+=chr(evt.key)
        if evt.key==8:
            word=word[:-1]
    return word
def blitText(text,spot):
    # takes in a string and position, and blit a picture of the text
    textpic=fnt.render(text,1,(0,139,0))
    screen.blit(textpic,spot)
def centerText(text,y,font):
    # samething as a blitText but bliting on the center
    textPic=font.render(text,1,(255,255,255))
    picRect=textPic.get_rect()
    picRect.center=600,y
    screen.blit(textPic,picRect[0:2])
def account():
    # allows the user to log in, sign up, or play as a guest
    global fnt,evt,keyvalid,lets,word,screen,data,spot
    global names,passwords,levels,lpoints,emails,currentTitle
    global message,renewemail
    data=open("accounts.txt","r").read().split("\n")
    #lists for account information
    names=[] # usernames
    passwords=[] # passwords
    levels=[] # current levels
    lpoints=[] # scored points
    emails=[] # emails
    for i in range(len(data)):
        if data[i]!="":
            if i%5==0:
                names+=[data[i]]
            elif i%5==1:
                passwords+=[data[i]]
            elif i%5==2:
                levels+=[data[i]]
            elif i%5==3:
                lpoints+=[data[i]]
            elif i%5==4:
                emails+=[data[i]]
    #pictures
    login=image.load("pictures\\login.png")
    signup=image.load("pictures\\createaccount.png")
    guest=image.load("pictures\\guest.png")
    loginfo=image.load("pictures\\loginfo.png")
    loginwrong=image.load("pictures\\loginwrong.png")
    makeaccount=image.load("pictures\\makeaccount.png")
    enteremail=image.load("pictures\\enteremail.png")
    renewable=image.load("pictures\\renewable.jpg")
    unrenewable=image.load("pictures\\unrenewable.png")
    success=image.load("pictures\\success.jpg")
    usernamefault=image.load("pictures\\usernamefault.jpg")
    passwordfault=image.load("pictures\\passwordfault.jpg")
    #flags
    # each flag will trigger a page 
    startvalid=True#flag for main screen
    loginvalid=False#flag to control login choice
    signupvalid=False#flag to control signup choice
    clearvalid=True#flag for controlling things that only happen once in loop
    usernamevalid=True#flag for entering username mode
    passwordvalid=False#flag for entering password mode
    entervalid=False#flag for mode when done entering info
    namevalid=True#flag for making username
    emailvalid=False#flag for making email
    newpasswordvalid=False#flag for making password
    confirmationvalid=False#flag for confirming password
    forgetvalid=False#flag for forget button
    createvalid=False#flag for create button
    donevalid=False#flag for done entering email
    renewvalid=False#flag for valid renew of password
    renewinvalid=False#flag for invalid renew of password
    #initial values
    loginbox=Rect(50,260,423,284)#login button
    guestBox=Rect(500,350,225,96)#guest button
    signupbox=Rect(850,290,288,169)#signup button
    usernamebox=Rect(455+74,196+132,283,22)#box for entering username
    passwordbox=Rect(455+74,196+200,283,22)#box for entering password
    enterbox=Rect(455+118,196+240,167-118,251-240)#enter button
    #initial values
    username=""
    password=""
    newname=""
    newpassword=""
    confirmpassword=""
    email=""
    renewemail=""
    message=""
    newnamebox=Rect(403+88,315,313,20)#box for making username
    emailbox=Rect(403+88,357,313,20)#box for making email
    newpasswordbox=Rect(403+88,399,313,20)#box for making password
    confirmationbox=Rect(403+88,441,313,20)#box for confirming password
    forgetbox=Rect(455+118,196+258,170-118,270-258)#foget button
    cancelbox=Rect(510+88,476,69,20)#cancel button
    createbox=Rect(590+88,476,126,20)#create button
    donebox=Rect(455+121,196+243,161-121,257-243)#done button
    enteremailbox=Rect(338+88,337,350,31)#box for entering validifying email
    mainMenu=Rect(455+97,196+275,185-97,289-275)
    #font
    fnt=font.SysFont("Calibri",16)
    running=True
    while running:
        clicked=False
        keyvalid=False
        
        for evt in event.get():
            if evt.type==QUIT:
                return -1,-1,-1,-1
            if evt.type==KEYDOWN:
                keyvalid=True
            if evt.type==MOUSEBUTTONDOWN:
                clicked=True
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        lets=key.get_pressed()
        screen.blit(setBg,(0,0))
        currentTitle+=1
        if currentTitle>=59:currentTitle=0
        screen.blit(titles[currentTitle/5],(400,20))
        if lets[27]==1:
            return -1,-1,-1,-1
        if startvalid:
            # first page (login,guest,sign up)
            screen.blit(login,(50,255))
            screen.blit(guest,(500,350))
            screen.blit(signup,(850,290))
            if clicked:
                if loginbox.collidepoint(mx,my):
                    startvalid=False
                    loginvalid=True
                elif signupbox.collidepoint(mx,my):
                    startvalid=False
                    signupvalid=True
                elif guestBox.collidepoint(mx,my):
                    return 'guest',1,0,1
        elif loginvalid:
            #type in username, forget password,back to menu
            screen.blit(loginfo,(455,196))
            if usernamevalid:
                #typing username
                draw.rect(screen,(255,0,0),(455+73,196+131,143,17),1)
                username=typing(username,30)
                blitText(username,(455+74,196+132))
                for i in range(455+78,455+73+len(password)*12,12):
                    draw.circle(screen,(0,0,0),(i,405),5)
                if clicked:
                    if passwordbox.collidepoint(mx,my):
                        usernamevalid,passwordvalid=entering(usernamevalid,passwordvalid)
                    elif enterbox.collidepoint(mx,my):
                        usernamevalid,entervalid=entering(usernamevalid,entervalid)
                    elif mainMenu.collidepoint(mx,my):
                        loginvalid,startvalid=entering(loginvalid,startvalid)
                        clearvalid=True
                        username=""
                        password=""
                    elif forgetbox.collidepoint(mx,my):
                        usernamevalid,forgetvalid=entering(usernamevalid,forgetvalid)
                if lets[9]==1 and keyvalid:
                    usernamevalid,passwordvalid=entering(usernamevalid,passwordvalid)
                if lets[13]==1 and keyvalid:
                    usernamevalid,entervalid=entering(usernamevalid,entervalid)
            elif passwordvalid:
                #typeing password
                draw.rect(screen,(255,0,0),(455+73,196+199,143,17),1)
                password=typing(password,22)
                for i in range(455+78,455+73+len(password)*12,12):
                    draw.circle(screen,(0,0,0),(i,405),5)
                blitText(username,(455+74,196+132))
                if clicked:
                    if usernamebox.collidepoint(mx,my):
                        passwordvalid,usernamevalid=entering(passwordvalid,usernamevalid)
                    elif enterbox.collidepoint(mx,my):
                        passwordvalid,entervalid=entering(password,entervalid)
                    elif mainMenu.collidepoint(mx,my):
                        loginvalid,startvalid=entering(loginvalid,startvalid)
                        clearvalid=True
                        username=""
                        password=""
                    elif forgetbox.collidepoint(mx,my):
                        passwordvalid,forgetvalid=entering(passwordvalid,forgetvalid)
                if keyvalid:
                    if lets[13]==1:
                        passwordvalid,entervalid=entering(passwordvalid,entervalid)
                    if lets[9]==1:
                        passwordvalid,usernamevalid=entering(passwordvalid,usernamevalid)
            elif entervalid:
                #confirm the username and password
                if username in names:
                    spot=names.index(username)
                    if password==passwords[spot]:
                        # if it is correct, return name,levels,points,and email
                        return names[spot],levels[spot],lpoints[spot],emails[spot]
                    else:
                        screen.blit(loginwrong,(455,196))
                        display.flip()
                        time.wait(3000)
                        entervalid,clearvalid=entering(entervalid,clearvalid)
                        usernamevalid=True
                        password=""                  
                else:                
                    screen.blit(loginwrong,(455,196))
                    display.flip()
                    time.wait(3000)
                    entervalid,clearvalid=entering(entervalid,clearvalid)
                    usernamevalid=True
                    password=""                
            elif forgetvalid:
                #getting the password back
                screen.blit(enteremail,(455,196))
                renewemail=typing(renewemail,30)
                blitText(renewemail,(455+71,196+189))
                if clicked:
                    if donebox.collidepoint(mx,my):
                        forgetvalid,donevalid=entering(forgetvalid,donevalid)
                if lets[13]==1 and keyvalid:
                    forgetvalid,donevalid=entering(forgetvalid,donevalid)
            elif donevalid:
                if username in names and emails[names.index(username)]==renewemail:
                    screen.blit(renewable,(326+88,300))
                    ltextpic=fnt.render(passwords[names.index(username)],1,(0,0,0))
                    screen.blit(ltextpic,(338+88,337))#blits text on
                    display.flip()
                    time.wait(3000)
                    donevalid,usernamevalid=entering(donevalid,usernamevalid)
                    renewemail=""
                else:
                    screen.blit(unrenewable,(455,196))
                    display.flip()
                    time.wait(3000)
                    donevalid,usernamevalid=entering(donevalid,usernamevalid)
                    renewemail=""
        elif signupvalid:
            # sign up page
            # this mainly deals with typing in the right boxes
            screen.blit(makeaccount,(300+88,268))
            screen.blit(fnt.render(message,1,(255,0,0)),(388+105,268+9))
            if namevalid:
                draw.rect(screen,(255,255,255),newnamebox)
                draw.rect(screen,(255,0,0),newnamebox,1)
                newname=typing(newname,32)
                blitText(newname,(403+88,315))
                if clicked:
                    if emailbox.collidepoint(mx,my):
                        namevalid,emailvalid=entering(namevalid,emailvalid)
                    elif newpasswordbox.collidepoint(mx,my):
                        namevalid,newpasswordvalid=entering(namevalid,newpasswordvalid)
                    elif confirmationbox.collidepoint(mx,my):
                        namevalid,confirmationvalid=entering(namevalid,confirmationvalid)
                    elif cancelbox.collidepoint(mx,my):
                        namevalid,clearvalid=entering(namevalid,clearvalid)
                        signupvalid,startvalid=entering(signupvalid,startvalid)
                        namevalid=True
                        newname=""
                        newpassword=""
                        email=""
                        confirmpassword=""
                    elif createbox.collidepoint(mx,my):
                        namevalid,createvalid=entering(namevalid,createvalid)
                blitText(email,(403+88,357))
                for i in range(410+88,410+88+len(newpassword)*12,12):
                    draw.circle(screen,(0,0,0),(i,409),5)
                for i in range(410+88,410+88+len(confirmpassword)*12,12):
                    draw.circle(screen,(0,0,0),(i,451),5)
                if keyvalid:
                    if lets[9]==1: 
                        namevalid,emailvalid=entering(namevalid,emailvalid)
                    if lets[13]==1:
                        namevalid,createvalid=entering(namevalid,createvalid)
            elif emailvalid:
                draw.rect(screen,(255,255,255),emailbox)
                draw.rect(screen,(255,0,0),emailbox,1)
                email=typing(email,32)
                blitText(email,(403+88,357))
                if clicked:
                    if newnamebox.collidepoint(mx,my):
                        emailvalid,namevalid=entering(emailvalid,namevalid)
                    elif newpasswordbox.collidepoint(mx,my):
                        emailvalid,newpasswordvalid=entering(emailvalid,newpasswordvalid)
                    elif confirmationbox.collidepoint(mx,my):
                        emailvalid,confirmationvalid=entering(emailvalid,confirmationvalid)
                    elif cancelbox.collidepoint(mx,my):
                        emailvalid,clearvalid=entering(emailvalid,clearvalid)
                        signupvalid,startvalid=entering(signupvalid,startvalid)
                        namevalid=True
                        newname=""
                        newpassword=""
                        email=""
                        confirmpassword=""
                    elif createbox.collidepoint(mx,my):
                        emailvalid,createvalid=entering(emailvalid,createvalid)
                blitText(newname,(403+88,315))
                for i in range(410+88,410+88+len(newpassword)*12,12):
                    draw.circle(screen,(0,0,0),(i,409),5)
                for i in range(410+88,410+88+len(confirmpassword)*12,12):
                    draw.circle(screen,(0,0,0),(i,451),5)
                if keyvalid:
                    if lets[9]==1:
                        emailvalid,newpasswordvalid=entering(emailvalid,newpasswordvalid)
                    if lets[13]==1:
                        emailvalid,createvalid=entering(emailvalid,createvalid)
            elif newpasswordvalid:
                draw.rect(screen,(255,255,255),newpasswordbox)
                draw.rect(screen,(255,0,0),newpasswordbox,1)
                newpassword=typing(newpassword,24)
                for i in range(410+88,410+88+len(newpassword)*12,12):
                    draw.circle(screen,(0,0,0),(i,409),5)
                if clicked:
                    if newnamebox.collidepoint(mx,my):
                        newpasswordvalid,namevalid=entering(newpasswordvalid,namevalid)
                    elif emailbox.collidepoint(mx,my):
                        newpasswordvalid,emailvalid=entering(newpasswordvalid,emailvalid)
                    elif confirmationbox.collidepoint(mx,my):
                        newpasswordvalid,confirmationvalid=entering(newpasswordvalid,confirmationvalid)
                    elif cancelbox.collidepoint(mx,my):
                        signupvalid,startvalid=entering(signupvalid,startvalid)
                        newpasswordvalid,clearvalid=entering(newpasswordvalid,clearvalid)
                        namevalid=True
                        newname=""
                        newpassword=""
                        email=""
                        confirmpassword=""
                    elif createbox.collidepoint(mx,my):
                        newpasswordvalid,createvalid=entering(newpasswordvalid,createvalid)
                blitText(email,(403+88,357))
                blitText(newname,(403+88,315))
                for i in range(410+88,410+88+len(confirmpassword)*12,12):
                    draw.circle(screen,(0,0,0),(i,451),5)
                if keyvalid:
                    if lets[9]==1:
                        newpasswordvalid,confirmationvalid=entering(newpasswordvalid,confirmationvalid)
                    if lets[13]==1:
                        newpasswordvalid,createvalid=entering(newpasswordvalid,createvalid)
            elif confirmationvalid:
                draw.rect(screen,(255,255,255),confirmationbox)
                draw.rect(screen,(255,0,0),confirmationbox,1)
                confirmpassword=typing(confirmpassword,32)
                for i in range(410+88,410+88+len(confirmpassword)*12,12):
                    draw.circle(screen,(0,0,0),(i,451),5)
                if clicked:
                    if newnamebox.collidepoint(mx,my):
                        confirmationvalid,namevalid=entering(confirmationvalid,namevalid)
                    elif emailbox.collidepoint(mx,my):
                        confirmationvalid,emailvalid=entering(confirmationvalid,emailvalid)
                    elif newpasswordbox.collidepoint(mx,my):
                        confirmationvalid,newpasswordvalid=entering(confirmationvalid,newpasswordvalid)
                    elif cancelbox.collidepoint(mx,my):
                        signupvalid,startvalid=entering(signupvalid,startvalid)
                        confirmationvalid,clearvalid=entering(confirmationvalid,clearvalid)
                        namevalid=True
                        newname=""
                        newpassword=""
                        email=""
                        confirmpassword=""
                    elif createbox.collidepoint(mx,my):
                        confirmationvalid,createvalid=entering(confirmationvalid,createvalid)
                blitText(newname,(403+88,315))
                blitText(email,(403+88,357))
                for i in range(410+88,410+88+len(newpassword)*12,12):
                    draw.circle(screen,(0,0,0),(i,409),5)
                if keyvalid:
                    if lets[13]==1:
                        confirmationvalid,createvalid=entering(confirmationvalid,createvalid)
                    if lets[9]==1:
                        confirmationvalid,namevalid=entering(confirmationvalid,namevalid)
            elif createvalid:
                if confirmpassword==newpassword:
                    if newname not in names:
                        if newname!="" and newpassword!="" and email!="" and confirmpassword!="":
                            names+=[newname]
                            emails+=[email]
                            passwords+=[newpassword]
                            lpoints+=["0"]
                            levels+=["1"]
                            data=open("accounts.txt","w")
                            for i in range(len(names)):
                                data.write(names[i]+"\n"+passwords[i]+"\n"+levels[i]+"\n"\
                                           +lpoints[i]+"\n"+emails[i]+"\n") 
                            data.close()
                            createvalid,clearvalid=entering(createvalid,clearvalid)
                            signupvalid,startvalid=entering(signupvalid,startvalid)
                            newname=""
                            newpassword=""
                            email=""
                            confirmpassword=""
                            namevalid=True
                        else:
                            createvalid,namevalid=entering(createvalid,namevalid)
                    else:
                        message="Username already exists"
                        createvalid,namevalid=entering(createvalid,namevalid)
                        newname=""                   
                        email=""
                        clearvalid=True
                else:
                    message="Password and verify does not match"
                    createvalid,namevalid=entering(createvalid,namevalid)
                    newpassword=""
                    confirmpassword=""
                    clearvalid=True
        display.flip()
n,l,s,e=account() 
if l==-1:
    qa()
if n!='guest':
    l,s=int(l),int(s)
    nameplace=names.index(n)
sub=int(s)
################################################################################
#################################### Variables #################################
################################################################################

#ball's initial position(when its on the plateform)def levelSetUp(n):
bx,by=512,738
tbx,tby=512,30
#platform position
px,py=412,748
tpx,tpy=412,0
#flags
tstarting=1# for two player
paused=leftClick=helps=select=playing=rightvalid=False
"""pause, select, helps, are variables to keep tracf of current game status.
leftClick, playing and rightvalid are checking the user's current status"""
leftvalid=starting=ballvalid=timeRenew=menu=gameMode=True
"""left valid, starting, ballvalid, timeRenew are the user's current status.
menu, gameMode is to keep track of the current game status."
"""
#initial values
fnt=font.SysFont('Courier',20) # font
cas=font.SysFont('calibri',34)

user=[]
"""a list to keep track of all the infomation about the balls
user=[[ball x,y, change in x,y],[center of the ball from last 10 update]"""
# we didn't user the last 10 update part because we fount another way to
# solve our problem, but it was too much work to take it out, so we left
# it there.

#background/text
address='graphic\\text\\'
backgrounds=[image.load(i) for i in glob('graphic\\bg\\*.png')]
"list of all the backgrounds"
bg=backgrounds[0] # the current background
texts=[image.load(address+str(i)+".png") for i in range(10)] # all the texts
helpPage=image.load('graphic\\text\\help.png') # the help page
cox=-2600+768 # background's x position
cot=1 # if the background is subtracting or adding

#music 
musicList=glob('sound\\music\\*') # list of music file names
curMus=0 # current playing music
myMusic=mixer.music # short cut
musSta="Play" # music status
#sound
effect=mixer.Sound('sound\\Effect.wav')
saucer=mixer.Sound('sound\\Saucer.wav')
aoLaser=mixer.Sound('sound\\Ao-laser.wav')
gun=mixer.Sound('sound\\Gunfire.wav')
byeBall=mixer.Sound('sound\\Byeball.wav')
#pictures/graphics
address='graphic\\Done\\'
picBall=image.load(address+'ball10.png')

picPad=image.load(address+'paddle.png')
picWhi=image.load(address+'Normal Block.png')
picGre=image.load(address+'Green Block.png')
picGra=image.load(address+'Gray Block.png')
picBro=image.load(address+'Bronze Block.png')
picSil=image.load(address+'Silver Block.png')
picGol=image.load(address+'Gold Block.png')

effBlu=transform.scale(image.load(address+'effBlue.png'),(12,12))
effGre=transform.scale(image.load(address+'effGreen.png'),(12,12))
effRed=transform.scale(image.load(address+'effRed.png'),(12,12))
effYel=transform.scale(image.load(address+'effYellow.png'),(12,12))

#pictures for the account function
scoreboard=image.load("pictures\\scoreboard.jpg")
alarmclock=image.load("pictures\\alarmclock.jpg")
goback=image.load("pictures\\goback.bmp")
restart=image.load("pictures\\restart.bmp")
pauseGame=image.load("pictures\\pause.png")
resume=image.load("pictures\\playbutton.png")
startbutton=image.load("pictures\\start.png")
helpbutton=image.load("pictures\\help.png")
oneplayerword=image.load("pictures\\1playerword.png")
twoplayerword=image.load("pictures\\2playerword.png")
customlevelword=image.load("pictures\\customlevels.png")
backword=image.load("pictures\\backword.png")
playword=image.load("pictures\\playword.png")
createword=image.load("pictures\\createword.png")
#boxes
gobackbox=Rect(1024,707,59,59)
pausebox=Rect(1079,707,59,59)
restartbox=Rect(1138,707,59,59)

re=[]# a list to delete elements inside another list (short for remove)
cx,cy=0,0 # ball's position
sx,sy=0,0 # ball's change in x and y
items=[] # all the power-ups that are falling on the screen
end=int(clock())+300 # playing time
radius=10 # radius of the ball
speed=1.0 # the speed of the ball
life=life2=2 # the number of lives
timeChange=0 # a flag to turn on the count down
disPage=1 # a flag to reset the level
bullets=[] # list of the bullets shot by "shooter"
shotKey=0  # the "w" key on the keyboard, a flag to check if it is pressed
nBut=bBut=mBut=0 # the 'b','n','m' keys on the keyboard, check if they are pressed
hsvalid=0 # whether to show highscore or not
#power effects
timer=[0] # the timer for each power
effects=['normal()'] # list that holds all the powers
blockColours=[(30,144,255),(0,255,0),(139,69,19),(192,192,192),(225,225,0)\
              ,(255,50,50),(100,100,100),(0,0,255)]# different block colours
colours=[(255,255,0),(255,0,255),(255,50,50),(50,255,50),(255,255,255),\
         (0,255,255),(200,200,200),(169,69,19),(50,10,176)] # all the colours for each power-up
##choose=[colours.index(i) for i in fcolours] # power-ups that can be use in the game
power=['bigball()','smallball()','fastball()','slowball()',\
       'pause()','addtime()','shield()','shooter()','multiball()'] # a list with all the power-up function
blocks=[[] for x in range (len(blockColours))]# all the blocks currently in game
blocks[0].append(123) # so the blocks wont be empty
quiting=False # flag to close the whole program

points=[(-1,1),(1,-1),(-1,1),(1,-1)]
#after collision with a block with either of the four points on the circle
#(up,left,right,down) will change the balls direction, this lists will
#be multiplied through sx,sy in order to change the direction

def setUp(n):
    "this function will set up each level before game starts"
    "basically resets all the variable back to default"
    "and load a new level"
    global ftime,fcolours,fblocks,bx,by,px,py,paused,select,playing,rightvalid
    global leftvalid,starting,ballvalid,timeRenew,user,end,items,timeChange
    global bullets,shotKey,timer,effects,choose,blocks,shotKey2,tdirect
    global tbx,tby,tpx,tpy,tl,tr,tstarting,life,life2,s,hsvalid,quiting
    global bg,cox,cot
    ftime,fcolours,fblocks=map(eval,open(n).read().split("\n"))
    "read the infomation in the files for time,effects,and blocks"
    bx,by=512,738
    px,py=412,748    
    tpx,tpy=412,0
    tbx,tby=512,30
    tstarting=1
    paused=select=playing=rightvalid=quiting=False
    leftvalid=starting=ballvalid=timeRenew=hsvalid=True
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
    cox=-2600+768
    cot=1

    bg=choice(backgrounds)
    
    blocks=[[] for x in range (len(blockColours))]
    for i in fblocks:
        for j in range (len(blockColours)):
            if i[0]==blockColours[j]:blocks[j].append(Rect(i[1]))    

################################################################################
################################# Ball and Blocks ##############################
################################################################################
            
def drawBlock():
    "this function will take all the element in blocks and draw it onto"
    "the back surfact - blockScreen"
    blockScreen.fill((0,0,0))
    for pos in range(len(blocks)):
        for each in blocks[pos]:draw.rect(blockScreen,blockColours[pos],each)

def boundary(gameMode):
    "this function will draw the boundary (blue walls) around the corner"
    draw.rect(screen,(0,0,255),(0,0,20,768))
    draw.rect(screen,(0,0,255),(1004,0,20,768))
    if gameMode!="2-Player Game":
        draw.rect(screen,(0,0,255),(0,0,1024,20))

def checkValid(pos):
    "check if the ball is inside each wall, if it is, move it out"
    cx,cy,sx,sy,ballPoint=user[pos]
    if cx-radius<20:
        cx,sx=21+radius,sx*-1
        aoLaser.play()
    elif cx+radius>1004:
        cx,sx=1003-radius,sx*-1
        aoLaser.play()
    elif cy-radius<20 and gameMode!="2-Player Game":
        sy,cy=sy*-1,21+radius
        aoLaser.play()
    user[pos]=cx,cy,sx,sy,ballPoint

def drawBall():
    "draws every single ball in user"
    for i in user:
        if i!=None:
            a,b,c,d,p=i
            screen.blit(picBall,(a-radius,b-radius))
        
def tick():
    "the time count down function"
    if gameMode!='2-Player Game':
        screen.blit(alarmclock,(1024,283))
        pic=fnt.render(str(end-int(clock())),1,(0,255,0))
        screen.blit(pic,(1093,310))
    else:
        global end
        end+=1
    
def movePlat():
    "moves the plateform when the user input from keyboard"
    global px,bx
    screen.blit(picPad,(px,py))
    if lets[97]==1 and px>20:
        px-=10
        if starting:bx-=10
    elif lets[100]==1 and px<804:
        px+=10
        if starting:bx+=10
        
def movePlat2():
    global tpx,tbx
    screen.blit(picPad,(tpx,tpy))
    if lets[276] and tpx>20:
        tpx-=10
        if tstarting:tbx-=10
    elif lets[275] and tpx<804:
        tpx+=10
        if tstarting:tbx+=10

def fire():
    "when the ball is still on the plateform, the ball will move right and left"
    "when the user hit 'w' the ball will leave the plateform"
    "this function takes care of that"
    global leftvalid,rightvalid,starting,playing,dist,ang,ballvalid,ballAdd
    global timeRenew,bx,by,user,tbx,tby,timeChange
    if leftvalid:
        bx-=4
        if bx<=px+50:leftvalid,rightvalid=0,1
    elif rightvalid:
        bx+=4
        if bx>=px+150:rightvalid,leftvalid=0,1
    if shotKey:
        starting=ballvalid=timeRenew=0
        playing=True
        cx,cy=bx,by
        dist=hypot(px+100-bx,py-by)
        ang=acos((px+100-bx)/dist)
        sx,sy=-cos(ang)*2,-sin(ang)*2
        user.append([cx,cy,sx,sy,[]])
def fire2():
    global tdirect,tstarting,playing,tbx,tby,user,playing
    if tdirect:
        tbx-=4
        if tbx<=tpx+50:tdirect=0
    else:
        tbx+=4
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
    global dist,ang,radius,po
    cx+=sx*speed
    cy+=sy*speed
    po=range(px-radius/2,px+200+radius/2)
    if (int(cy)in range(748-radius,758-radius) and int(cx) in po):
        "this is to reset the angle of the ball when the ball hits the paddle"
        sx,sy=findAng(px,py,cx,cy,1)
        aoLaser.play()
    elif gameMode=="2-Player Game":
        po=range(tpx-radius/2,tpx+200+radius/2)
        if (int(cy) in range (15+radius,25+radius) and int(cx) in po):
            sx,sy=findAng(tpx,tpy,cx,cy,0)
            aoLaser.play()
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
        if cpoints[point][1]<764 and cpoints[point][1]>0:
            if blockScreen.get_at(cpoints[point])!=(0,0,0):
                "if the colour at that pixel is not black"
                "I know the ball is colliding with a block"
                colourPos=blockScreen.get_at(cpoints[point])
                colourPos=blockColours.index(colourPos) # get the index of the colour at the pixel in blockColours
                if point in [0,1,2,3]:
                    sx*=points[point][0]
                    sy*=points[point][1]
                    cx,cy=findPos(cpoints[point],colourPos,sx,sy,cx,cy,point)
                    break
                else:
                    sx,sy,cx,cy=findPos(cpoints[point],colourPos,sx,sy,cx,cy,'True')
                    break
    user[pos]=cx,cy,sx,sy,ballPoint

    
def findPos(p,c,sx,sy,cx,cy,valid):
    " find out which type of block it colliding with the ball"
    global blocks
    for block in range(len(blocks)):
        for each in blocks[block]:
            if each.collidepoint(p):
                blockEffect(c,each,block)
                ox,oy=each[0]+each[2]/2.0,each[1]+each[3]/2.0 # center of the block
                dx,dy=ox-p[0],oy-p[1] # center of the block - point of collision
                if valid=='True':
                    a=atan(sy/sx)
                    x,y=radius*cos(a)+1,radius*sin(a)+1
                    if dx<0:
                        if dy<0:
                            cx,cy=each[0]+each[2]+radius+1,each[1]+each[3]+radius+1
                            return -sy,-sx,cx,cy
                        elif dy>0:
                            cx,cy=each[0]+each[2]+radius+1,each[1]-radius-1
                            return sy,sx,cx,cy
                    elif dx>0:
                        if dy>0:
                            cx,cy=each[0]-radius-1,each[1]-radius-1
                            return -sy,-sx,cx,cy
                        elif dy<0:
                            cx,cy=each[0]-radius-1,each[1]+each[3]+radius+1
                            return sy,sx,cx,cy
                elif valid==2:return each[0]+each[2]+radius,cy
                elif valid==0:return each[0]-radius,cy
                elif valid==3:return cx,each[1]+each[3]+radius
                elif valid==1:return cx,each[1]-radius
def blockEffect(col,block,pos):
    global s
    """
    each type of blocks has different effects on the gameplay.
    0 is normal
    1 is power-ups
    2 and 5 turn into 0
    3 turns into 2
    4 turns into 3
    6 cannot be destoried

    """
    
    re=[]
    if col==0:
        re.append((pos,block))
        s+=10
    elif col==1 and len(choose)!=0:
        s+=10
        num=choice(choose)
        if gameMode=="2-Player Game":
            direction=choice([-3,3])
        else:
            direction=3
        if num in [0,1]:current=effBlu
        elif num in [2,3,4]:current=effYel
        elif num in [5,6,7,8]:current=effGre
        items.append([[block[0]+35,block[1]],num,direction,current])
        re.append((pos,block))
    elif col==2 or col==5:
        s+=30
        blocks[0].append(block)
        re.append((pos,block))
    elif col==3:
        blocks[2].append(block)
        re.append((pos,block))
        s+=20
    elif col==4:
        blocks[3].append(block)
        re.append((pos,block))
        s+=30
    elif col==7:
        re.append((pos,block))
    elif col==6:
        effect.play()
    for i in re:
        saucer.play()
        pos,stuff=i
        blocks[pos].remove(stuff)
    drawBlock()

def item():
    "After a green block is hit, it will drop a power-up"
    "this function will randomly generate a power-up and controls all the"
    "movement of each power-up"
    re=[]
    for i in range(len(items)):
        center,num,direction,current=items[i]
        screen.blit(current,(center[0]-6,center[1]-6))
        items[i][0]=items[i][0][0],items[i][0][1]+direction
        if items[i][0][1]>760:
            re.append(items[i])
            if items[i][0][0] in range(px,px+200) :
                "if the power-up landed on the paddle, the effect will apply"
                "to the user"
                if num not in [5,8,6]:
                    if num in [4]:
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
                if num not in [5,8,6]:
                    if num in [4]:
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
        pic=fnt.render(effects[i][:-2]+"   "+str(timer[i][1]-timer[i][0]),1,timer[i][2])
        screen.blit(pic,(1030,i*30+400))
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
################################# Effect Function ##############################
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
    global radius,picBall
    picBall=transform.scale(image.load('graphic\\Done\\ball10.png'),(26,26))
    radius=13
def smallball():
    " makes the ball smaller"
    global radius,picBall
    picBall=transform.scale(image.load('graphic\\Done\\ball10.png'),(14,14))
    radius=7
def addtime():
    " adds 20 seconds to the clock"
    global end
    end+=20
def fastball():
    " makes the ball move faster"
    global speed
    speed=4
def slowball():
    " makes the ball move slower"
    global speed
    speed=2
def pause():
    " stops the ball"
    global speed
    speed=0
def shield():
    global blocks,blockColours
    " creates a shield at the bottom of the screen to prevent the ball from"
    " falling"    
    blocks[-1]+=[Rect(0,748,1024,13)]
    if gameMode=="2-Player Game":
        blocks[-1]+=[Rect(0,10,1024,13)]
    drawBlock()
def shooter():
    " allow users to shoot bullets that will help to break the blocks for them"
    global bullets
    if shotKey and len(bullets)<10:
        bullets.append([[px+90,728,3,3],5])
        gun.play()
    if gameMode=="2-Player Game" and shotKey2 and len(bullets)<20:
        bullets.append([[tpx+90,40,3,3],-5])
        gun.play()
    re=[]
    for i in range (len(bullets)):
        draw.rect(screen,(255,255,0),bullets[i][0])
        direction=bullets[i][-1]
        bullets[i][0][1]-=direction
        x,y,l,w=bullets[i][0]
        if blockScreen.get_at((x,y))!=(0,0,0):
            colourPos=blockScreen.get_at((x,y))
            colourPos=blockColours.index(colourPos)
            findPos((x,y),colourPos,0,0,0,0,123)
            re.append(bullets[i])
        elif blockScreen.get_at((x+l,y))!=(0,0,0):
            colourPos=blockScreen.get_at((x+l,y))
            colourPos=blockColours.index(colourPos)
            findPos((x+l,y),colourPos,0,0,0,0,123)
            re.append(bullets[i])
        elif y<21:re.append(bullets[i])
        elif y>749:re.append(bullets[i])
    for i in re:bullets.remove(i)
                
def normal():
    " returns everything back to normal"
    global radius,speed,shots,heights,bullets,picBall
    radius=10
    picBall=transform.scale(image.load('graphic\\Done\\ball10.png'),(20,20))
    shots=[]
    heights=[]
    speed=3
    
################################################################################
#################################### Game play #################################
################################################################################

def updateScreen():
    " this function will update all the graphics of the screen"
    " and music"
    global curMus,musSta
    #blocks
    pictures=[picWhi,picGre,picBro,picSil,picGol]
    for i in range(0,5):
        for each in blocks[i]:
            x,y,l,w=each
            screen.blit(pictures[i],(x,y))
    for each in blocks[-1]:draw.rect(screen,blockColours[-2],each)
    for each in blocks[-2]:
        x,y,l,w=each
        screen.blit(picGra,(x,y))
    #boundaries
    boundary(gameMode)        
    #platform
    movePlat()
    if gameMode=="2-Player Game":movePlat2()
    #ball
    if starting:screen.blit(picBall,(bx-radius,by-radius))
    if tstarting and gameMode=="2-Player Game":
        screen.blit(picBall,(tbx-radius,tby-radius))
    drawBall()
    curMus,musSta=playMusic(curMus,musSta)



def gameover(n):
    " when the game is over, redirect the screen back to main menu"
    global gameMode,select,disPage,s,hsvalid,menu,currentTitle,helps,playing
    global life,blocks
    screen.blit(setBg,(0,0))
    currentTitle+=1
    if currentTitle>=59:currentTitle=0
    screen.blit(titles[currentTitle/5],(400,20))
    centerText(n,375,cas)
    centerText("going back to main menu",425,cas)
    display.flip()
    time.wait(3000)
    while hsvalid and gameMode=="1-Player Mode":
        highScores()
    gameMode="0"
    menu=1
    select=helps=playing=0
    blocks[0]+=[None]
    life=2
    disPage=1

    
def highScores():
    " displays the highscores"
    global hsvalid,quitting,leftclick,tempscores,currentTitle,menu
    leftclick=0
    screen.fill((0,0,0))
    for evt in event.get():
        if evt.type==QUIT:hsvalid,quitting=0,1
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==1:
                leftclick=1
        if evt.type==KEYDOWN:
            if evt.key==27:hsvalid,quitting=0,1
    if leftclick:hsvalid=False
    screen.blit(setBg,(0,0))
    currentTitle+=1
    if currentTitle>=59:currentTitle=0
    screen.blit(titles[currentTitle/5],(400,20))
    tempscores=[]
    for i in range(len(lpoints)):
        tempscores+=[(lpoints[i],names[i])]
    tempscores.sort(reverse=True)
    if len(tempscores)<=10:
        for i in range(len(tempscores)):
            blitText("%-30s%30s"%(tempscores[i][1],str(tempscores[i][0])),(250,150+i*50))
    else:
        for i in range(10):
            blitText("%-30s%30s"%(tempscores[i][1],str(tempscores[i][0])),(250,150+i*50))
    display.flip()

def playMusic(cur,musSta):
    " this function controls the music in game"
    if nBut:
        myMusic.stop()
    elif bBut:
        myMusic.stop()
        cur-=2
        if cur==-2:cur=len(musicList)-2
    if mBut:
        if musSta=="Stop":musSta="Play"
        elif musSta=="Play":musSta="Stop"
    if musSta=="Stop":myMusic.stop()
    if myMusic.get_busy()==0 and musSta=="Play":        
        myMusic.load(musicList[cur])
        myMusic.play()
        cur+=1
        if cur==len(musicList):cur=0
    return cur,musSta

def run():
    " main event"
    global shotKey,user,leftClick,paused,bullets
    global life,timer,effects,starting,playing,ballvalid,shotKey2
    global px,py,keyvalid,l,bx,by,items,disPage,levels,disPage
    global tpx,tpy,tbx,tby,life2,tdirect,tstarting,clicked,s,menu,select,gameMode
    global nBut,bBut,mBut
    leftClick=0
    keyvalid=clicked=False
    shotKey=shotKey2=0
    nBut=bBut=mBut=0
    for evt in event.get():
        if evt.type==QUIT:gameMode,disPage,menu="",1,1
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==1:clicked=1
        if evt.type==KEYDOWN:
            keyvalid=True
            if evt.key==27:gameMode,disPage,menu="",1,1
            if evt.key==119:shotKey=1
            if evt.key==273:shotKey2=1
            if evt.key==112:paused=1
            if evt.key==110:nBut=1
            if evt.key==109:mBut=1
            if evt.key==98:bBut=1
    if len(user)==1 and playing:
        if life==0:
            s=sub
            gameover('You lost! Game Over')
        else:
            if gameMode!="2-Player Game":
                byeBall.play()
                normal()
                life-=1
                timer=[0]
                items=[]
                effects=['normal()']
                starting=ballvalid=timeRenew=leftvalid=1
                playing=paused=startGame=helps=rightvalid=select=False
                px=412
                py=748
                bx,by=512,738
                user=[None]
                bullets=[]
            else:
                if starting==0 and tstarting==0:
                    byeBall.play()
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
                    starting=ballvalid=timeRenew=leftvalid=1
                    playing=paused=startGame=helps=rightvalid=select=False
                    px=412
                    py=748
                    bx,by=512,738
                    user=[None]
                    bullets=[]
    if end-int(clock())<0 and playing:
        s=sub
        gameover('Time\'s Up! Game over')
    valid=1
    for i in blocks[:-2]:
        if len(i)!=0:valid=0
    if valid:
        if gameMode!="1-Player Game":gameover('You Beat the Level')
        else:
            l+=1
            disPage=1
    return 1

def menuRun():
    "the menu page in the beginning of the screen, play or help"
    global menu,select,leftClick,mx,my,mp,helps,pageStatus,quiting,currentTitle
    leftClick=0
    for evt in event.get():
        if evt.type==QUIT:menu,quiting=0,1
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==1:leftClick=1
        if evt.type==KEYDOWN:
            if evt.key==27:menu,quiting=0,1
    myMusic.stop()
    mx,my=mp=mouse.get_pos()
    screen.blit(setBg,(0,0))
    currentTitle+=1
    if currentTitle>=59:currentTitle=0
    screen.blit(titles[currentTitle/5],(400,20))
    startRect=texts[0].get_rect()
    startRect.center=600,360
    screen.blit(texts[0],(startRect[0],startRect[1]))
    helpRect=texts[1].get_rect()
    helpRect.center=600,577
    screen.blit(texts[1],(helpRect[0],helpRect[1]))


    if startRect.collidepoint(mp) and leftClick:select,menu=1,0
    elif helpRect.collidepoint(mp) and leftClick:menu,helps=0,1
    display.flip()

def helpRun():
    " the help page"
    global leftClick,mx,my,mp,menu,helps,quiting,currentTitle,select,gameMode
    leftClick=0
    for evt in event.get():
        if evt.type==QUIT:helps,quiting=0,1
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==1:leftClick=1
        if evt.type==KEYDOWN:
            if evt.key==27:helps,quiting=0,1
    mx,my=mp=mouse.get_pos()
    screen.blit(helpPage,(0,0))
    currentTitle+=1
    if currentTitle>=59:currentTitle=0
    screen.blit(titles[currentTitle/5],(400,20))

    if leftClick:helps,menu,select,gameMode=0,1,0,""
    display.flip()

def selectRun():
    " the selecting game mode page, 1-player, 2-player, or custom levels"
    global leftClick,select,mx,my,mp,menu,gameMode,quiting,currentTitle
    leftClick=0
    for evt in event.get():
        if evt.type==QUIT:select,quiting=0,1
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==1:leftClick=1
        if evt.type==KEYDOWN:
            if evt.key==27:select,quiting=0,1
    myMusic.stop()
    mx,my=mp=mouse.get_pos()
    screen.blit(setBg,(0,0))
    currentTitle+=1
    if currentTitle>=59:currentTitle=0
    screen.blit(titles[currentTitle/5],(400,20))
    oneRect=texts[2].get_rect()
    oneRect.center=600,200
    twoRect=texts[3].get_rect()
    twoRect.center=600,350
    cusLev=texts[4].get_rect()
    cusLev.center=600,500
    backRect=texts[5].get_rect()
    backRect.center=600,650
    screen.blit(texts[2],(oneRect[0],oneRect[1]))
    screen.blit(texts[3],(twoRect[0],twoRect[1]))
    screen.blit(texts[4],(cusLev[0],cusLev[1]))
    screen.blit(texts[5],(backRect[0],backRect[1]))
    if leftClick:
        if oneRect.collidepoint(mp):gameMode,select='1-Player Game',0
        elif twoRect.collidepoint(mp):gameMode,select='2-Player Game',0
        elif cusLev.collidepoint(mp):gameMode,select='Custom Levels',0
        elif backRect.collidepoint(mp):select,menu=0,1
    display.flip()

levelEdit=0

def customRun():
    " the custom levels page, where user can select to play, or create levels"
    global leftClick,gameMode,select,mx,my,mp,quiting,currentTitle
    leftClick=0
    for evt in event.get():
        if evt.type==QUIT:select,gameMode,quiting=1,0,1
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==1:leftClick=1
        if evt.type==KEYDOWN:
            if evt.key==27:select,gameMode,quiting=1,0,1
    mx,my=mp=mouse.get_pos()
    screen.blit(setBg,(0,0))
    currentTitle+=1
    if currentTitle>=59:currentTitle=0
    screen.blit(titles[currentTitle/5],(400,20))

    playRect=texts[6].get_rect()
    playRect.center=600,200
    creLev=texts[7].get_rect()
    creLev.center=600,350
    sty1=texts[8].get_rect()
    sty1.center=600,450
    sty2=texts[9].get_rect()
    sty2.center=600,510
    backRect=texts[5].get_rect()
    backRect.center=600,640
    screen.blit(texts[5],(backRect[0],backRect[1]))
    screen.blit(texts[6],(playRect[0],playRect[1]))
    screen.blit(texts[7],(creLev[0],creLev[1]))
    screen.blit(texts[8],(sty1[0],sty1[1]))
    screen.blit(texts[9],(sty2[0],sty2[1]))

    if leftClick:
        if playRect.collidepoint(mp):gameMode="Play"
        elif sty1.collidepoint(mp):gameMode="Style 1"
        elif sty2.collidepoint(mp):gameMode="Style 2"
        elif backRect.collidepoint(mp):select,gameMode=1,""
##            if selectionPage[i]=="Back":select,gameMode=1,""
##            else:gameMode=selectionPage[i]
    display.flip()

def gamePause():
    "pausing the game while in game"
    global paused,timeChange,end,mx,my,quiting
    for evt in event.get():
        if evt.type==QUIT:
            paused=0
            mouse.set_visible(1)
        if evt.type==KEYDOWN:
            if evt.key==112:
                paused=0
                mouse.set_visible(1)
        if evt.type==MOUSEBUTTONDOWN:
            paused=0
            mouse.set_visible(1)
    mx,my=mp=mouse.get_pos()
    screen.fill((0,0,0))
    screen.blit(resume,mp)
    pic=fnt.render("Click to Resume",1,(255,255,255))
    screen.blit(pic,(mx-70,my+59))
    if timeChange!=int(clock()):
        end+=1
        timeChange=int(clock())
    display.flip()

while run():
    " main loop"
    mx,my=mp=mouse.get_pos()
    mb=mouse.get_pressed()
    lets=key.get_pressed()
    screen.blit(bg,(0,cox))
    if cot:cox+=0.1
    else:cox-=0.2
    if cox>=0:cot=0
    elif cox<=-2600+768:cot=1
    
    while menu:menuRun()
    while select:selectRun()    
    while helps:helpRun()
    while gameMode=="Custom Levels":customRun()
    
    screen.blit(goback,(1024,707))
    screen.blit(pauseGame,(1079,707))
    screen.blit(restart,(1138,707))
    screen.blit(scoreboard,(1024,100))
    screen.subsurface(Rect(1024,408,176,707-408)).fill((0,0,0))
    scoretext=fnt.render(str(s),1,(0,0,0))
    screen.blit(scoretext,(1070,180))
    
    if clicked:
        if gobackbox.collidepoint(mp):
            select=1
            disPage=1
            gameMode="0"
            s=sub
        elif pausebox.collidepoint(mp):
            paused=1
            mouse.set_visible(0)
        elif restartbox.collidepoint(mp):
            disPage=1
    
    if gameMode=="1-Player Game":
        while paused:gamePause()
        if disPage:
            disPage=0
            level="1p\\level "+str(l)+".txt"
            setUp(level)
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
                if int(cy+sy)>768-radius and starting==0:re.append(user[pos])
        for i in re:user.remove(i)
    elif gameMode=="Play":
        while disPage:
            disPage=0
            level=displayMenu()
            setUp(level)
            drawBlock()
            
        "main game"
        
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
                if int(cy+sy)>768-radius and starting==0:re.append(user[pos])
        for i in re:user.remove(i)
    elif gameMode=="2-Player Game":
        while paused:gamePause()
        while disPage:
            disPage=0
            level=displayMenu()
            setUp(level)
            drawBlock()
        updateScreen()
        for i in range (life):draw.circle(screen,(255,0,0),(10,30+25*i),10)
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
                if int(cy+sy)>768-radius-1 and playing:
                    re.append(user[pos])
                elif int(cy+sy)<radius+1 and playing:
                    re.append(user[pos])
        for i in re:user.remove(i)
        if ballvalid and timeRenew:end=int(clock())+ftime
        tick()
    elif gameMode=="Style 1":
        screen.fill((0,0,0))
        main()
        gameMode="Custom Levels"
    elif gameMode=="Style 2":
        screen.fill((0,0,0))
        main2()
        gameMode="Custom Levels"
    display.flip()
    if quiting:break
qa()
if n!='guest' and n!=-1:
    lpoints[nameplace]=str(s)
    levels[nameplace]=str(l)
    data=open("accounts.txt","w")
    for i in range(len(names)):
        data.write(names[i]+"\n"+passwords[i]+"\n"+levels[i]+"\n"\
                    +lpoints[i]+"\n"+emails[i]+"\n")
    data.close()


