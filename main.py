import matplotlib.pyplot as plt 

import numpy as np 

import matplotlib.animation as animation



   


ypoints = np.array([1,3,7,5,8]) 
xpoints = np.array([5,3,7,8,1]) 

plt.plot(xpoints, ypoints) 
plt.scatter(xpoints, ypoints)    
plt.show() 


angles = np.linspace(0, 360, 200)    
rad_angles = np.radians(angles)
sin_fun = np.sin(rad_angles) 
fig, ax = plt.subplots() 
line, = ax.plot(angles, np.sin(rad_angles))   
print(sin_fun)
plt.plot(angles, sin_fun)
plt.xlabel("Angle (degrees)")
plt.ylabel("sin(angle)") 
ax.set_ylim(-1.2, 1.2)   
#plt.show() 

def update(frame): 
    line.set_ydata(np.sin(rad_angles + frame/10)) 
    return line, 
ani = animation.FuncAnimation(fig, update, frames= 50, interval = 30, blit = True) 
plt.show()
  




