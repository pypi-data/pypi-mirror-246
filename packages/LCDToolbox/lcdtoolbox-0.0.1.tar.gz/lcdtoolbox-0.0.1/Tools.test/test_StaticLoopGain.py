

from Tools.StaticGain import calculate_static_loop_gain
from sympy import symbols

class Test_calculate_static_loop_gain:
    def test_TestCase1(self):
        """
        From exam 2021
        """
        Kp, tau, s, c, b = symbols('Kp, tau, s, c, b')
        G1 = c/(tau*s + 1)
        G2 = 1/s
        H = b

        G_ol = (Kp * G1 * G2 * H).simplify()
        G_ol
        Kp, b, c = symbols('Kp b c')
        K0 = calculate_static_loop_gain(G_ol)
        assert K0 == Kp*b*c