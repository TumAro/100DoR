
import time

class PIDController:
    def __init__(self, kp=0, ki=0, kd=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.reset()

    def reset(self):
        # reset the controler state
        self.integral = 0.0
        self.prevError = 0.0

        self.lastControl = 0.0
        self.lastTime = time.time()

    def tune(self, kp=None, ki=None, kd=None):
        if kp is not None: self.kp = kp
        if ki is not None: self.ki = ki
        if kd is not None: self.kd = kd

    
    def heuristicPID(self, error, dt):
        self.error = error

        P = self.kp*self.error

        self.integral += self.error*dt
        I = self.ki * self.integral

        derv = (self.error - self.prevError) / dt if dt > 1e-3 else 0
        D = self.kd * derv
        self.prevError = self.error

        control = P+I+D
        self.lastControl = control

        return control, P, I, D
    
    
    def znPID(self, error, dt, init=True, KU=1, TU=1):
        self.error = error

        if init:
            P = self.kp*self.error
            return P, P, 0, 0
        
        else:
            self.kp = 0.6*KU*0.5
            self.ki = 1.2*KU/(TU*0.3)
            self.kd = 0.075*KU*TU * 0.5

            return self.heuristicPID(error, dt)