import unittest
import sys
from os.path import join
sys.path.append(join('..'))

import quantities as pq

import astroquantities as aq
from equations import scaleHeight, meanPlanetTemp, starLuminosity, ratioTerminatorToStar, SNRPlanet,\
    surfaceGravity, transitDuration, density, estimateMass, calcSemiMajorAxis, calcSemiMajorAxis2, calcPeriod, \
    estimateDistance


class Test_scaleHeight(unittest.TestCase):
    def test_works_earth(self):

        mu_p = 28.964 * pq.u
        T_eff_p = 290 * pq.degK
        g_p = 9.81 * pq.m / pq.s ** 2

        answer = 8486.04 * pq.m
        result = scaleHeight(T_eff_p, mu_p, g_p)

        self.assertAlmostEqual(answer, result, 2)


class Test_meanPlanetTemp(unittest.TestCase):
    def test_works_mars(self):

        a = 1.524 * pq.au
        A_p = 0.25
        T_s = 5800 * pq.K
        R_s = 1 * aq.R_s

        answer = 231.1 * pq.K  # TODO actual answer 227.17
        result = meanPlanetTemp(A_p, T_s, R_s, a)

        self.assertAlmostEqual(answer, result, 1)


class Test_starLuminosity(unittest.TestCase):
    def test_works_sun(self):

        R_s = 1 * aq.R_s
        T_eff_s = 5780 * pq.degK

        answer = 3.89144e+26 * pq.W
        result = starLuminosity(R_s, T_eff_s)

        self.assertAlmostEqual(answer, result, delta=0.0001e27)


class Test_ratioTerminatorToStar(unittest.TestCase):
    def test_works_earth(self):

        H_p = 8500 * pq.m
        R_p = 1 * aq.R_e
        R_s = 1 * aq.R_s

        answer = 1.12264e-06 * pq.dimensionless
        result = ratioTerminatorToStar(H_p, R_p, R_s)

        self.assertTrue(answer - result < 0.001)


class Test_SNRPlanet(unittest.TestCase):
    def test_works(self):

        params = {'SNRStar': 400,
                  'starPlanetFlux': 1.12e-06,
                  'Nobs': 200,
                  'pixPerbin': 5,
                  'NVisits': 1,
                  }

        answer = 0.01417
        result = SNRPlanet(**params)

        self.assertAlmostEqual(answer, result, 5)


class Test_surfaceGravity(unittest.TestCase):
    def test_works_earth(self):

        R_p = 1 * aq.R_e
        M_p = 1 * aq.M_e

        answer = 9.823 * pq.m / pq.s**2
        result = surfaceGravity(M_p, R_p)

        self.assertAlmostEqual(answer, result, 2)


class Test_transitDuration(unittest.TestCase):
    def test_works_gj1214(self):

        R_p = 0.02 * aq.R_j
        R_s = 0.21 * aq.R_s
        i = 88.17 * pq.deg
        a = 0.014 * pq.au
        P = 1.58040482 * pq.day

        answer = 45.8329 * pq.min
        result = transitDuration(P, R_s, R_p, a, i)

        self.assertAlmostEqual(answer, result, 3)

@unittest.skip("Not written")
class Test_logg(unittest.TestCase):
    def test_works_gj1214(self):
        assert False


@unittest.skip("Not written")
class Test_starTemperature(unittest.TestCase):
    def test_works_gj1214(self):
        assert False


@unittest.skip("Not written")
class Test_transitDepth(unittest.TestCase):
    def test_works_gj1214(self):
        assert False


class Test_density(unittest.TestCase):
    def test_works_water(self):  # Doesnt work as its not a sphere

        M = 1 * pq.kg
        R = 1 * pq.m

        answer = 0.2387 * pq.kg / pq.m**3  # TODO calcluate this result manually
        result = density(M, R).rescale(pq.kg / pq.m**3)

        self.assertAlmostEqual(answer, result, 3)

    def test_works_hd189(self):

        M = 1.144 * aq.M_j
        R = 1.138 * aq.R_j

        answer = 1.0296 * pq.g / pq.cm**3  # real answer 0.963
        result = density(M, R)

        self.assertAlmostEqual(answer, result, 3)


class Test_estimateMass(unittest.TestCase):
    def test_works_jupiter(self):

        R = 6.9911 * (10**7) * pq.m
        d = 1.326 * pq.g / pq.cm**3

        result = estimateMass(R, d).rescale(pq.kg)
        answer = 1.898*(10**27)*pq.kg

        self.assertAlmostEqual(answer, result, delta=1e24)


class Test_calcSemiMajorAxis(unittest.TestCase):
    def test_works_earth(self):

        M_s = aq.M_s
        P = 1 * pq.year

        result = calcSemiMajorAxis(P, M_s)
        answer = 1 * pq.au

        self.assertAlmostEqual(answer, result, 3)


class Test_calcSemiMajorAxis2(unittest.TestCase):
    def test_works_gj1214(self):

        T_p = 520 * pq.K
        T_s = 3026 * pq.K
        R_s = 0.21 * aq.R_s
        A_p = 0.3

        result = calcSemiMajorAxis2(T_p, T_s, A_p, R_s)
        answer = 0.01665 * pq.au

        self.assertAlmostEqual(answer, result, 3)


class Test_calcPeriod(unittest.TestCase):
    def test_works_gj1214(self):

        a = 0.014 * pq.au
        M_s = 0.153 * aq.M_s

        result = calcPeriod(a, M_s)
        answer = 1.546 * pq.day

        self.assertAlmostEqual(answer, result, 3)


class Test_estimateDistance(unittest.TestCase):
    def test_works_online_example(self):

        m = 14
        M = 0

        result = estimateDistance(m, M, 0)
        answer = 6309.6 * pq.pc

        self.assertAlmostEqual(answer, result, 1)

if __name__ == '__main__':
    unittest.main()