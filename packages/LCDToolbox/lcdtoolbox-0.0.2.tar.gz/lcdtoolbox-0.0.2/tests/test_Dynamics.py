from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr

from Tools.Dynamics import system_order, system_type, calculate_static_loop_gain


class Test_system_order:
    def test_TestCase1(self):
        """
        From exam 2021 Q1
        """
        s, a, b, c, gamma, beta = symbols('s a b c gamma beta')
        system = gamma*(b*s+c)/(a*s*(s**2+s*a+beta))

        assert system_order(system) == 3
    
    def test_TestCase2(self):
        """
        From exam 2015 Q6
        """
        system = parse_expr('b*d * (gmm*s + phi)/(alpha*s + bet) * 1/(s + a) * 1/(s + c)')

        assert system_order(system) == 3

    def test_TestCase3(self):
        """
        From exam 2015 Q15
        """
        system = parse_expr('Kp*1/(s+1)*1/(s+2)*1/(s+a)')

        assert system_order(system) == 3

class Test_system_type:
    def test_TestCase1(self):
        """
        From exam 2021 Q1
        """
        s, a, b, c, gamma, beta = symbols('s a b c gamma beta')
        system = gamma*(b*s+c)/(a*s*(s**2+s*a+beta))

        assert system_type(system) == 1

    def test_TestCase2(self):
        """
        From exam 2021 Q14
        """
        system = parse_expr('Kp*b*c/(s*(s*tau + 1))')

        assert system_type(system) == 1

    def test_TestCase3(self):
        """
        From exam 2015 Q6
        """
        system = parse_expr('b*d * (gmm*s + phi)/(alpha*s + bet) * 1/(s + a) * 1/(s + c)')

        assert system_type(system) == 0

    def test_TestCase4(self):
        """
        From exam 2015 Q15
        """
        system = parse_expr('Kp*1/(s+1)*1/(s+2)*1/(s+a)')

        assert system_type(system) == 0


class Test_calculate_static_loop_gain:
    def test_TestCase1(self):
        """
        From exam 2021 Q14
        """
        G_ol = parse_expr('Kp*b*c/(s*(s*tau + 1))')
        Kp, b, c = symbols('Kp b c')
        
        K0 = calculate_static_loop_gain(G_ol)
        assert K0 == Kp*b*c

    def test_TestCase2(self):
        """
        From textbook 'Feedback control techniques' sec. 11.4
        """
        G_ol = parse_expr('Kp * 22/(100*s**2 + 5*s + 1)')
        Kp, s = symbols('Kp, s')
  
        K0 = calculate_static_loop_gain(G_ol)

        assert K0 == Kp * 22
        
    def test_TestCase3(self):
        """
        From exam 2015 Q15
        """
        system = parse_expr('Kp*1/(s+1)*1/(s+2)*1/(s+a)')
        K0_answer = parse_expr('Kp/(2*a)')

        K0 = calculate_static_loop_gain(system)

        assert K0 == K0_answer
    
