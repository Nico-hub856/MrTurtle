from turtle import *

screen(400, 400)

t = Turtle()

for i in range(40):
    t.rotate(10)
    t.backward(10)
    t.wait(0.1)

done()