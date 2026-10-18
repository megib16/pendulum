import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

g = 9.81          # gravity (m/s^2)
L = 1.5           # pendulum length (m)
dt = 0.02         # time step (s)
n_frames = 500

# Materials and sizes
rho_rod = 7850.0         # steel density (kg/m^3)
rod_radius = 0.005       # rod cross-section radius (m)
rho_bob = 1200.0         # plastic density (kg/m^3)
bob_radius = 0.1         # bob radius (m)

# Mass = density * volume
m_rod = rho_rod * np.pi * rod_radius**2 * L          # cylinder
m_bob = rho_bob * (4 / 3) * np.pi * bob_radius**3    # solid sphere
print(f"rod mass: {m_rod:.2f} kg, bob mass: {m_bob:.2f} kg")

# Moment of inertia about the pivot:
#   rod (thin, pivoted at one end): 1/3 m L^2
#   bob (sphere, parallel-axis theorem): m L^2 + 2/5 m r^2
I = m_rod * L**2 / 3 + m_bob * L**2 + 0.4 * m_bob * bob_radius**2
# Gravity torque acts at each center of mass: rod at L/2, bob at L
torque_arm = m_rod * L / 2 + m_bob * L
k = g * torque_arm / I   # replaces g / L from the ideal pendulum

# Simulate: theta'' = -k * sin(theta) - damping * theta'
theta = np.radians(90)   # starting angle
omega = 0.0              # starting angular velocity
thetas = []
for _ in range(n_frames):
    thetas.append(theta)
    omega += (-k * np.sin(theta) - 0.2 * omega) * dt
    theta += omega * dt

thetas = np.array(thetas)
x = L * np.sin(thetas)
y = -L * np.cos(thetas)

fig, ax = plt.subplots()
ax.set_xlim(-1.2 * L, 1.2 * L)
ax.set_ylim(-1.2 * L, 0.2 * L)
ax.set_aspect("equal")
ax.set_title("Pendulum")

rod, = ax.plot([], [], "k-", lw=2) #k stands for black and - for a solid line    
bob = plt.Circle((0, 0), bob_radius, color="red")  # drawn in meters, so its size is to scale
ax.add_patch(bob)


def update(frame):
    rod.set_data([0, x[frame]], [0, y[frame]])
    bob.set_center((x[frame], y[frame]))
    return rod, bob


ani = animation.FuncAnimation(fig, update, frames=n_frames, interval=dt * 1000, blit=True)
plt.show()
