import pygame
import math
import sys
from xml.dom import minidom
from numpy import array as a


class Trace:
    def __init__(self):
        self.segments = []
        self.colors = []

    def GetCoordinates(self, svg_file):
        self.segments = []
        self.segments.append((0, 0))
        doc = minidom.parse(svg_file)
        paths = doc.getElementsByTagName('path')
        for path in paths:
            d = path.getAttribute('d')
            segments = d.split(' ')
            mod = "M"
            for segment in segments:
                if (segment in ("L", "l", "H", "h", "V", "v", "M", "m")):
                    mod = segment
                    continue
                if mod in ("L", "M"):
                    coordinates = segment.split(',')
                    x1, y1 = float(coordinates[0]), float(coordinates[1])
                    self.segments.append((x1, y1))
                elif mod in ("l", "m"):
                    d_coordinates = segment.split(',')
                    x1, y1 = self.segments.pop()
                    self.segments.append((x1, y1))
                    x1 += float(d_coordinates[0])
                    y1 += float(d_coordinates[1])
                    self.segments.append((x1, y1))
                elif mod == "H":
                    x1, y1 = self.segments.pop()
                    self.segments.append((x1, y1))
                    x1 = float(segment)
                    self.segments.append((x1, y1))
                elif mod == "h":
                    x1, y1 = self.segments.pop()
                    self.segments.append((x1, y1))
                    x1 += float(segment)
                    self.segments.append((x1, y1))
                elif mod == "V":
                    x1, y1 = self.segments.pop()
                    self.segments.append((x1, y1))
                    y1 = float(segment)
                    self.segments.append((x1, y1))
                elif mod == "v":
                    x1, y1 = self.segments.pop()
                    self.segments.append((x1, y1))
                    y1 += float(segment)
                    self.segments.append((x1, y1))
        self.segments.remove((0, 0))

    def PaintPath(self):
        self.colors = []
        self.colors.append((0, 128, 0))
        for i in range(1, len(self.segments) - 1):
            x1, y1 = self.segments[i - 1]
            x2, y2 = self.segments[i]
            x3, y3 = self.segments[i + 1]
            l1 = x2 - x1
            l2 = x3 - x2
            m1 = y2 - y1
            m2 = y3 - y2
            fi = math.acos((l1 * l2 + m1 * m2) / ((l1 ** 2 + m1 ** 2) * (l2 ** 2 + m2 ** 2)) ** 0.5)
            if fi < 0.61:
                self.colors.append((0, 128, 0))
            elif fi < 1.23:
                self.colors.append((255, 255, 0))
            elif fi < 1.86:
                self.colors.append((255, 0, 0))
            elif fi < 2.49:
                self.colors.append((125, 0, 128))
            else:
                self.colors.append((0, 0, 0))


class Frame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))

    def Create(self):
        self.screen.fill((255, 255, 255))

    def Draw(self, trace):
        coordinates = a(trace.segments)
        x_koef = self.width / max(coordinates[:,0])
        y_koef = self.height / max(coordinates[:,1])
        for i in range(len(trace.segments) - 1):
            x1, y1 = trace.segments[i]
            x2, y2 = trace.segments[i+1]
            color = trace.colors[i]
            pygame.draw.line(self.screen, color, (int(x1*x_koef), int(y1*y_koef)), (int(x2*x_koef), int(y2*y_koef)), 3)

        pygame.display.update()

    def Clear(self):
        self.screen.fill((255, 255, 255))
        pygame.display.update()


frame = Frame(800, 600)
frame.Create()
traces = []
while True:
    traces.append(Trace())
    traces[0].GetCoordinates('curve.svg')
    traces[0].PaintPath()

    frame.Draw(traces[0])
    traces.clear()
    pygame.time.delay(500)
    frame.Clear()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()