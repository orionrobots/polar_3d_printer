import pygame

from pygame import (draw, image)
import math
from kinematic_2arm_bone import Kinematic2Bone


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
        self.max_color_index = len(self.colors) - 1

    def get_color(self, intended, actual):
        distx = intended[0] - actual[0]
        distx2 = distx * distx
        disty = intended[1] - actual[1]
        disty2 = disty * disty
        sqdist = distx2 + disty2
        index = int(sqdist / self.per_division)
        # if index != 0:
        #     print("%s != %s : %s" % (intended, actual, index))
        index = min(index, self.max_color_index)
        return self.colors[index]


def setup_colors():
    white = 255, 255, 255
    black = 0, 0, 0
    red = 255, 0, 0
    green = 0, 255, 0
    blue = 0, 0, 255
    return red, white


class PlotBasicKinematic:
    def __init__(self, rod_length, hw, hh, color_scale, fail_color):
        self.rod_length = rod_length
        self.hh = hh
        self.hw = hw
        self.color_scale = color_scale
        self.fail_color = fail_color
        self.solver = Kinematic2Bone(rod_length, rod_length)

    def solution_to_color(self, a1, a2, relx, rely):
        actual = ((math.cos(a1) + math.cos(a1 + a2)) * self.rod_length,
                  (math.sin(a1) + math.sin(a1 + a2)) * self.rod_length)
        color = self.color_scale((relx, rely), actual)
        return color

    def get_position(self, x, y):
        #get the info from the kine simulation
        relx = x - self.hw
        rely = y - self.hh
        try:
            a1, a2 = self.solver.solve_for((relx, rely))
        except AssertionError:
            color = self.fail_color
        else:
            color = self.solution_to_color(a1, a2, relx, rely)

        return color

normal_stepper = 1.8
lego_encoder = 1
geared_down = 1.8/4

class PlotWithStepperResolution(PlotBasicKinematic):
    step_distance = math.radians(geared_down)
    def round_to_step(self, angle_rads):
        return angle_rads - math.fmod(angle_rads, self.step_distance)

    def get_position(self, x, y):
        #get the info from the kine simulation
        relx = x - self.hw
        rely = y - self.hh
        try:
            a1, a2 = self.solver.solve_for((relx, rely))
        except AssertionError:
            color = self.fail_color
        else:
            # Do conversion here
            # round a1 and a2 to the nearest step distance
            a1 = self.round_to_step(a1)
            a2 = self.round_to_step(a2)

            color = self.solution_to_color(a1, a2, relx, rely)

        return color


def main():
    pygame.init()

    red, white = setup_colors()

    redscale = [[n, 255 - n, 0] for n in range(0, 254, 10)]
    size = width, height = 1080, 1080
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
            screen.set_at((x, y), color)
        if x % 100 == 0:
            pygame.display.update()

    image.save(screen, "test_output.png")

if __name__ == "__main__":
    main()