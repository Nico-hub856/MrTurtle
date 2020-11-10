import pygame as pg
import sys, time
from os import path
vec = pg.math.Vector2

game_folder = path.dirname(__file__)

WIDTH = 0
HEIGHT = 0

penup = False
pendown = True

close = False

up = "up"
down = "down"
right = "right"
left = "left"

positions = []
sizes = []
colors = []

x_pos = 0
y_pos = 0

x_size = 0
y_size = 0

t_color = 0

screen_color = 0

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

red = (255, 0, 0)
blue = (0, 0, 255)
cyan = (150, 150, 255)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)

pen_size = 1
pen_color = red

s = pg.display.set_mode((100,100))

turtle_img = pg.image.load(path.join(game_folder, "turtle.png"))

font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def init():
    global clock
    pg.init()
    pg.mixer.init()
    clock = pg.time.Clock()
    
def screen(width=1366, height=768, fullscreen=False, caption="screen", color=white):
    global s, WIDTH, HEIGHT, cam
    global turtles, t, screen_color
    init()
    if fullscreen == True:
        s = pg.display.set_mode((width,height), pg.FULLSCREEN)
    else:
        s = pg.display.set_mode((width,height))
    pg.display.set_caption(caption)
    HEIGHT = height
    WIDTH = width
    cam = Camera()
    
    screen_color = color
    
    turtles = pg.sprite.Group() 
    t = T(WIDTH/2, HEIGHT/2)
    turtles.add(t)
    
    update()
                
def update():
    global s, t, pendown, w, h, pen_size, pen_color, positions, sizes, colors, cam, close, screen_color
    if close == False:
        t.pos -= t.vel
    t.rect.centerx = int((t.pos[0] + cam.cam_x) * cam.cam_z)
    t.rect.centery = int((t.pos[1] + cam.cam_y) * cam.cam_z)
    #t.image = pg.transform.scale(t.image_orig, (int(t.size * 1.2 * cam.cam_z), int(t.size * cam.cam_z))) 
    if close == False:
        if pendown == True:
            positions.append([t.pos[0], t.pos[1]])
            sizes.append(pen_size)
            colors.append(pen_color)
    cam.update()
    turtles.update()
    s.fill(screen_color)
    draw_lines()
    if cam.hide == False:
        turtles.draw(s)
    #draw_point()
    if close == False:
        draw_text(s, "Work in progress...", 18, WIDTH - 80, 0)
    elif close == True:
        draw_text(s, "Done!", 18, WIDTH - 30, 0)
    pg.display.flip()
    events()

def draw_lines():
    global positions, sizes, colors, cam
    for i in range(len(positions)-1):
        pg.draw.line(s, colors[i], (int((positions[i][0] + cam.cam_x) * cam.cam_z), int((positions[i][1] + cam.cam_y) * cam.cam_z)), (int((positions[i+1][0] + cam.cam_x) * cam.cam_z), int((positions[i+1][1] + cam.cam_y) * cam.cam_z)), sizes[i])

class T(pg.sprite.Sprite):
    def __init__(self, x, y, s=40, color=YELLOW):
        global turtle_img, WIDTH, HEIGHT, cam
        pg.sprite.Sprite.__init__(self)
        self.image_orig = pg.transform.scale(turtle_img, (int(s * 1.2), s)) 
        self.image = self.image_orig
        #self.image = pg.transform.rotate(self.image_orig, 180)
        self.rect = self.image.get_rect()
        self.width = int(s*1.2)
        self.height = s
        self.rect.centerx = x
        self.rect.centery = y
        self.size = s
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        
    def rotation(self,surf):
        w, h = self.image.get_size()
        originPos = [w//2,h//2]
        #originPos[0] = w//2
        #originPos[1] = h//2
        pos = self.pos
        
        angle = self.rot
        
        w, h       = self.image.get_size()
        box        = [pg.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

        # calculate the translation of the pivot 
        pivot        = pg.math.Vector2(originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move   = pivot_rotate - pivot

        origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

        self.image = pg.transform.rotate(self.image_orig, angle)
        new_rect = self.image.get_rect()
        new_rect[0] = origin[0]
        new_rect[1] = origin[1]

        self.rect = new_rect
        
def done():
    global pendown, penup, close
    pendown = False
    penup = True
    close = True
    while close:
        update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    
def events():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()

class Turtle():
    def wait(self, secs):
        time.sleep(secs)
        update()

    def pen_up(self):
        global penup, pendown
        pendown = False
        penup = True
        update()
        
    def pen_down(self):
        global penup, pendown
        penup = False
        pendown = True
        update()
        
    def go_to(self,x,y):
        global t
        t.pos[0] = x
        t.pos[1] = y
        update()
        
    def color(self,color):
        global pen_color
        pen_color = color
        update()

    def size(self,size):
        global pen_size
        pen_size = size
        update()
        
    def move(self,steps):
        global t
        t.vel = vec(steps, 0).rotate(-t.rot)
        update()
        
    def forward(self,steps):
        global t
        t.vel = vec(steps, 0).rotate(-t.rot)
        update()
        
    def backward(self,steps):
        global t
        t.vel = vec(-steps, 0).rotate(-t.rot)
        update()
        
    def left(self, degree):
        global t, s
        if degree > 0:
            t.rot += int(-degree)
        t.rotation(s)
        update()
    def right(self, degree):
        global t, s
        if degree > 0:
            t.rot += int(degree)
        t.rotation(s)
        update()
    def rotate(self,degree):
        global t, turtle_img
        if degree == "right":
            t.rot = 180
        elif degree == "left":
            t.rot = 0
        elif degree == "up":
            t.rot = -90
        elif degree == "down":
            t.rot = 90
        else:
            t.rot += int(degree)
        t.rotation(s)
        update()
        
    def clear(self):
        global sizes, colors, positions
        sizes = []
        colors = []
        positions = []
        update()

class Camera():
    def __init__(self):
        self.cam_x = 0
        self.cam_y = 0
        self.cam_z = 1
        self.hide = False
        self.last_press = 0
        
    def update(self):
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.cam_x += 4 / self.cam_z
        if keystate[pg.K_RIGHT]:
            self.cam_x -= 4 / self.cam_z
        if keystate[pg.K_UP]:
            self.cam_y += 4 / self.cam_z
        if keystate[pg.K_DOWN]:
            self.cam_y -= 4 / self.cam_z       
        if keystate[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_press > 250:
                self.last_press = now
                self.hide = not self.hide
        if keystate[pg.K_F1]:
            self.cam_z *= 1.01
            #self.cam_x = 0
            #self.cam_y = 0
        if keystate[pg.K_F2]:
            self.cam_z *= 0.99
