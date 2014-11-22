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


def setup_colors():
    white = 255, 255, 255
    black = 0, 0, 0
    red = 255, 0, 0
    green = 0, 255, 0
    blue = 0, 0, 255
    return red, white


def plot_basic_kinematic(hw, hh, red, rod_length, rs, x, y):
    relx = x - hw
    rely = y - hh
    try:
        a1, a2 = kinematic_solution(rod_length, rod_length, (relx, rely))
    except AssertionError:
        color = red
    else:
        actual = (math.cos(a1) * rod_length + math.cos(a1 + a2) * rod_length,
                  math.sin(a1) * rod_length + math.sin(a1 + a2) * rod_length)
        rounded = (round(actual[0]), round(actual[1]))
        assert rounded == (relx, rely), "%s not equal %s. A1 is %f, A2 is %f" % (repr(actual),
                                                                                 repr((relx, rely)), a1, a2)
        color = rs.get_color((relx, rely), actual)
    return color


class PlotBasicKinematic:
    def __init__(self, rod_length, hw, hh, color_scale, fail_color):
        self.rod_length = rod_length
        self.hh = hh
        self.hw = hw
        self.color_scale = color_scale
        self.fail_color = fail_color
        self.step_distance = math.radians(1.8)

    def get_position(self, x, y):
        #get the info from the kine simulation
        relx = x - self.hw
        rely = y - self.hh
        try:
            a1, a2 = kinematic_solution(self.rod_length, self.rod_length, (relx, rely))
        except AssertionError:
            color = self.fail_color
        else:
            actual = (math.cos(a1) * self.rod_length + math.cos(a1 + a2) * self.rod_length,
                      math.sin(a1) * self.rod_length + math.sin(a1 + a2) * self.rod_length)
            rounded = (round(actual[0]), round(actual[1]))
            assert rounded == (relx, rely), "%s not equal %s. A1 is %f, A2 is %f" % (repr(actual),
                                                                                     repr((relx, rely)), a1, a2)
            color = self.color_scale((relx, rely), actual)

        return color


class PlotWithStepperResolution(PlotBasicKinematic):
    def round_to_step(self, angle_rads):
        mult = round(angle_rads / self.step_distance)
        return mult * self.step_distance

    def get_position(self, x, y):
        #get the info from the kine simulation
        relx = x - self.hw
        rely = y - self.hh
        try:
            a1, a2 = kinematic_solution(self.rod_length, self.rod_length, (relx, rely))
        except AssertionError:
            color = self.fail_color
        else:
            # Do conversion here
            # round a1 and a2 to the nearest step distance
            a1 = self.round_to_step(a1)
            a2 = self.round_to_step(a2)

            actual = (math.cos(a1) * self.rod_length + math.cos(a1 + a2) * self.rod_length,
                      math.sin(a1) * self.rod_length + math.sin(a1 + a2) * self.rod_length)
            rounded = (round(actual[0]), round(actual[1]))
            color = self.color_scale((relx, rely), actual)

        return color


def main():
    pygame.init()

    red, white = setup_colors()

    redscale = [[n, 255 - n, 0] for n in range(0, 254, 10)]
    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)
    screen.fill(white)

    rod_length = width / 4

    rs = ErrorToRedscale(redscale, 20)
    hw = width / 2
    hh = height / 2

    # plot = PlotBasicKinematic(rod_length, hw, hh, rs.get_color, red)
    plot = PlotWithStepperResolution(rod_length, hw, hh, rs.get_color, red)

    for x in range(0, width - 1):
        for y in range(0, height - 1):
            color = plot.get_position(x, y)
            draw.line(screen, color, (x, y), (x+1, y))
        pygame.display.update()
    image.save(screen, "test_output.png")

if __name__ == "__main__":
    main()