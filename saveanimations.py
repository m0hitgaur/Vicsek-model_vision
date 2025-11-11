import matplotlib.pyplot as plt
import numpy as np
import os

current_directory = os.getcwd()

# Main loop for user input
flag = 0

while flag == 0:
    check = input("Single frame(s/S) or multiple frames(m/M): ")

    if check.lower() == "m":
        # Parameters
        noise = input("Noise: ")
        while noise not in ["0.5", "0.05", "1"]:
            print("Invalid choice")
            noise = input("Noise: ")

        angle = input("Angle: ")
        while angle not in ["45", "90", "120", "180"]:
            print("Invalid choice")
            angle = input("Angle: ")

        trial = input("Trial: ")

        # Load details from the parameter file
        detail = []
        with open(current_directory + f'/Angle_{angle}/Noise_{noise}/parameters.txt', 'r') as file:
            for line in file:
                detail.append(line)

        Length_of_box = float(detail[1])   # Size of the grid
        maxiter = int(detail[3])
        Number_of_agents = int(detail[0])
        Lx = int(detail[1])
        Ly = float(detail[2])
        dt = float(detail[5])

        # Create visualization folder
        visualization_path = current_directory + f'/Angle_{angle}/Noise_{noise}/visualization'
        if not os.path.exists(visualization_path):
            os.makedirs(visualization_path)

        times = []
        for i in range(maxiter):
            if i < 10:
                tf = 1
            elif i < 100:
                tf = 10
            elif i < 1000:
                tf = 50
            else:
                tf = 100
            if i % tf == 0:
                times.append(i)

        # Function to load data from files
        def load_data(path):
            data = []
            with open(path, 'r') as f:
                for line in f:
                    data.append(float(line.strip()))
            return np.array(data)

        # Generate and save images for each time step
        for t in range(len(times)):
            path_template_x = current_directory + f'/Angle_{angle}/Noise_{noise}/flockingdata/positionx_{trial}_{times[t]}_.dat'
            path_template_y = current_directory + f'/Angle_{angle}/Noise_{noise}/flockingdata/positiony_{trial}_{times[t]}_.dat'
            path_template_theta = current_directory + f'/Angle_{angle}/Noise_{noise}/flockingdata/theta_{trial}_{times[t]}_.dat'

            # Load position and angle data
            positionx = load_data(path_template_x)
            positiony = load_data(path_template_y)
            theta = load_data(path_template_theta)

            # Extract data for the specific time step
            px = positionx
            py = positiony
            th = theta

            # Compute velocity components
            vx = np.cos(th)
            vy = np.sin(th)

            # Create and save quiver plot
            fig, ax = plt.subplots()
            ax.quiver(px, py, vx, vy, angles='xy', scale_units='xy', scale=1)
            ax.set_xlim([0, Lx])
            ax.set_ylim([0, Ly])
            ax.set_title(f"N={Number_of_agents}|η={noise}|α={angle}|t={times[t]}")
            plt.savefig(os.path.join(visualization_path, f'animation_{trial}_{times[t]}.png'))
            plt.close(fig)  # Close the figure to free up memory

        flag = 1

    elif check.lower() == "s":
        # Parameters
        noise = input("Noise: ")
        while noise not in ["0.5", "0.05", "1"]:
            print("Invalid choice")
            noise = input("Noise: ")

        angle = input("Angle: ")
        while angle not in ["45", "90", "120", "180"]:
            print("Invalid choice")
            angle = input("Angle: ")

        time = input("Time: ")
        trial = input("Trial: ")

        # Load details from the parameter file
        detail = []
        with open(current_directory + f'/Angle_{angle}/Noise_{noise}/parameters.txt', 'r') as file:
            for line in file:
                detail.append(line)

        # Function to load data from files
        def load_data(path):
            data = []
            with open(path, 'r') as f:
                for line in f:
                    data.append(float(line.strip()))
            return np.array(data)

        # File paths for data
        path_template_x = current_directory + f'/Angle_{angle}/Noise_{noise}/flockingdata/positionx_{trial}_{time}_.dat'
        path_template_y = current_directory + f'/Angle_{angle}/Noise_{noise}/flockingdata/positiony_{trial}_{time}_.dat'
        path_template_theta = current_directory + f'/Angle_{angle}/Noise_{noise}/flockingdata/theta_{trial}_{time}_.dat'

        # Load position and angle data
        positionx = load_data(path_template_x)
        positiony = load_data(path_template_y)
        theta = load_data(path_template_theta)

        # Extract data for the specific time step
        px = positionx
        py = positiony
        th = theta

        # Compute velocity components
        vx = np.cos(th)
        vy = np.sin(th)

        # Create and save quiver plot
        fig, ax = plt.subplots()
        ax.quiver(px, py, vx, vy, angles='xy', scale_units='xy', scale=1)
        ax.set_xlim([0, int(detail[1])])
        ax.set_ylim([0, float(detail[2])])
        ax.set_title(f"N={int(detail[0])}|η={noise}|α={angle}|t={time}")
        plt.show()
        plt.close(fig)

        flag = 1

    else:
        print("Wrong option. Try again!")
