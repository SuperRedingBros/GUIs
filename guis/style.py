import pathlib
path = pathlib.Path(__file__).parent.resolve()

class styleObj():
    def getW(self):
        return self.w

    def getH(self):
        return self.h

    def getZ(self):
        return self.z

    def initialvalues(self):
        self.h =0
        self.w =0
        self.z = 0
        self.wrapedhight = 0
        self.wrapedwidth = 0
        self.radiovalue = ""
        self.notifys = []
        self.popouts = []
        self.rx = 0
        self.ry = 0
        self.fillvalue = 0
        self.ovy = "visible"
        self.ovx = "visible"
        self.x = 0
        self.out = False
        self.children = []
        self.child = ""
        self.sibling = ""
        self.skip = []
        self.type = str(type(self).__name__ )
        #print(self.type)
        self.frame = False
        self.ispressing = False
        self.mouseover = False
        self.active = False
        self.changed = True
        self.limg = None
        self.dbackground = (0,0,0)
        self.wrap = -1
        self.image = "./assets/pythonicon.png"
        self.imgr = (0,0,0,0)
        self.absx = 0
        self.absy = 0
        self.lastgradient = "Blahb"
        self.display="vlist"
        self.border = {
        "color":"white",
        "width":-1,
        "round":0
        }
        self.round = (-1,-1,-1,-1)
        self.padding = (0,0,0,0)
        self.margin = (0,0,0,0)
        self.color = (255,255,255)
        self.activecolor = (255,255,255)
        self.inactivecolor = (255,255,255)
        self.background = None
        self.text = ""
        self.justification = ""
        self.angle = 0
        fontpath = str(pathlib.PurePath(path,"assets/Xolonium-Bold.ttf"))
        self.font = {"File":fontpath,"Scale":20,
        "Italics":False,
        "Underline":False}
        self.lastfont = {}
        self.flip = False
        self.gradient = {
        "base":(0,0,0),
        "end":(0,0,0),
        "types":"",
        "inverse":False,
        "vert":True,
        "flip":False
        }
        self.useboxmodel = True
        #print(parent)

    def __init__(self):
        self.initialvalues()
