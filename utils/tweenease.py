import time
import math
import enum

# Easing library

class EaseType(enum.Enum):
    easeincubic = 0
    easeoutcubic = 1
    easeinoutcubic = 2
    easeinquart = 3
    easeoutquart = 4
    easeinoutquart = 5

class Tween():
    def __init__(self, duration, type = EaseType.easeincubic):
        self.duration = duration
        self.type = type
        self.done = False
        self.ellapsed_time = 0
        self.start_time = 0
        self.ratio = 0

    def start(self):
        if(self.duration == 0 or self.duration is None):
            print("No duration set for this Tween class instance !")
            return
        self.ratio = 0
        self.done = False
        self.start_time = time.time()
    
    def end(self):
        self.done = True
        self.ratio = 1
        self.start_time = 0
        self.ellapsed_time = 0

    def isdone(self):
        return self.done
    
    def estimate(self):
        self.ellapsed_time = time.time()-self.start_time
        self.ratio = self.ellapsed_time / self.duration
        if self.ratio >= 1:
            self.end()
        if(self.type == EaseType.easeincubic):
            return self.ease_in_cubic(self.ratio)
        elif(self.type == EaseType.easeoutcubic):
            return self.ease_out_cubic(self.ratio)
        elif(self.type == EaseType.easeinoutcubic):
            return self.ease_in_out_cubic(self.ratio)
        elif(self.type == EaseType.easeinquart):
            return self.ease_in_quart(self.ratio)
        elif(self.type == EaseType.easeoutquart):
            return self.ease_out_quart(self.ratio)
        elif(self.type == EaseType.easeinoutquart):
            return self.ease_in__out_quart(self.ratio)
        else: return None

    @staticmethod
    def ease_in_cubic(t:float):
        return t**3

    @staticmethod
    def ease_out_cubic(t:float):
        return 1-math.pow(1-t,3)

    @staticmethod
    def ease_in_out_cubic(t:float):
        if(t < 0.5):
            return 4 * t * t * t
        return 1 - math.pow(-2 * t + 2, 3) / 2

    @staticmethod
    def ease_in_quart(t:float):
        return t**4

    @staticmethod
    def ease_out_quart(t:float):
        return 1 - math.pow(1 - t, 4)

    @staticmethod
    def ease_in__out_quart(t:float):
        if(t < 0.5):
            return 8 * t * t * t * t
        return 1 - math.pow(-2 * t + 2, 4) / 2



'''tween = Tween(1, EaseType.easeinquart)

run = True
tween.start()
while run:
    time.sleep(0.05)
    print(str(tween.estimate())+",")
    run = not tween.isdone'''
