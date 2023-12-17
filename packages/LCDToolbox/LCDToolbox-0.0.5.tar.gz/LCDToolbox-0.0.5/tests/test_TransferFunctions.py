
from lcdtoolbox.TransferFunctions import InputType, steady_state_error
from sympy import symbols

class Test_steady_state_error:
    def test_TestCase1(self):
        """
        From exam 2021
        """
        Kp, b, c = symbols('Kp b c')
        K0 = Kp*b*c

        assert steady_state_error(N=1, input_type=InputType.RAMP, h0=1, K0=K0) == 1/K0

    def test_TestCase2(self):
        """
        From exam 2015 Q20
        """

        assert steady_state_error(N=0, input_type=InputType.STEP, h0=1, K0=10) - 0.9 < 0.1