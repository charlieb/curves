from functools import reduce
from math import pi, sin, cos, sqrt
from random import random
import svgwrite as svg

X,Y = 0,1

class Turtle:
    def __init__(self):
        self.angle = 0  # starting angle
        self._angle = self.angle # used in drawing
        self.pos = [0,0]
        self.turn_angle=pi/2
        self.step_length=10 # starting length
        self._step_length=self.step_length # used in drawing
        self.step_scaler = sqrt(2)
        self.lines = []
    def forward(self):
        prev_pos = self.pos.copy()
        self.pos[X] += self._step_length * cos(self._angle)
        self.pos[Y] += self._step_length * sin(self._angle)
        self.lines.append([prev_pos, self.pos.copy()])
    def turn_pos(self):
        self._angle += self.turn_angle
    def turn_neg(self):
        self._angle -= self.turn_angle
    def mul_step(self):
        self._step_length *= self.step_scaler
    def div_step(self):
        self._step_length /= self.step_scaler
    def draw(self, commands, string, start = [0,0]):
        self.pos = start
        self.lines = []
        self._angle = self.angle
        self._step_length=self.step_length
        for sym in string:
            if sym in commands:
                commands[sym](self)
        return self.lines
    def extent(self):
        minx, miny = 99999, 99999
        maxx, maxy = -99999, -99999
        for line in self.lines:
            for x,y in line:
                if maxx < x: maxx = x
                if minx > x: minx = x
                if maxy < y: maxy = y
                if miny > y: miny = y
        return maxx-minx, maxy-miny
    def single_line(self):
        if self.lines == []: return []
        return [self.lines[0][0]] + [line[1] for line in self.lines]


default_commands = {
        'F': Turtle.forward,
        '+': Turtle.turn_pos,
        '-': Turtle.turn_neg,
        '*': Turtle.mul_step,
        '/': Turtle.div_step,
        }
examples = {
        'dragon' : {
            'axiom': 'FX',
            'rules': {
                'X': 'X+YF',
                'Y': 'FX-Y',
                },
            'commands' : default_commands,
            },
        'hilbert' : {
            'axiom': 'X',
            'rules': {
                'X': '+YF-XFX-FY+',
                'Y': '-XF+YFY+FX-',
                #'X': '+Y/F-X/FX-/FY+',
                #'Y': '-X/F+Y/FY+/FX-',
                },
            'commands' : default_commands,
            },
        }

def write_lines(lines, filename, color='black', opacity=1.0, width=1.0):
    dwg = svg.Drawing(filename)
    minx, miny = 99999, 99999
    maxx, maxy = -99999, -99999
    for line in lines:
        for x,y in line:
            if maxx < x: maxx = x
            if minx > x: minx = x
            if maxy < y: maxy = y
            if miny > y: miny = y

        svgline = svg.shapes.Line(*line)
        svgline.fill('none')
        svgline.stroke(color, width=width)
        dwg.add(svgline)
    print(minx, miny, maxx, maxy)

    dwg.viewbox(minx=minx, miny=miny, width=maxx-minx, height=maxy-miny)
    dwg.save()

def write_iterations(iterations, commands, filename, scale=0.5):
    t = Turtle()
    t.step_scaler = scale
    width = 1.
    color = 'black'

    dwg = svg.Drawing(filename)
    minx, miny = 99999, 99999
    maxx, maxy = -99999, -99999
    for i, syms in enumerate(iterations):
        t.draw(commands, syms, start = [t.step_length*scale**(i+1), t.step_length*scale**(i+1)])
        
        line = t.single_line()

        for x,y in line:
            if maxx < x: maxx = x
            if minx > x: minx = x
            if maxy < y: maxy = y
            if miny > y: miny = y

        svgline = svg.shapes.Polyline(line)
        svgline.fill('none')
        svgline.stroke(color, width=width)
        dwg.add(svgline)

        width *= scale

    print(minx, miny, maxx, maxy)

    dwg.viewbox(minx=minx, miny=miny, width=maxx-minx, height=maxy-miny)
    dwg.save()


def expand(rules, string):
    return reduce(lambda acc, sym: acc + (rules[sym] if sym in rules else sym), string, '')

def main():
    curve = 'hilbert'
    t = Turtle()
    t.step_scaler = float(1/2)
    iterations = []
    iterations.append(expand(examples[curve]['rules'], examples[curve]['axiom']))
    for _ in range(7):
        iterations.append('*' + expand(examples[curve]['rules'], iterations[-1]))

    lines = t.draw(examples[curve]['commands'], iterations[-1])
    write_lines(lines, 'test.svg')

    write_iterations(iterations, examples[curve]['commands'], 'test.svg', scale=0.5)

if __name__ == '__main__':
    main()
