
import re
import json

"""

Selectors:
 element =5
 #ID =15
 .class=10
 * Universel=0

Combinators
  (space) child of
  > child selector (>)
  + adjacent sibling selector (+)
  ~ general sibling selector (~)

with attr
element[attr]

with attr and value
element[attr=value]

selector:pseudo-class

selector::pseudo-element


Example:


"blahblah   +   blah"
to
["blahblah","+","blah"]

and

"blahblah+blah"
to
["blahblah","+","blah"]

and

"  blah   blah  "
to
["blah"," ","blah"]

textWidget {
    Background: red;
}

textWidget + textWidget {
    Background: limegreen;
}

vlistWidget,textWidget {
    Color: blue;
}

.class ~ textWidget {
    Color: lightblue;
}

radioWidget {
    Background: lgrey;
}

radioWidget:hover {
    Background: grey;
}

radioWidget:active {
    Background: yellow;
}

p::first-line {
    color: yellow;
}

div > p {
    padding: 32px;
}

p + p  p{
    color: green;
}

#img + p {
    color: limegreen;
}

"""

css = """
    * {
        color: red;
    }

    p {
        color: limegreen;
    }

    p #hello,p #hellothere {
        color: blue;
    }

    p #id {
        color: lightblue;
    }

    button:active {
        color: yellow;
    }

    p:first-line {
        color: yellow;
    }

    div > {
        padding: 32px;
    }

    p + p {
        color: green;
    }

    #img + p {
        color: limegreen;
    }

    @media screen and (min-width: 480px) {
        @media (min-height: 480px) {
            p {
                p:p;
            }
            ps {
                pss:psp;
            }
        }
    }

    ps {
        pss:psp;
    }

    """

selectors = ("#",".","*",":","::")

combinators = (" ",">","+","~")

def tokenize(totoken):
    totoken = totoken.strip()
    #print(totoken)
    a = re.split("[\s>\+~]+",totoken)
    b = re.findall("[\s > \+ ~]+",totoken)
    b.append("start")
    l = []
    v = 0
    for i in a:
        l.append(i)
        l.append(b[v])
        #print(l)
        v+=1
    l.reverse()
    return l

#print(tokenize("p + p "))

def mediaQuery(query):
    s = query
    s = s.lower()
    s = s.replace("@media","",1)
    s = s.replace("not","##not")
    s = s.replace("and","##")
    s = s.split("##")
    good = True
    for q in s:
        q = q.strip()
        #print(q)
        if q == "screen" or q == "all":
            continue
        elif "(" in q :
            good=False
            break
        else:
            good=False
            break
    return good

mediaQuery("@media only screen (min-height: 480px)")

def csstodict(css):
    #print(css)
    dict = {}
    tokens = css.split(";")
    tokens.pop(-1)
    #print(tokens)
    for t in tokens:
        d = t.split(":")
        v = d[1]
        if type(v) == str:
            v = v.strip()
        k = d[0]
        if type(k) == str:
            k = k.strip()
        dict[k] = v
    #print(dict)
    return dict

class cssparser(object):

    def get(self,widget):
        #print(self.data)
        out = {}
        data = []
        index = 0
        elementtype = ""
        lwidget=widget
        for d in self.data:
            #print(d)
            good = True
            for it in d.split("###"):
                it = it.strip()
                if it[0]!="@":
                    for sd in it.split(","):
                        data.append([])
                        ld = sd
                        for c in combinators:
                            ld = it.replace(c,"{}"+c)
                        vs = ld.split("{}")
                        vs = tokenize(sd)
                        #print(vs)

                        for i in range(int(len(vs)/2)):
                            #print(x)
                            #print(d)
                            con=vs[i*2]
                            con=con.strip()
                            value=vs[(i*2)+1]
                            #print(con+" , "+value)
                            if con =="start":
                                    k=value
                                    prio = 0
                                    for c in selectors:
                                        k = k.replace(c,"{}"+c)
                                    k = k.split("{}")
                                    for v in k:
                                        #print(v)
                                        b,p = lwidget.matchesQuery(v)
                                        if not b:
                                            good=False
                                        else:
                                            prio+=p
                            elif con =="":
                                    k=value
                                    prio = 0
                                    for c in selectors:
                                        k = k.replace(c,"{}"+c)
                                    k = k.split("{}")
                                    for v in k:
                                        #print(v)
                                        r = lwidget.hasParentOfQuery(v)
                                        if type(r)==tuple:
                                            b,p = r
                                        if not b:
                                            good=False
                                        else:
                                            prio+=p
                            elif con =="+":
                                    k=value
                                    prio = 0
                                    cwidget = lwidget
                                    lwidget = lwidget.lastSibling()
                                    if lwidget!=None:
                                        for c in selectors:
                                            k = k.replace(c,"{}"+c)
                                        k = k.split("{}")
                                        for v in k:
                                            #print(v)
                                            b,p = lwidget.matchesQuery(v)
                                            if not b:
                                                good=False
                                            else:
                                                prio+=p
                                    else:
                                        good = False
                                    lwidget = cwidget
                            elif con =="~":
                                    k=value
                                    #print(k)
                                    prio = 0
                                    cwidget = lwidget
                                    loop=True
                                    for c in selectors:
                                        k = k.replace(c,"{}"+c)
                                    k = k.split("{}")
                                    while loop:
                                        lwidget = lwidget.lastSibling()
                                        if lwidget!=None:
                                            for v in k:
                                                #print(v)
                                                b,p = lwidget.matchesQuery(v)
                                                if b:
                                                    prio+=p
                                                    #print("L")
                                                    loop = False
                                        else:
                                            good = False
                                            #print("Loop")
                                            loop = False
                                    lwidget = cwidget
                            elif con ==">":
                                    k=value
                                    prio = 0
                                    cwidget = lwidget
                                    lwidget = lwidget.parentref
                                    if lwidget!=None:
                                        for c in selectors:
                                            k = k.replace(c,"{}"+c)
                                        k = k.split("{}")
                                        for v in k:
                                            #print(v)
                                            b,p = lwidget.matchesQuery(v)
                                            if not b:
                                                good=False
                                            else:
                                                prio+=p
                                    else:
                                        good = False
                                    lwidget = cwidget
                            else:
                                #print(con)
                                good = False
                        if good:
                            continue
                        else:
                            break
                else:
                    if mediaQuery(it):
                        pass
                    else:
                        good=False
                        break
            if good:
                data[index].append(prio)
                data[index].append(self.data[d])

            index+=1
        #print(data)
        return data

    def oldparse(self):
        text = self.css
        text = text.replace("}", "{")
        text = text.split("{")
        textlen = int(len(text)/2)
        textlen = range(textlen)
        count = 0
        list = {}
        for x in textlen:
            sels = text[(x*2)]
            sels = sels.strip()
            #sels = sels.split(" ")
            data = text[(x*2)+1]
            data = csstodict(data)
            for l in sels.split(','):
                list.update({l:data})

        self.data = list
        #print(list)
        return list

    def parse(self):
        text = self.css
        textlen = int(len(text)/2)
        textlen = range(textlen)
        count = 0
        list = {}
        stack = []
        looping=True
        while looping:
            f = re.search("[\{\}]",text)
            if f != None:
                #print(f)
                s = f.span()
                ltext = text[:s[0]].strip()#+text[s[1]:]
                if f.group()=="{":
                    stack.append(ltext)
                else:
                    if ltext:
                        list[" ### ".join(stack)]=csstodict(ltext)
                    stack.pop(-1)
                text = text[s[1]:]
                #data = csstodict(data)
                #for l in sels.split(','):
                #    list.update({l:data})
                #print(ltext)
                #print(f.group())
                #looping=False
            else:
                looping=False
        self.data = list
        #print(json.dumps(list,indent=3))
        return list

    def feed(self,text):
        text = text.replace("\n", "")
        self.css += text

    def __init__(self):
        self.css = ""
        self.data={}

parser = cssparser()
parser.feed(css)
parser.parse()
