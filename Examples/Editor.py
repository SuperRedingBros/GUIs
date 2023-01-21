import guis

#print(dir(guis))

from guis import *
import pygame
pygame.init()

usefull = False
ldw = 1280
ldh = 720
variabletest = 0
looping=True



if __name__ == '__main__':
    if usefull:
        gameDisplay = pygame.display.set_mode((ldw, ldh), pygame.FULLSCREEN,pygame.RESIZABLE )
        s = pygame.display.get_window_size()
        dw = s[0]
        dh = s[1]
    else:
        gameDisplay = pygame.display.set_mode((ldw, ldh),pygame.RESIZABLE)
    s = pygame.display.get_window_size()
    dw = s[0]
    dh = s[1]
    pygame.display.set_caption('Editor')
    clock = pygame.time.Clock()

screen = guis.mainWidget("grey",style={},data={},inglobals=globals())
vl = vlistWidget("VList",screen)
hl = hlistWidget("TopBar",vl,style={"W":dw,"H":32})
run = buttonWidget("Run",hl,action="""try:
    exec(tb.getText())
except Exception as e:
    print(e)
    """,style={"W":64,"H":32})
tbt = textWidget(id="Hello", parent=run,style={
"Text":"Run",
"Justification":"left top",
"Color":"black",
"Wrap":dw,
"W":64,"H":32,
"Padding":(0,0,0,0),
"Margin":(0,0,0,0),
"Round":(5,5,5,5),
"Background":"None"
})
tb = textBoxWidget("TextBox",vl,enterquits=False,style={
"Text":"Type!",
"Color":"black",
"InactiveColor":"grey",
"ActiveColor":"lgrey",
"Background":None,
"W":dw,
"H":dh,
"Wrap":dw
})
tbt = textWidget(id="Hello", parent=tb,style={
"Text":"self.parentref.getText()",
"Justification":"left top",
"W":dw,
"H":dh,
"Color":"white",
"Wrap":dw,
"Padding":(0,0,0,0),
"Margin":(0,0,0,0),
"Round":(5,5,5,5),
"Border":{
"color":"white",
"width":2,
"round":1
},
"Background":"self.parentref.dbackground"
})

def renderframe(events,display,skipevents=False,screen=None):
    #print("frame")
    global dw
    global dh
    if not skipevents:
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if(event.key==pygame.K_ESCAPE):
                    pygame.quit()
                    quit()
                screen.prossesinputs("Keydown",event,display,globals())
            if event.type == pygame.KEYUP:
                screen.prossesinputs("Keyup",event,display,globals())
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.prossesinputs("Mousedown",event,display,globals())
            if event.type == pygame.MOUSEMOTION:
                screen.prossesinputs("Mousemove",event,display,globals())
            if event.type == pygame.MOUSEBUTTONUP:
                screen.prossesinputs("Mouseup",event,display,globals())
            if event.type == pygame.FINGERDOWN:
                pass
            if event.type == pygame.FINGERUP:
                pass
            if event.type == pygame.VIDEORESIZE:
                s = pygame.display.get_window_size()
                dw = s[0]
                dh = s[1]
                display.fill((0,0,0))
                pygame.display.update()
            if  event.type == WINDOWLEAVE:
                screen.prossesinputs("Mouseleave",event,display,globals())

    #pygame.display.update()
    screen.redraw(display)

def render():
    global looping
    guis.globallink = globals()
    while looping:
        global variablestr
        global variabletest
        #Quit on clicking the "X" in the corner, or by pressing the escape + enter key.
        variabletest += .5
        clock.tick(60)
        #variablestr = str(round(variabletest))
        #variabletest+=1
        renderframe( pygame.event.get(),gameDisplay,screen=screen )
        screen.update()
        pygame.display.update()
        #pygame.time.wait(1500)
        variabletest += .5
        #print("Tick",clock.get_time())
        #print(vl.countchildren())
    pygame.quit()

render()
