from sympy import symbols

from Tools.Dynamics import system_order, system_type


class Test_system_order:
    def test_TestCase1(self):
        """
        From exam 2021 Q1
        """
        s, a, b, c, gamma, beta = symbols('s a b c gamma beta')
        system = gamma*(b*s+c)/(a*s*(s**2+s*a+beta))

        assert system_order(system) == 3

class Test_system_type:
    def test_TestCase1(self):
        """
        From exam 2021 Q1
        """
        s, a, b, c, gamma, beta = symbols('s a b c gamma beta')
        system = gamma*(b*s+c)/(a*s*(s**2+s*a+beta))

        assert system_type(system) == 1