import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider

import seaborn as sns

sns.set_style('darkgrid')

OMEGA = np.pi / 4

pi_chr = '\u03C0'
OMEGA_PRINT = f"{pi_chr}/4"

freq_x = 4
freq_y = 2

AMP_X = 5
AMP_Y = 2

no_samples = 2000
TIME = np.linspace(0, 2*np.pi, no_samples)


def create_sines():
    sin_x = np.array([AMP_X * np.sin(freq_x * TIME + OMEGA)], dtype="float")
    sin_y = np.array([AMP_Y * np.sin(freq_y * TIME)], dtype="float")

    sin_x = np.transpose(sin_x)
    sin_y = np.transpose(sin_y)

    return sin_x, sin_y


def plot_sines(sin_x, sin_y):
    fig = plt.figure()
    ax1 = plt.subplot(311)
    ax2 = plt.subplot(312, sharex=ax1)
    ax3 = plt.subplot(313)

    # Setting pi values as ticks and labels
    ax1.set_xlim(0, 2*np.pi)
    ax1.set_xticks(np.arange(0, 2*np.pi + 0.01, np.pi / 4))

    x_labels = [
        '$0$', r'$\pi/4$', r'$\pi/2$', r'$3\pi/4$', r'$\pi$',
        r'$5\pi/4$', r'$3\pi/2$', r'$7\pi/4$', r'$2\pi$'
    ]
    ax1.set_xticklabels(x_labels)

    # sin_X subplot
    line_x, = ax1.plot(TIME, sin_x)

    ax1.set_ylim(-(AMP_X + 0.1), AMP_X + 0.1)
    ax1.set_yticks(np.arange(-AMP_X, AMP_X))

    ax1.set_ylabel("X value")
    ax1.grid(True, which='both')

    # sin_Y subplot
    line_y, = ax2.plot(TIME, sin_y)

    # ax2.set_xlim(0, 2*np.pi)
    ax2.set_ylim(-(AMP_Y + 0.1), AMP_Y + 0.1)
    ax2.set_yticks(np.arange(-AMP_Y, AMP_Y))

    ax2.set_ylabel("Y value")
    ax2.grid(True, which='both')

    # Sliders' subplot
    ax3.axis('off')

    fig.tight_layout()
    return fig, line_x, line_y


def _x_slider(nfreq_x, fig):
    # On change of x slider
    global sin_x, freq_x

    freq_x = round(nfreq_x, 1)

    sin_x = np.array([AMP_X * np.sin(nfreq_x * TIME + OMEGA)], dtype="float")
    sin_x = np.transpose(sin_x)

    line_x.set_ydata(sin_x)
    fig.canvas.draw_idle()  # Update figure

    title = (
        f"x = {AMP_X}sin({freq_x}t + {OMEGA_PRINT})\n" +
        f"y = {AMP_Y}sin({freq_y}t)"
    )
    ax.set_title(title, fontsize=14)

    dot.set_visible(True)
    anim.event_source.start()
    anim.frame_seq = anim.new_frame_seq()


def _y_slider(nfreq_y, fig):
    # On change of y slider
    global sin_y, freq_y

    freq_y = round(nfreq_y, 1)

    sin_y = np.array([AMP_Y * np.sin(nfreq_y * TIME)], dtype="float")
    sin_y = np.transpose(sin_y)

    line_y.set_ydata(sin_y)
    fig.canvas.draw_idle()  # Update figure

    title = (
        f"x = {AMP_X}sin({freq_x}t + {OMEGA_PRINT})\n" +
        f"y = {AMP_Y}sin({freq_y}t)"
    )
    ax.set_title(title, fontsize=14)

    dot.set_visible(True)
    anim.event_source.start()
    anim.frame_seq = anim.new_frame_seq()


def reset_anim(info):
    """Callback func for button which resets animation; info is not used."""
    print("Animation restarted!")
    anim.frame_seq = anim.new_frame_seq()
    dot.set_visible(True)
    anim.event_source.start()


def add_widgets(fig):
    slider_ax = fig.add_axes([0.2, 0.2, 0.65, 0.03])
    slider_x = Slider(
        slider_ax,
        "X frequency",
        valmin=1,
        valmax=20,
        valinit=freq_x,
        valstep=0.1
    )

    slider_ax = fig.add_axes([0.2, 0.15, 0.65, 0.03])
    slider_y = Slider(
        slider_ax,
        "Y frequency",
        valmin=1,
        valmax=20,
        valinit=freq_y,
        valstep=0.1
    )

    # TODO: Currently button presence lags animation a lot
    # while hovering over sines' figure

    # butt_ax = fig.add_axes([0.45, 0.08, 0.08, 0.05])
    # reset_butt = Button(
    #     butt_ax,
    #     "Reset"
    # )

    return slider_x, slider_y


def update(i, curve):
    curve.set_data(sin_x[:i, :], sin_y[:i, :])
    dot.set_data(sin_x[i, :], sin_y[i, :])

    # Stop animation at the end and set dot invisible
    if i == no_samples - 1:
        anim.event_source.stop()
        dot.set_visible(False)


def create_curve():
    title = (
        f"x = {AMP_X}sin({freq_x}t + {OMEGA_PRINT})\n" +
        f"y = {AMP_Y}sin({freq_y}t)"
    )
    ax.set_title(title, fontsize=14)

    ax.set_xlim([-(AMP_X + 0.1), AMP_X + 0.1])
    ax.set_ylim([-(AMP_Y + 0.1), AMP_Y + 0.1])

    curve, = ax.plot([], [])
    dot, = ax.plot([], [], 'o', color='red')

    anim = animation.FuncAnimation(
        curve_fig,
        lambda i: update(i, curve),
        frames=len(TIME),
        interval=1
    )

    return anim, dot


if __name__ == "__main__":
    sin_x, sin_y = create_sines()

    fig, line_x, line_y = plot_sines(sin_x, sin_y)
    slider_x, slider_y = add_widgets(fig)

    curve_fig, ax = plt.subplots(1, 1)
    anim, dot = create_curve()

    slider_x.on_changed(lambda val: _x_slider(val, fig))
    slider_y.on_changed(lambda val: _y_slider(val, fig))
    # reset_butt.on_clicked(reset_anim)

    plt.show()
