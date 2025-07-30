import os
from pathlib import Path
import matplotlib.pyplot as plt

def plotter(file_name: str, orienation: str = 'x'):
    target_path = os.path.join(paper_path, file_name, f'{orienation}.csv')

    if os.path.exists(target_path):
        folder_path = os.path.join(results_path, file_name)
        
        os.makedirs(folder_path, exist_ok = True)

if __name__ == '__main__':
    origin_path = os.getcwd()

    paper_path = os.path.join(origin_path, 'paper')
    simulation_path = os.path.join(origin_path, 'simulations')

    results_path = os.path.join(origin_path, 'results')

    if not os.path.exists(paper_path) or not os.path.exists(simulation_path):
        raise FileExistsError('Paper/Simulations folder(s) do not exist')
    
    for file in [f for f in os.listdir(simulation_path) if f.endswith('.npy') and os.path.isfile(os.path.join(simulation_path, f))]:
        file_name = Path(file).stem

        folder_path = os.path.join(paper_path, file_name)

        if os.path.exists(folder_path):
            data_files = [f for f in os.listdir(folder_path) if f.endswith('.csv') and os.path.isfile(os.path.join(folder_path, f))]

            for f in data_files:
                plotter(file_name = file_name, orienation = Path(f).stem)