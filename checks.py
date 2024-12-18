import sys

from netCDF4 import Dataset

from postproc.output_checks import atmo_surf_mass_balance, number_mass_consistency


def main():
    # Parameter
    diameter = 2e-5
    density = 2500
    # Output files
    fxy_path = f'./data/{sys.argv[1]}_xy.0{sys.argv[2]}.nc'
    f3d_path = f'./data/{sys.argv[1]}_3d.0{sys.argv[2]}.nc'

    # Load netCDF files
    fxy = Dataset(fxy_path, 'r+')
    f3d = Dataset(f3d_path, 'r+')

    # Load dimensions
    x, y = f3d.variables['x'][:], f3d.variables['y'][:]
    zu_3d, zw_3d = f3d.variables['zu_3d'][:], f3d.variables['zw_3d'][:]
    time = f3d.variables['time'][1:]

    # Load variables
    mconc1 = f3d.variables['dust_mc_bin1'][:]
    mconc2 = f3d.variables['dust_mc_bin2'][:]

    surf_mass1 = fxy.variables['dust_surf_mass_bin1_xy'][:]
    surf_mass2 = fxy.variables['dust_surf_mass_bin2_xy'][:]

    surf_numb1 = fxy.variables['dust_surf_numb_bin1_xy'][:]
    surf_numb2 = fxy.variables['dust_surf_numb_bin2_xy'][:]

    atmo_surf_mass_balance(time, x, y, zw_3d, mconc2, surf_mass2)

    number_mass_consistency(time, surf_mass2, surf_numb2, diameter, density)

if __name__ == '__main__':
    main()
