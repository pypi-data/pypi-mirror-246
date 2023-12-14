#!/usr/bin/env python3
r"""
使用turtle模块的太阳系模拟程序，
改编自Python安装目录自带的Lib\turtledemo\planet_and_moon.py
提示：若程序变卡慢，单击屏幕可清屏。
"""
from time import perf_counter
from random import randrange
from turtle import Shape, Turtle, update, Screen, Terminator, Vec2D as Vec, mainloop

__author__="七分诚意 qq:3076711200"
__email__="3076711200@qq.com"
__version__="1.3.1"

G = 8

scr=None

class GravSys:
    # 引力系统
    __slots__=['planets', 'removed_planets', 't', 'dt', 'frameskip',
               'scale', 'scr_x', 'scr_y',
               'show_fps','__last_time','writer','fps','following']
    def __init__(self):
        self.planets = []
        self.removed_planets=[]
        self.t = 0
        self.dt = 0.002 # 速度
        #frameskip: 程序在绘制一帧之前跳过的帧数
        self.frameskip=50
    def init(self):
        for p in self.planets:
            p.init()
    def start(self):
        while True:
            self.__last_time=perf_counter()
            # 计算行星的位置
            for i in range(self.frameskip):
                self.t += self.dt
                for p in self.planets:
                    p.step()

            for p in self.planets:
                p.update()
            update()
    def fast(self,event):
        self.dt*=1.1
    def slow(self,event):
        self.dt/=1.1

class Star(Turtle):
    def __init__(self, gravSys, m, x, v,
                 shape,shapesize=1,orbit_color=None):
        Turtle.__init__(self)
        self.shape(shape)
        self.size=shapesize
        self.shapesize(shapesize)
        if orbit_color is not None:
            self.pencolor(orbit_color)
        self.m = m
        self.penup()
        self.setpos(x)
        self.pendown()
        self.v = v
        gravSys.planets.append(self)
        self.gravSys = gravSys
    def init(self):
        dt = self.gravSys.dt
        self.a = self.acc()
        self.v = self.v + 0.5*dt*self.a
    def acc(self): # 利用引力公式计算加速度
        a = Vec(0,0)
        for planet in self.gravSys.planets:
            if planet is not self:
                v = planet._position-self._position
                a += (G*planet.m/abs(v)**3)*v
        return a
    def step(self): # 利用加速度计算速度和位移
        dt = self.gravSys.dt
        #self._position += dt*self.v
        self.setpos(self._position + dt*self.v) # _position直接为该turtle位置

        self.a = self.acc()
        self.v = self.v + dt*self.a
    def update(self):
        sun = self.gravSys.planets[0]
        if self != sun:
            self.setheading(self.towards(sun))

class Sun(Star):
    # 太阳不移动, 固定在引力系统的中心
    def step(self):
        pass

def main():
    global scr
    scr=Screen()
    scr.screensize(10000,10000)
    try:
        scr._canvas.master.state("zoomed")
    except:pass
    scr.bgcolor("#000030")
    scr.tracer(0,0)

    # create compound turtleshape for planets
    s = Turtle()
    s.reset()
    s.ht()
    s.pu()
    s.fd(8)
    s.lt(90)
    s.begin_poly()
    s.circle(8, 180)
    s.end_poly()
    _light = s.get_poly()
    s.begin_poly()
    s.circle(8, 180)
    s.end_poly()
    _dark = s.get_poly()
    s.begin_poly()
    s.circle(8)
    s.end_poly()
    _circle = s.get_poly()
    update()
    s.hideturtle()
    def create_shape(screen,name,light,dark=None):
        shape = Shape("compound")
        if dark is not None:
            shape.addcomponent(_light,light)
            shape.addcomponent(_dark,dark)
        else:
            shape.addcomponent(_circle,light)
        screen.register_shape(name, shape)


    create_shape(scr,"mercury","gray70","grey50")
    create_shape(scr,"venus","gold","brown")
    create_shape(scr,"earth","blue","blue4")
    create_shape(scr,"moon","gray70","grey30")
    create_shape(scr,"mars","red","red4")

    # setup gravitational system
    gs = GravSys()
    sun = Sun(gs,1e6, Vec(0,0), Vec(0,0),
              "circle",1.8)
    sun.color("yellow")
    sun.penup()

    # 水星
    mercury = Star(gs,100, Vec(48,0), Vec(0,420),
                   "mercury",0.5, "gray")
    # 金星
    venus = Star(gs,5000, Vec(-120,0), Vec(0,-260),
                 "venus",0.7, "gold4")
    # 地球
    earth = Star(gs,4000, Vec(210,0), Vec(0,195),
                 "earth",0.8, "blue")
    # 月球
    moon = Star(gs,30, Vec(216,0), Vec(0,260),
                "moon",0.5)
    # 火星及卫星
    mars = Star(gs,2000, Vec(0,330), Vec(-160, 0),
                "mars",0.6, "red")
    # 水星
    #mercury = Star(gs,300, Vec(65,0), Vec(0,320),
    #               "mercury",0.5, "gray")
    # 金星
    #venus = Star(gs,3600, Vec(140,0), Vec(0,240),
    #             "venus",0.7, "gold4")
    # 地球
    #earth = Star(gs,4000, Vec(-210,0), Vec(0,-195),
    #             "earth",0.8, "blue")
    # 月球
    #moon = Star(gs,30, Vec(-216,0), Vec(0,-260),
    #            "moon",0.5)
    # 火星及卫星
    #mars = Star(gs,1000, Vec(0,-430), Vec(140, 0),
     #           "mars",0.6, "red")
    # 绑定键盘事件
    cv=scr.getcanvas()
    cv.bind_all("<Key-equal>",gs.fast)
    cv.bind_all("<Key-minus>",gs.slow)
    #scr.tracer(1,0)
    def clear_scr(x=None,y=None):
        for planet in gs.planets:
            planet.clear()

    scr.onclick(clear_scr)
    gs.following=earth
    gs.init()
    gs.start()

if __name__ == '__main__':
    main()
    mainloop()
