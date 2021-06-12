from .formulae import convert_to, si
import numpy as np
from matplotlib import pyplot


def plot(var, mult, qlabel, fname, output):
    dt = output['t'][1] - output['t'][0]
    dz = output['z'][1] - output['z'][0]
    tgrid = np.concatenate(((output['t'][0] - dt / 2,), output['t'] + dt / 2))
    zgrid = np.concatenate(((output['z'][0] - dz / 2,), output['z'] + dz / 2))
    convert_to(zgrid, si.km)

    fig = pyplot.figure(constrained_layout=True)
    gs = fig.add_gridspec(25, 5)
    ax1 = fig.add_subplot(gs[:-1, 0:4])
    mesh = ax1.pcolormesh(tgrid, zgrid, output[var]*mult, cmap='twilight', rasterized=True)

    ax1.set_xlabel('time [s]')
    ax1.set_ylabel('z [km]')

    cbar = fig.colorbar(mesh, fraction=.05, location='top')
    cbar.set_label(qlabel)

    ax2 = fig.add_subplot(gs[:-1, 4:], sharey=ax1)
    ax2.set_xlabel(qlabel)

    last_t = -1
    for i, t in enumerate(output['t']):
        x, z = output[var][:, i]*mult, output['z'].copy()
        convert_to(z, si.km)
        params = {'color': 'black'}
        for line_t, line_s in {3: ':', 6: '--', 9: '-', 12: '-.'}.items():
            if last_t < line_t * si.minutes <= t:
                print(f"plotting line at={t}")
                params['ls'] = line_s
                ax2.plot(x, z, **params)
                ax1.axvline(t, **params)
        last_t = t

