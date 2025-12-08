import os, json
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')

    origin      = os.getcwd()
    paper       = os.path.join(origin, 'paper')
    simulation  = os.path.join(origin, 'simulations')
    results     = os.path.join(origin, 'results')

    if not os.path.exists(paper) or not os.path.exists(simulation):
        raise FileExistsError('Paper/Simulations folder(s) do not exist')

    os.makedirs(results, exist_ok = True)

    for f in os.listdir(simulation):
        name = Path(f).stem

        paper_data_path = os.path.join(paper, f'{name}.csv')

        if not os.path.exists(paper_data_path):
            print(f'Equivalent Paper Data not founded.')
            
            continue

        paper_data = pd.read_csv(paper_data_path, header = None)

        with open(os.path.join(simulation, f), 'r') as file:
            simulation_data = json.load(file)

        processed_data = []

        for d in simulation_data:
            processed_data.append((
                float(d['porosity']),
                float(d['permeability']) / 3**2
            ))
            
        plt.figure(figsize = (8, 5))

        plt.plot(paper_data[0].values, paper_data[1].values, 'k-', label = 'Paper')
        plt.plot(np.array([p[0] for p in processed_data]), np.array([p[1] for p in processed_data]), 'bo', label = 'Simulation')

        plt.xlabel('Porosity')
        plt.ylabel('Permeability / R²')

        plt.xlim(0.6, 1)
        plt.yscale('log')
        plt.ylim(1e-3, 1e2)
        
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(results, f'{name}.png'), dpi = 300)