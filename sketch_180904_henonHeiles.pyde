from Saver import saves
N_PHI = 1
N_save = N_PHI

fc = 1
wd = 1920/fc; ht = 1080/fc

A = 0.25045
Af = 1.
np = 1000
hi = .25; hf = .9
zoom = PVector(2,4/.5625)
bound = PVector.mult(zoom,.1)
fadeamt = 0.0
ld = 2000
hs = .5

def settings():
    size(wd,ht)

def setup():
    global S, saver
    colorMode(HSB,1.)
    background(0)
    S = syst(np,hi,hf)
    ###
    saver = saves(N_PHI, N_save)

def draw():
    global A
    blendMode(SUBTRACT)
    noStroke()
    fill(fadeamt)
    rect(0,0,width,height)
    blendMode(BLEND)
    translate(width/2.,height/2.)
    S.update()
    # A = map(cos(TWO_PI*frameCount/10000+PI),-1,1,.05,.3)
    ### saving
    saver.save_frame()

###########
class particle():
    def __init__(self,pos,h,life,L):
        self.pos = pos
        self.h = h
        self.L = L
        self.life = life
    
    def update(self):
        if self.life <= 0:
            self.pos = PVector(random(-1,1),random(-1,1))
            self.h = map(self.pos.mag(),0,2**.5/zoom.mag(),hi,hf)
            self.life = self.L
        x = self.pos.x*cos(A*TWO_PI) - self.pos.y*sin(A*TWO_PI) + self.pos.x**2*sin(A*TWO_PI)
        y = self.pos.x*sin(A*TWO_PI) + self.pos.y*cos(A*TWO_PI) - self.pos.x**2*cos(A*TWO_PI)
        self.pos = PVector(x,y)
        self.oob()
        self.life -= 1
    
    def show(self):
        b = map(self.life,0,self.L,0,1)
        dh = map(self.life,0,self.L,hs,0)
        stroke(color(hloop(self.h+dh),1,b))
        xi = map(self.pos.x,-1,1,-zoom.x,zoom.x)*width/2
        yi = map(self.pos.y,-1,1,-zoom.y,zoom.y)*height/2
        point(xi,yi)
    
    def oob(self):
        if not(-1/bound.x <= self.pos.x <= 1/bound.x) or \
            not(-1/bound.y <= self.pos.y <= 1/bound.y):
            self.pos = PVector(random(-1,1),random(-1,1))
            self.h = map(self.pos.mag(),0,2**.5/zoom.mag(),hi,hf)

class syst():
    def __init__(self,n,hmin,hmax):
        self.n = n
        self.pts = []
        for i in xrange(n):
            pos = PVector(random(-1,1),random(-1,1))
            h = map(pos.mag(),0,2**.5,hmin,hmax)
            p = particle(pos,h,i+ld+1,n+ld)
            self.pts.append(p)
    
    def update(self):
        for i in xrange(len(self.pts)):
            self.pts[i].update()
            self.pts[i].show()

#####################
def hloop(h):
    if not(0<=h<1): return h - floor(h)
    else: return h

def keyPressed():
    global A,Af
    if key == 'f': print frameCount
    if key == 's': saver.onClick()
    if key == 'a': print A
    if key == 'o': A += Af; print "A: ",A
    if key == 'l': A -= Af; print "A: ",A
    if key == 'i': Af *= 10; print "Af: ",Af
    if key == 'k': Af /= 10; print "Af: ",Af
