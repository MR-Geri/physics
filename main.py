import random
from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
from time import time


class DoublePendulum:
    def __init__(self, init_state=None, l1=1.0, l2=1.0, m1=1.0, m2=1.0, g=9.8, origin=(0, 0)):
        if init_state is None:
            init_state = [120, 0, -20, 0]
        self.init_state = np.asarray(init_state, dtype='float')
        self.params = (l1, l2, m1, m2, g)
        self.origin = origin
        self.time_elapsed = 0
        self.state = self.init_state * np.pi / 180.

    def position(self):
        """compute the current x,y positions of the pendulum arms"""
        (L1, L2, M1, M2, G) = self.params

        x = np.cumsum([self.origin[0], L1 * sin(self.state[0]), L2 * sin(self.state[2])])
        y = np.cumsum([self.origin[1], -L1 * cos(self.state[0]), -L2 * cos(self.state[2])])
        return x, y

    def energy(self):
        """compute the energy of the current state"""
        (L1, L2, M1, M2, G) = self.params

        x = np.cumsum([L1 * sin(self.state[0]), L2 * sin(self.state[2])])
        y = np.cumsum([-L1 * cos(self.state[0]), -L2 * cos(self.state[2])])
        vx = np.cumsum([L1 * self.state[1] * cos(self.state[0]), L2 * self.state[3] * cos(self.state[2])])
        vy = np.cumsum([L1 * self.state[1] * sin(self.state[0]), L2 * self.state[3] * sin(self.state[2])])

        u = G * (M1 * y[0] + M2 * y[1])
        k = 0.5 * (M1 * np.dot(vx, vx) + M2 * np.dot(vy, vy))

        return u + k

    def dstate_dt(self, state, t):
        """compute the derivative of the given state"""
        (M1, M2, L1, L2, G) = self.params

        dydx = np.zeros_like(state)
        dydx[0] = state[1]
        dydx[2] = state[3]

        cos_delta = cos(state[2] - state[0])
        sin_delta = sin(state[2] - state[0])

        den1 = (M1 + M2) * L1 - M2 * L1 * cos_delta * cos_delta
        dydx[1] = (M2 * L1 * state[1] * state[1] * sin_delta * cos_delta
                   + M2 * G * sin(state[2]) * cos_delta
                   + M2 * L2 * state[3] * state[3] * sin_delta
                   - (M1 + M2) * G * sin(state[0])) / den1

        den2 = (L2 / L1) * den1
        dydx[3] = (-M2 * L2 * state[3] * state[3] * sin_delta * cos_delta
                   + (M1 + M2) * G * sin(state[0]) * cos_delta
                   - (M1 + M2) * L1 * state[1] * state[1] * sin_delta
                   - (M1 + M2) * G * sin(state[2])) / den2

        return dydx

    def step(self, dt):
        """execute one time step of length dt and update state"""
        self.state = integrate.odeint(self.dstate_dt, self.state, [0, dt])[1]
        self.time_elapsed += dt


# ------------------------------------------------------------
# set up initial state and global variables
state = [random.randint(-180, 180), 0, random.randint(-180, 180), 0]
pendulum = DoublePendulum(state)  # [180.0, 0.0, -20.0, 0.0]
dt = 1.0 / 60  # 60 fps

# ------------------------------------------------------------
# set up figure and animation
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2))
ax.grid()

line, = ax.plot([], [], 'o-', lw=2)
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
energy_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)


def init():
    """initialize animation"""
    line.set_data([], [])
    time_text.set_text('')
    energy_text.set_text('')
    return line, time_text, energy_text


def animate(i):
    """perform animation step"""
    global pendulum, dt
    pendulum.step(dt)

    line.set_data(*pendulum.position())
    time_text.set_text('time = %.1f' % pendulum.time_elapsed)
    energy_text.set_text('energy = %.3f J' % pendulum.energy())

    return line, time_text, energy_text


if __name__ == '__main__':
    # choose the interval based on dt and the time to animate one step
    t0 = time()
    animate(0)
    t1 = time()
    interval = 1000 * dt - (t1 - t0)
    #
    ani = animation.FuncAnimation(fig, animate, frames=600, interval=interval, blit=True, init_func=init)
    ani.save('double_pendulum_new.mp4', fps=60, extra_args=['-vcodec', 'libx264'])
