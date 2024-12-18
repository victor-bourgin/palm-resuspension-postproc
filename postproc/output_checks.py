import matplotlib.pyplot as plt
import numpy as np

from .utils import cells_volume


def atmo_surf_mass_balance(time, x, y, zw_3d, mconc, surf_mass):
    # Initialze arrays
    atmo_mass = np.zeros_like(time)
    depo_mass = np.zeros_like(time)

    # Compute total suspended dust mass
    vols = cells_volume(x, y, zw_3d)

    for t in range(len(time)):
        atmo_mass[t] = np.sum(np.sum(mconc[t,1:,:,:], axis=(1,2)) * vols) * 1000
        depo_mass[t] = np.sum(surf_mass[t,0,:,:]) * 1000

    tot_mass = atmo_mass + depo_mass

    # Estimate error
    abs_error = tot_mass[-1] - tot_mass[0]
    rel_error = abs(abs_error)/tot_mass[0]*100

    print(f'absolute error: {abs_error:.2e} g')
    print(f'relative error: {rel_error:.2e} %')

    # Plot mass evolution in the domain
    fig, ax = plt.subplots()

    ax.plot(time, atmo_mass, color='r', ls='--', label='Suspended')
    ax.plot(time, depo_mass, color='r', label='Deposited')
    ax.plot(time, tot_mass, color='k', label='Total')

    ax.set_xlim([time[0], time[-1]])
    ax.set_ylim([0.0, 1.1*tot_mass.max()])

    ax.grid(True)

    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Mass [g]')
    ax.legend()

    fig.savefig('./figs/mass_balance.png', dpi=300)


def number_mass_consistency(time, surf_mass, surf_numb, diameter, density):
    # Initialiaze arrays
    mass_tot = np.zeros_like(time)
    mass_from_num = np.zeros_like(time)

    # Mass of one particle
    part_mass = (np.pi / 6) * (diameter**3) * density

    # Compute total particle mass and number
    for t in range(len(time)):
        mass_tot[t] = np.sum(surf_mass[t,0,:,:]) * 1000
        mass_from_num[t] = np.sum(surf_numb[t,0,:,:]) * part_mass * 1000

    # Plot evolution over time
    fig, ax = plt.subplots()

    ax.plot(time, mass_tot, color='k', label='Total mass')
    ax.plot(time, mass_from_num, color='k', ls='--', label='Mass from numb.')

    ax.set_xlim([time[0], time[-1]])
    ax.set_ylim([0.0, 1.1*mass_tot.max()])

    ax.grid(True)

    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Mass [g]')
    ax.legend()

    fig.savefig('./figs/mass_consistency.png', dpi=300)
