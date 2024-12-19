import csv
import os
import re


def cells_volume(x, y, zw_3d):
    # Compute cell sizes in all directions
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    dz = zw_3d[1:] - zw_3d[:-1]

    return dx*dy*dz

def read_exp_data() -> dict:
    # Name pattern of the exp data files
    pattern = re.compile(r"alumina(\d+)_run(\d+)\.csv")

    data = {}

    for filename in os.listdir("exp/"):
        match = pattern.match(filename)
        # Extract the diameter and run number
        if match:
            diameter = int(match.group(1))
            run_nb = int(match.group(2))

            # Initialize data[diameter] if it doesn't exist
            if diameter not in data:
                data[diameter] = {}

            # Read data from file and store it
            with open(f"exp/{filename}", mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row

                data[diameter][run_nb] = [[], []]

                for row in reader:
                    data[diameter][run_nb][0].append(float(row[0]))
                    data[diameter][run_nb][1].append(float(row[1]))
    return data