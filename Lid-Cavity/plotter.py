import os
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

def plotter(file_name: str, orienation: str = 'x'):
    target_path = os.path.join(paper_path, file_name, f'{orienation}.csv')

    if os.path.exists(target_path):
        folder_path = os.path.join(results_path, file_name)
        
        os.makedirs(folder_path, exist_ok = True)

        data = pd.read_csv(target_path, header = None)

        x_paper = data[0] / (nx if orienation == 'x' else 1)
        y_paper = data[1] / (1 if orienation == 'x' else ny)

        x_sim = [i / nx for i in range(nx)] if orienation == 'x' else (u[nx // 2, :] / u0)
        y_sim = (v[:, ny // 2] / u0)  if orienation == 'x' else [i / ny for i in range(ny)]

        fig, ax = plt.subplots(figsize=(7, 5))

        if orienation == 'x':
            ax.set_xlim(0, 1)
        else:
            ax.set_ylim(0, 1)

        ax.plot(x_paper, y_paper, color = 'r', marker='o', linestyle=' ')
        ax.plot(x_sim, y_sim, color = 'b', marker=' ', linestyle='-')

        ax.set_xlabel('x/X' if orienation == 'x' else 'u/U')
        ax.set_ylabel('v/U' if orienation == 'x' else 'y/Y')

        ax.legend(['Paper', 'Simualtion'])

        ax.set_title(f'{file_name} {'Horizontal' if orienation == 'x' else 'Vertical'} ({it})')
        
        plt.savefig(os.path.join(folder_path, f'{orienation}.png'))

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')

    origin_path = os.getcwd()

    paper_path = os.path.join(origin_path, 'paper')
    simulation_path = os.path.join(origin_path, 'simulations')

    results_path = os.path.join(origin_path, 'results')

    if not os.path.exists(paper_path) or not os.path.exists(simulation_path):
        raise FileExistsError('Paper/Simulations folder(s) do not exist')
    
    for file in [f for f in os.listdir(simulation_path) if f.endswith('.npy') and os.path.isfile(os.path.join(simulation_path, f))]:
        file_name = Path(file).stem

        data = np.load(os.path.join(simulation_path, file), allow_pickle = True).item()

        tau = data['meta']['tau']
        u0 = data['meta']['u0']
        it = data['meta']['iteration']

        u = data['u'][1:-1, 1:-1]
        v = data['v'][1:-1, 1:-1]

        nx, ny = u.shape

        folder_path = os.path.join(paper_path, file_name)

        if os.path.exists(folder_path):
            data_files = [f for f in os.listdir(folder_path) if f.endswith('.csv') and os.path.isfile(os.path.join(folder_path, f))]

            for f in data_files:
                plotter(file_name = file_name, orienation = Path(f).stem)