import pygame

from pygame import (draw, image)
import math
from kinematic_2arm_bone import kinematic_solution


class ErrorToRedscale:
    def __init__(self, colors, scale):
        self.colors = colors
        sqscale = scale * scale
        # if we have 20 colours
        # and 400 scale (400 sq)
        # then we want 1 colour change for every 20 out.
        # and max out at the last one
        self.per_division = sqscale / len(colors)
        print("Per division is %s" % self.per_division)

    def get_color(self, intended, actual):
        distx = intended[0] - actual[0]
        distx2 = distx * distx
        disty = intended[1] - actual[1]
        disty2 = disty * disty
        sqdist = distx2 + disty2
        index = int(sqdist / self.per_division)
        if index != 0:
            print("%s != %s : %s" % (intended, actual, index))
        index = min(index, len(self.colors) - 1)
        return self.colors[index]



def main():
    pygame.init()

    white =  255, 255, 255
    black =  0, 0, 0
    red =    255, 0, 0
    green =  0, 255, 0
    blue =   0, 0, 255

    redscale = [[n, 255 - n, 0] for n in range(0, 254, 10)]
    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)
    screen.fill(white)

    rod_length = width / 4

    rs = ErrorToRedscale(redscale, width)
    hw = width / 2
    hh = height / 2
    for x in range(0, width - 1):
        for y in range(0, height - 1):
            # try:
                relx = x - hw
                rely = y - hh
                try:
                    a1, a2 = kinematic_solution(rod_length, rod_length, (relx, rely))
                except AssertionError:
                    draw.line(screen, red, (x, y), (x+1, y))
                    continue
                else:
                    actual = (math.cos(a1) * rod_length + math.cos(a1 + a2) * rod_length,
                              math.sin(a1) * rod_length + math.sin(a1 + a2) * rod_length)
                    rounded = (round(actual[0]), round(actual[1]))
                    assert rounded == (relx, rely), "%s not equal %s. A1 is %f, A2 is %f" % (repr(actual),
                                                                                            repr((relx, rely)), a1, a2)
                    draw.line(screen, rs.get_color((relx, rely), actual), (x, y), (x+1, y))
            # except AssertionError:
            #     draw.line(screen, red, (x, y), (x+1, y))
        pygame.display.update()
    image.save(screen, "test_output.png")

if __name__ == "__main__":
    main()