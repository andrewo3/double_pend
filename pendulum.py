import numpy as np

class DoublePend():
    def __init__(self,l1,l2,m1,m2,a1,a2,v1,v2):
        self.l1 = l1
        self.l2 = l2
        self.m1 = m1
        self.m2 = m2
        self.a1 = a1
        self.a2 = a2
        self.ad1 = v1
        self.ad2 = v2
        self.add1 = 0
        self.add2 = 0
        self.g = 200
    def update(self,t = 0.001):
        t1 = -0.5*self.g*np.sin(self.a2)
        t2 = -0.5*self.l1*(self.ad1**2)*np.sin(self.a1-self.a2)

        s1 = -(0.5*self.m1+self.m2)*self.g*np.sin(self.a1)
        s3 = 0.5*self.m2*self.l2*(self.ad2**2)*np.sin(self.a1-self.a2)
        s4_1 = self.m2*1.5*np.cos(self.a1-self.a2)*(-t1)
        s4_2 = self.m2*1.5*np.cos(self.a1-self.a2)*(-t2)
        s5_1 = self.m2*1.5*np.cos(self.a1-self.a2)*-0.5*self.l1*np.cos(self.a1-self.a2)
        s5_2 = self.l1*(1/3*self.m1+self.m2)
        
        self.add1 = (-s1-s3-s4_1-s4_2)/(s5_1+s5_2)

        t3 = 0.5*self.l1*self.add1*np.cos(self.a1-self.a2)

        self.add2 = 3/self.l2*(-t1-t2-t3)
        self.ad1 += self.add1 * t
        self.ad2 += self.add2 * t
        
        self.a1 += self.ad1 * t
        self.a2 += self.ad2 * t
        self.a1 %= 2 * np.pi
        self.a2 %= 2 * np.pi