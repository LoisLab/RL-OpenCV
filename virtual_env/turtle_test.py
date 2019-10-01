from turtle import *

'''
standard turtle graphics test code from Python docs
'''

setup(width=820,height=820,startx=None,starty=None)
screensize(800,800)
color('red', 'yellow')
begin_fill()
goto(0,0)
while True:
    forward(200)
    left(170)
    if abs(pos()) < 1:
        break
end_fill()
done()
