"""Additive corrected finite witness; original v1 remains immutable failed evidence."""
import unittest
import test_discriminators as base

F=base.F

class IndependentDiscriminatorsV2(base.IndependentDiscriminators):
    def test_half_angle_sign_and_chronological_rounding(self):
        theta=F(-1)
        s,c=base.trig(theta,1,3)
        self.assertEqual(s,(F(-5,8),F(-3,8)))
        self.assertEqual(base.row(theta,(F(1),F(1)),(F(),F()),1,3)[1],s)
        actual_s,actual_c,_=base.actual.finite_trig(theta/2,base.actual.MeasuredWork(),1,3)
        self.assertEqual(((actual_s.lo,actual_s.hi),(actual_c.lo,actual_c.hi)),(s,c))
        u,v=(F(1,7),F(1,7)),(F(2,9),F(2,9))
        forward=base.trace([F(-9,7),F(-1)],u,v,0,1)
        reverse=base.trace([F(-1),F(-9,7)],u,v,0,1)
        self.assertEqual(forward,((F(-3,2),F(2)),(F(-3,2),F(2))))
        self.assertEqual(reverse,((F(-3,2),F(3,2)),(F(-1,2),F(3,2))))
        self.assertNotEqual(forward,reverse)
        angles=[F(-9,7),F(-9,7)]
        uv=base.trace(angles,(F(1),F(1)),(F(),F()),0,0)
        early=base.trace(angles,(F(1),F(1)),(F(),F()),0,0,True)
        self.assertEqual(tuple(map(base.center,uv)),(F(2),F()))
        self.assertEqual(tuple(map(base.center,early)),(F(1),F()))
        self.assertNotEqual(tuple(map(base.center,uv)),tuple(map(base.center,early)))

if __name__=='__main__':
    unittest.main()
