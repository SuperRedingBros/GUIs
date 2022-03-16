import guis
from guis import *
import pygame

usefull = False
ldw = 1280
ldh = 960

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
    screen.redraw(display,"none")
    #pygame.display.update()

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
        print(clock.get_time())
    pygame.quit()


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
    pygame.display.set_caption('GUI Tests')

if __name__ == '__main__' and False:
    screen = guis.mainWidget(pygame,"red",style={},data={})
    hl1 = guis.wraplistWidget("Hi2",screen,style={
    "Background":"dyellow",
    "Border":{
    "color":"white",
    "width":-1,
    "round":1
    }},data={},wrapwidth=550)
    hl2 = guis.wraplistWidget("Hi2",hl1,style={
    "Background":"yellow",
    "Border":{
    "color":"blue",
    "width":5,
    "round":1
    }},data={},wrapwidth=550)
    helloworld = guis.textWidget(id="Hello", parent=hl1,style={
    "Text":"Hello World Time",
    "Justification":"left top",
    "Wrap":172,
    "Padding":(0,0,0,0),
    "Background":None,
    "Margin":(0,0,0,0),
    "Round":(5,5,5,5),
    "Border":{
    "color":"white",
    "width":1,
    "round":1
    }
    })
    helloworld.copy(newid=randid, newparent=hl1)
    helloworld.copy(newid=randid, newparent=hl1)
    helloworld.copy(newid=randid, newparent=hl1)
    helloworld.copy(newid=randid, newparent=hl1)
    helloworld.copy(newid=randid, newparent=hl1)
    helloworld.copy(newid=randid, newparent=hl1)
    helloworld.copy(newid=randid, newparent=hl1)
    helloworld.copy(newid=randid, newparent=hl2)
    helloworld.copy(newid="randid", newparent=hl2)
    helloworld.copy(newid=randid, newparent=hl2)
    helloworld.copy(newid="randid", newparent=hl2)
    #vlistWidget("Hi3","Hi2",0,0,red,grey,style={"W":"self.hfill()"})
    #surfaceWidget("HI",25,25,25,25,"main",white)
    #c.draw("Line",(255,0,0),((0,0),(25,25)),25)
    #c.draw("Arc",(255,0,0),((25,25,55,55),math.radians(25),math.radians(255)),5)
    #c.draw("Ellipse",(255,0,0),((55,55,55,55)),10)
    render()
    #imageWidget(id="Image",parent="Hi",x=0,y=0,color=white,activecolor=white,
    #text="Hi",image="assets/checkmark.png",style={"H":dh,"W":dw})
    quit()

if __name__ == '__main__' and True:
    #print(wrapline("HHHHHH hHHH HH HH HHH HH H HH H", dynamicFont, 120))
    screen = mainWidget(pygame,"purple",style={"Border":{
    "color":"red",
    "width":3,
    "round":1
    }},data={})
    vl = vlistWidget(id="Hi12", parent=screen, style={"Border":{
    "color":"green",
    "width":5,
    "round":1
    }})
    #vl.ignore=["Border"]
    hl1 = wraplistWidget("Hi2",vl,style={"Border":{
    "color":"green",
    "width":-5,
    "round":1
    }},data={},wrapwidth=150)
    hl2 = hlistWidget("Hi123",vl,style={},data={})
    #vlistWidget("Hi3","Hi2",0,0,red,grey,style={"W":"self.hfill()"})
    #surfaceWidget("HI",25,25,25,25,"main",white)
    n = noneWidget(id="None")
    popout = floatyBoxWidget(id="Popout", parent=screen, style={
    "H":16
    })
    vl7 = vlistWidget(id="Hi12", parent=popout, style={
    "Background":"grey",
    "W":512,
    "H":256
    })
    helloworld0 = textWidget(id="Hello", parent=vl7,style={
    "Text":"Hello World Time",
    "Justification":"left top",
    "W":"72",
    "H":"72",
    "Round":(5,5,5,5),
    "Border":{
    "color":"white",
    "width":-1,
    "round":1
    },
    "Gradient":{
        "base":(255,0,255),
        "end":(0,0,0),
        "types":"text",
        "inverse":False,
        "vert":True,
        "flip":False
    }
    })
    sw2 = switchWidget(id="Switch",parent=vl7,style={
    "W":32,
    "H":32,
    "Round":(16,16,16,16),
    "ActiveColor":"lred",
    "Background":"white",
    "Gradient":{
        "base":"red",
        "end":"yellow",
        "types":["background"],
        "inverse":"self.active",
        "vert":False,
        "flip":False
    }
    })
    cb2 = checkWidget(id="Check",parent=vl7,style={
    "W":64,
    "H":64
    })
    b = buttonWidget(id="Button", parent=vl7, action="popout.out = False", style={
    "W":64,
    "H":32
    })
    textWidget(id="Text", parent=b,style={
    "Text":"Ok.",
    "Color":"black",
    "Background":None,
    "W":64,
    "H":32,
    "Justification":"center middle"
    })

    emptyWidget(id="Empty", parent=vl, style={
    "W":64,
    "H":32
    }, data={})

    dr = dropdown("Test", vl, "Hello")
    dr.addoption("Hello")
    dr.addoption("Hi")
    dr.addoption("Hola")
    dr.addoption("Aloha")
    #popout.out = True
    buttonWidget(id="Button", parent=vl, action="popout.out = True", style={
    "W":64,
    "H":32
    })
    counter = textWidget(id="HelloCounter", parent=hl1,style={
    "Text":
    """text""",
    "W":"64",
    "H":"64",
    "Wrap":104,
    "Color":"white",
    "Padding":(0,0,0,0),
    "Margin":(0,0,0,0),
    "Background":(255,2,2),
    "Justification":"left top",
    "Gradient":{
        "base":(155,125,0),
        "end":(55,0,0),
        "types":"background",
        "inverse":True,
        "vert":False,
        "flip":False
    }
    },data={"Break":False,"Load":'L'})
    helloworld = textWidget(id="Hello", parent=hl1,style={
    "Text":"Hello World Time",
    "Justification":"left top",
    "W":"172",
    "H":"72",
    "Wrap":128,
    "Padding":(0,0,0,0),
    "Margin":(0,0,0,0),
    "Round":(5,5,5,5),
    "Border":{
    "color":"white",
    "width":2,
    "round":1
    },
    "Gradient":{
        "base":(255,0,255),
        "end":(0,0,0),
        "types":"text",
        "inverse":False,
        "vert":True,
        "flip":False
    }
    })
    helloworld.copy(newid=randid)
    #print(counter.hasParentOfQuery("mainWidget"))
    sl = sliderWidget(id="Slider", parent=vl, style={
    "W":32,
    "H":32,
    "Background":"grey",
    "Slider":{
        "x":0,
        "w":130,
        "h":0,
        "y":0,
        "dw":8,
        "dwo":12,
        "dh":8,
        "dho":12,
        "inc":1,
        "drawinc":5,
        "notch":",w"
    }
    })
    hlw1 = hlistWidget(id="Arc List", parent=vl, style={})
    ov = overlayWidget("Indicator", parent=hlw1, style={})
    imbs = textWidget(id="HelloTwo", parent=ov, style={
    "Text":"",
    "Color":"black",
    "W":64,
    "H":64,
    "Background":"grey",
    "Round":(32,32,32,32)
    })
    arcp = arcProgressWidget(id="Arc", parent=ov,style={
    "Text":"variablestr",
    "W":64,
    "H":64,
    "Background":None,
    "Color":"red",
    "FillValue": """sl.sliderx/sl.slidemaxx""",
    "Maxangle":360,
    "Angle":-90,
    "Flip":False,
    "Image":"self.arrowwhite"
    })
    arcc = canvasWidget("Canvas", parent=ov, style={
    "W":64,
    "H":64,
    "Background":None
    })
    arcc.draw("Arc",(255,0,0),((0,0,64,64),math.radians(0),math.radians(360)),2)
    ov.copy()
    hpr = hprogressWidget(id="Hello", parent=vl,style={
    "Text":"variablestr",
    "W":"dw",
    "H":32,
    "Background":"lgrey",
    "Color":"cornflowerblue",
    "FillValue": """sl.sliderx/sl.slidemaxx""",
    "Round":(25,25,25,25),
    "Flip":False
    })
    tb = textBoxWidget("TextBox",hl1,style={
    "Text":"Type!",
    "Color":"black",
    "InactiveColor":"grey",
    "ActiveColor":"lgrey",
    "Background":None
    })
    tbt = textWidget(id="Hello", parent=tb,style={
    "Text":"self.parentref.mytext if self.parentref.mytext != '' else self.parentref.text",
    "Justification":"left top",
    "W":"self.textboxw(64)",
    "H":"self.textboxh(32)",
    "Color":"white",
    "Wrap":128,
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
    cb = checkWidget(id="Check",parent=hl1,style={
    "W":64,
    "H":64
    })
    hl2 = hlistWidget("Hi1234",vl,style={
    "W":"dw"
    })
    hwt = textWidget(id="HelloTwo", parent=vl, style={
    "Text":"Hello World Nice To See You",
    "Justification":"left top",
    "Wrap":256
    })
    ov2 = overlayWidget("Hi1212", parent=vl, style={})
    imb = textWidget(id="HelloTwo", parent=ov2, style={
    "Text":"",
    "Color":"black",
    "W":64,
    "H":64,
    "Background":"white",
    "Round":(32,32,32,32)
    })
    i = imageWidget(id="Image", parent=ov2, style={
    "W":64,
    "H":64,
    "Image":"img_file",
    "Angle":"int(variabletest)"
    })
    hlw = hlistWidget(id="RadioList", parent=vl, style={})
    r = radioWidget(id="randid", parent=hlw, style={
    "Color":"black",
    "ActiveColor":"lyellow",
    "InActiveColor":"White",
    "W":16,
    "H":16
    })
    r.copy(newid="randid")
    r.copy(newid="randid")
    r.copy(newid="randid")
    w = canvasWidget("Canvas", parent=vl, style={
    "W":56,
    "H":56,
    "Background":"white"
    })
    sw = switchWidget(id="Switch",parent=vl,style={
    "W":32,
    "H":32,
    "Round":(16,16,16,16),
    "ActiveColor":"lred",
    "Background":"white",
    "Gradient":{
    "base":"red",
    "end":"yellow",
    "types":"background",
    "inverse":"self.active",
    "vert":False,
    "flip":False
    }
    })
    #c.draw("Line",(255,0,0),((0,0),(25,25)),25)
    #c.draw("Arc",(255,0,0),((25,25,55,55),math.radians(25),math.radians(255)),5)
    #c.draw("Ellipse",(255,0,0),((55,55,55,55)),10)
    w.draw("Polygon",(255,0,0),((25,25),(52,52),(52,25)),2)
    g = graphWidget("Graph", vl, style={
    "W":72,
    "H":72
    })
    fg = screen.find("Graph")
    fg.linepoint(1, 1)
    fg.linepoint(1, 2)
    g2 = g.copy()
    g2.linepoint(2, 2)
    drag = dragSnaplessWidget("Drag", vl, style={
    "W":64,
    "H":32
    })
    imb2 = textWidget(id="HelloTwo", parent=drag, style={
    "Text":"Hello",
    "Color":"black",
    "W":64,
    "H":32,
    "Background":"white",
    "Round":(16,16,16,16),
    "Margin":(0,0,0,0),
    "Border":{
    "color":"white",
    "width":-1,
    "round":1
    }
    })
    drop = dropWidget("Drop", vl, style={
    "W":64,
    "H":32,
    "Border":{
    "color":"white",
    "width":2,
    "round":1
    }
    })
    drop1 = dropWidget("Drop1", vl, style={
    "W":64,
    "H":32,
    "Border":{
    "color":"white",
    "width":2,
    "round":1
    }
    })
    drop2 = dropWidget("Drop2", vl, style={
    "W":64,
    "H":32,
    "Border":{
    "color":"white",
    "width":2,
    "round":1
    }
    })
    abs = absDrawWidget(id="Draw", parent=vl, style={})
    t2 = textWidget(id="Hello", parent=abs,style={
    "Text":"Hello",
    "Justification":"left top",
    "ABSX":100,
    "ABSY":100,
    "Color":"white",
    "Wrap":128,
    "Padding":(0,0,0,0),
    "Margin":(0,0,0,0),
    "Round":(5,5,5,5),
    "Border":{
    "color":"white",
    "width":5,
    "round":1
    },
    "Background":"red"
    })
    render()
    #imageWidget(id="Image",parent="Hi",x=0,y=0,color=white,activecolor=white,
    #text="Hi",image="assets/checkmark.png",style={"H":dh,"W":dw})

    quit()

if __name__ == '__main__' and False:
    htmltogui.setup(gameDisplay)

    htmltogui.openfile("./guis/testhtml/test.html")

if __name__ == '__main__' and False:

    screen = mainWidget(pygame,"blue",style={},data={})
    vl = vlistWidget("vl",screen)
    i = imageWidget(id="Image", parent=vl, style={
    "W":64,
    "H":64,
    "Image":"img_file",
    "Angle":"int(variabletest)"
    })
    i = imageWidget(id="Image", parent=vl, style={
    "W":64,
    "H":64,
    "Image":"img_file",
    "Angle":"int(variabletest)"
    })
    i = imageWidget(id="Image", parent=vl, style={
    "W":64,
    "H":64,
    "Image":"img_file",
    "Angle":"int(variabletest)"
    })
    #vlistWidget("Hi3","Hi2",0,0,red,grey,style={"W":"self.hfill()"})
    #surfaceWidget("HI",25,25,25,25,"main",white)
    #c.draw("Line",(255,0,0),((0,0),(25,25)),25)
    #c.draw("Arc",(255,0,0),((25,25,55,55),math.radians(25),math.radians(255)),5)
    #c.draw("Ellipse",(255,0,0),((55,55,55,55)),10)
    render()
    #imageWidget(id="Image",parent="Hi",x=0,y=0,color=white,activecolor=white,
    #text="Hi",image="assets/checkmark.png",style={"H":dh,"W":dw})
    quit()
