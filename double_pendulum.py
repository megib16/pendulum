import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

g = 9.81
L1, L2 = 1.0, 1.0         # rod lengths (m)
m1, m2 = 1.0, 1.0         # bob masses (kg)
dt = 0.01                 # time step (s)
n_frames = 1500


def derivs(state):
    """state = [theta1, theta2, omega1, omega2]; returns its time derivative."""
    t1, t2, w1, w2 = state
    d = t1 - t2
    den = 2 * m1 + m2 - m2 * np.cos(2 * d)
    a1 = (-g * (2 * m1 + m2) * np.sin(t1)
          - m2 * g * np.sin(t1 - 2 * t2)
          - 2 * np.sin(d) * m2 * (w2**2 * L2 + w1**2 * L1 * np.cos(d))) / (L1 * den)
    a2 = (2 * np.sin(d) * (w1**2 * L1 * (m1 + m2)
                           + g * (m1 + m2) * np.cos(t1)
                           + w2**2 * L2 * m2 * np.cos(d))) / (L2 * den)
    return np.array([w1, w2, a1, a2])


def rk4_step(state, dt):
    # Runge-Kutta 4: much more accurate than plain Euler, which drifts on chaotic systems
    k1 = derivs(state)
    k2 = derivs(state + 0.5 * dt * k1)
    k3 = derivs(state + 0.5 * dt * k2)
    k4 = derivs(state + dt * k3)
    return state + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


# Simulate: start both rods at these angles, at rest
state = np.array([np.radians(120), np.radians(-10), 0.0, 0.0])
states = []
for _ in range(n_frames):
    states.append(state)
    state = rk4_step(state, dt)
states = np.array(states)

t1, t2 = states[:, 0], states[:, 1]
x1 = L1 * np.sin(t1)
y1 = -L1 * np.cos(t1)
x2 = x1 + L2 * np.sin(t2)
y2 = y1 - L2 * np.cos(t2)

fig, ax = plt.subplots()
R = L1 + L2
ax.set_xlim(-1.1 * R, 1.1 * R)
ax.set_ylim(-1.1 * R, 1.1 * R)
ax.set_aspect("equal")
ax.set_title("Double pendulum")

rods, = ax.plot([], [], "k-", lw=2)                      # pivot -> bob 1 -> bob 2
bobs, = ax.plot([], [], "o", color="red", markersize=10)  # both bobs
trail, = ax.plot([], [], "-", color="blue", lw=1, alpha=0.5)  # path of the second bob
trail_len = 200


def update(frame):
    rods.set_data([0, x1[frame], x2[frame]], [0, y1[frame], y2[frame]])
    bobs.set_data([x1[frame], x2[frame]], [y1[frame], y2[frame]])
    start = max(0, frame - trail_len)
    trail.set_data(x2[start:frame + 1], y2[start:frame + 1])
    return rods, bobs, trail


ani = animation.FuncAnimation(fig, update, frames=n_frames, interval=dt * 1000, blit=True)
plt.show()
