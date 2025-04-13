import numpy as np
import matplotlib.pyplot as plt

def Trivial_Rot(x, y, res_angle):
    if 0 <= res_angle <= 45:
        return x, y, res_angle
    elif 45 < res_angle <= 135:
        return -y, x, res_angle - 90
    elif 135 < res_angle <= 225:
        return -x, -y, res_angle - 180
    elif 225 < res_angle <= 315:
        return y, -x, res_angle - 270
    elif 315 < res_angle <= 360:
        return x, y, res_angle - 360
    

def Friend_Rot(x, y, res_angle):
    if 0 <= abs(res_angle) < 8.13:
        return 25*x, 25*y, res_angle
    elif 8.13 <= abs(res_angle) < 26.565:
        if  res_angle < 0:
            return 24*x - 7*y, 7*x + 24*y, res_angle + 16.26
        else:
            return 24*x + 7*y, -7*x + 24*y, res_angle - 16.26
    elif 26.565 <= abs(res_angle) :
        if res_angle < 0:
            return 20*x - 15*y, 15*x + 20*y, res_angle + 36.87
        else:
            return 20*x + 15*y, -15*x + 20*y, res_angle - 36.87
        
def USR_CORDIC(x, y, res_angle):
    if 0 <= abs(res_angle) < 7.125/2:
        return 129*x, 129*y, res_angle
    elif 7.125/2 <= abs(res_angle):
        if res_angle < 0:
            return 128*x - 16*y, 16*x + 128*y, res_angle + 7.125
        else:
            return 128*x + 16*y, -16*x + 128*y, res_angle - 7.125
        
def CORDIC_4(x, y, res_angle):
    if res_angle < 0:
        return 32*x - y, x + 32*y, res_angle + 1.79
    else:
        return 32*x + y, -x + 32*y, res_angle - 1.79
    
def CORDIC_5(x, y, res_angle):
    if res_angle < 0:
        return 64*x - y, x + 64*y, res_angle + 0.895
    else:
        return 64*x + y, -x + 64*y, res_angle - 0.895
    
def Nano_Rot(x, y, res_angle):
    k = res_angle//0.112
    if res_angle < 0:
        return 512*x - k*y, k*x + 512*y, res_angle + 0.112*k
    else:
        return 512*x + k*y, -k*x + 512*y, res_angle - 0.112*k
    
def CORDIC_II(angle):
    x = 1
    y = 0
    x, y, angle = Trivial_Rot(x, y, angle) #stage 1
    if abs(angle) <= 0.028:
        return x, y, angle

    
    x, y, angle = Friend_Rot(x, y, angle) #stage 2
    x = x/16
    y = y/16
    if abs(angle) <= 0.028:
        return x/1.563, y/1.563, angle

    
    
    x, y, angle = USR_CORDIC(x, y, angle) #stage 3
    x = x/128
    y = y/128
    if abs(angle) <= 0.028:
        return x/(1.563*1.008), y/(1.563*1.008), angle
    
    
    x, y, angle = CORDIC_4(x, y, angle) #stage 4
    x = x/32
    y = y/32
    if abs(angle) <= 0.028:
        return x/(1.563*1.008), y/(1.563*1.008), angle
    
    
    
    x, y, angle = CORDIC_5(x, y, angle) #stage 5
    x = x/64
    y = y/64
    if abs(angle) <= 0.028:
        return x/(1.563*1.008), y/(1.563*1.008), angle

    
    
    x, y, angle = Nano_Rot(x, y, angle) #stage 6
    x = x/512
    y = y/512
    if abs(angle) <= 0.028:
        return x/(1.563*1.008), y/(1.563*1.008), angle

   
    
    return x/(1.563*1.008), y/(1.563*1.008), angle
    


x = np.linspace(0, 360, 10000)
trans_x = np.zeros_like(x)
relative_error_cos = np.zeros_like(x)
relative_error_sin = np.zeros_like(x)

for i in range(len(x)):
    input_x = x[i]
    input_x = float(input_x)

    x_out, y_out, angle = CORDIC_II(input_x)

    trans_x[i] = x_out
    
    real_x = np.cos(input_x*np.pi/180)
    real_y = np.sin(input_x*np.pi/180)

    relative_error_cos[i] = (np.abs((real_x - x_out)/real_x))*100

    relative_error_sin[i] = (np.abs((real_y - y_out)/real_y))*100

plt.xlim(0, 360)
plt.ylim(0, 1)
# plt.plot(x, trans_x)
plt.scatter(x, relative_error_cos, s=1)
plt.scatter(x, relative_error_sin, s=1)
plt.xlabel("Angle (degree)")
plt.ylabel("Relative error (%)")
plt.legend(["cosine", "sine"])
plt.title("CORDIC II relative error")
plt.show()
