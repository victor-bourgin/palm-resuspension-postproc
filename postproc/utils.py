def cells_volume(x, y, zw_3d):
    # Compute cell sizes in all directions
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    dz = zw_3d[1:] - zw_3d[:-1]

    return dx*dy*dz