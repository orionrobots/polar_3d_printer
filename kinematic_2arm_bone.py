""" Info from http://www.ryanjuckett.com/programming/analytic-two-bone-ik-in-2d/ helped
"""
import math


class Kinematic2Bone:
    """System for positioning two bones to reach a target from origin. Set up static items first,
    then solve for target positions after"""
    def __init__(self, length1, length2):
        self.length1 = length1
        self.length2 = length2
        assert length1 > 0 and length2 > 0
        self.cos_angle2_denom = 2.0 * length1 * length2
        assert self.cos_angle2_denom > 0.0001
        self.sq_both_len = length1 * length1 + length2 * length2

    def solve_for(self, target, negative_sol=False):
        """solve the kinematic solution for the target.
        Set negative_Sol to true to get the alternate negative solution.
        Credit to ryan juckett.
        Raise if no valid solutions. Approx not allowed here."""
        target_dist_sqr = (target[0] * target[0]) + (target[1] * target[1])
        cos_angle2 = (target_dist_sqr - self.sq_both_len) / self.cos_angle2_denom
        # assert in legal cosine range?
        assert -1.0 <= cos_angle2 <= 1.0
        angle2 = math.acos(cos_angle2)
        if negative_sol:
            angle2 = -angle2
        sin_angle2 = math.sin(angle2)

        # Compute the value of angle1 based on the sine and cosine of angle2
        tri_adjacent = self.length1 + self.length2 * cos_angle2
        tri_opposite = self.length2 * sin_angle2

        tan_y = target[1] * tri_adjacent - target[0] * tri_opposite
        tan_x = target[0] * tri_adjacent + target[1] * tri_opposite

        # Note that it is safe to call Atan2(0,0) which will happen if targetX and
        # targetY are zero
        angle1 = math.atan2(tan_y, tan_x)
        return angle1, angle2


def kinematic_solution(length1, length2, target, negative_2=False):
    """rods are connected at pivot point. We want the angles.
    target - tuple/list indexable of 2 - x,y.
    output - (motor1_angle, motor2_angle). Credit to ryan juckett.
    Raise if no valid solutions. Approx not allowed here."""
    assert length1 > 0 and length2 > 0

    cos_angle2_denom = 2.0 * length1 * length2
    assert cos_angle2_denom > 0.0001

    target_dist_sqr = (target[0] * target[0]) + (target[1] * target[1])

    cos_angle2 = (target_dist_sqr - length1 * length1 - length2 * length2) / cos_angle2_denom
    # assert in legal cosine range?
    assert -1.0 <= cos_angle2 <= 1.0
    angle2 = math.acos(cos_angle2)
    if negative_2:
        angle2 = -angle2
    sin_angle2 = math.sin(angle2)

    # Compute the value of angle1 based on the sine and cosine of angle2
    tri_adjacent = length1 + length2 * cos_angle2
    tri_opposite = length2 * sin_angle2

    tan_y = target[1] * tri_adjacent - target[0] * tri_opposite
    tan_x = target[0] * tri_adjacent + target[1] * tri_opposite

    # Note that it is safe to call Atan2(0,0) which will happen if targetX and
    # targetY are zero
    angle1 = math.atan2(tan_y, tan_x)
    return angle1, angle2


def kine_degrees(*args):
    result = kinematic_solution(*args)
    return math.degrees(result[0]), math.degrees(result[1])

if __name__ == "__main__":
    rods = 10
    print(kine_degrees(rods, rods, (1, 1) ))
    print(kine_degrees(rods, rods, (0, 0) ))
    print(kine_degrees(rods, rods, (0, 8) ))
    print(kine_degrees(rods, rods, (0, 10) ))
    print(kine_degrees(rods, rods, (0, 19) ))
    print(kine_degrees(rods, rods, (0, 20) ))
    print(kine_degrees(rods, rods, (20, 0) ))
    print(kine_degrees(rods, rods, (0.1, 5.2) ))
