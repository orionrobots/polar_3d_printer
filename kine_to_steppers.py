"""Kinematic to steppers.
This will be an output stage. It will expect an input stream stage which streams:
a1, a2, tool parameters (it will not touch tool parameters, for now pass through).
"""


class KineToSteppers:
    def __init__(self, step_distance):
        self._step_distance = step_distance
        self._input_stream = []
        self._current_position_m1 = 0
        self._current_position_m2 = 0

    def attach_input_stream(self, input_stream):
        self._input_stream = input_stream

    def start_output_stream(self):
        """"Start the output. Will generate outputs"""
        for input in self._input_stream:
            tween = self._process(input)
            for frame in tween:
                yield tween.next()

    def _process(self, input):
        """Produce a tween output for the input item"""
        # we have a current position, and a destination position.
        # Expect input to be
