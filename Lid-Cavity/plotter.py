import os
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from itertools import cycle
from matplotlib.lines import Line2D

x_labels = {}
y_labels = {}

def load_curve_from_paper(paper_path, file_name, orientation, nx, ny):
    csv_path = os.path.join(paper_path, file_name, f'{orientation}.csv')
    
    if not os.path.exists(csv_path):
        return None, None
    
    df = pd.read_csv(csv_path, header=None)
    x_paper = df[0] / (nx if orientation == 'x' else 1)
    y_paper = df[1] / (1 if orientation == 'x' else ny)
    return np.asarray(x_paper), np.asarray(y_paper)

def sim_curve(u, v, u0, nx, ny, orientation):
    if orientation == 'x':
        x_sim = np.arange(nx) / nx
        y_sim = v[:, ny // 2] / u0
    else:
        x_sim = u[nx // 2, :] / u0
        y_sim = np.arange(ny) / ny
    return x_sim, y_sim

def add_curve_to_axes(ax, x, y, orientation, style, color):
    if style == 'paper':
        ax.plot(x, y, marker='o', linestyle='none', color=color)
    else:
        ax.plot(x, y, linestyle='-', color=color)

    if orientation == 'x':
        ax.set_xlim(0, 1)
        ax.set_xlabel('x/X')
        ax.set_ylabel('v/U')
    else:
        ax.set_ylim(0, 1)
        ax.set_xlabel('u/U')
        ax.set_ylabel('y/Y')

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')

    origin_path     = os.getcwd()
    paper_path      = os.path.join(origin_path, 'paper')
    simulation_path = os.path.join(origin_path, 'simulations')
    results_path    = os.path.join(origin_path, 'results')
    combine_path    = os.path.join(results_path, 'combine')

    if not os.path.exists(paper_path) or not os.path.exists(simulation_path):
        raise FileExistsError('Paper/Simulations folder(s) do not exist')

    os.makedirs(results_path, exist_ok = True)
    os.makedirs(combine_path, exist_ok = True)

    combined_x_curves = []
    combined_y_curves = []

    color_cycle = cycle(plt.cm.tab10.colors)
    reynolds_colors = {}

    for file in [f for f in os.listdir(simulation_path)
                 if f.endswith('.npy') and os.path.isfile(os.path.join(simulation_path, f))]:
        file_name = Path(file).stem
        reynolds_key = ''.join([c for c in file_name if c.isdigit()])
        
        if reynolds_key not in reynolds_colors:
            reynolds_colors[reynolds_key] = next(color_cycle)

        data = np.load(os.path.join(simulation_path, file), allow_pickle = True).item()
        
        u0 = data['meta']['u0']
        u = data['u'][1:-1, 1:-1]
        v = data['v'][1:-1, 1:-1]
        
        nx, ny = u.shape

        for orientation in ('x', 'y'):
            xp, yp = load_curve_from_paper(paper_path, file_name, orientation, nx, ny)
        
            if xp is None:
                continue
        
            xs, ys = sim_curve(u, v, u0, nx, ny, orientation)
            color = reynolds_colors[reynolds_key]

            if orientation == 'x':
                combined_x_curves.append((xp, yp, 'paper', color))
                combined_x_curves.append((xs, ys, 'simulation', color))
            else:
                combined_y_curves.append((xp, yp, 'paper', color))
                combined_y_curves.append((xs, ys, 'simulation', color))

    def plot_combined(curves, orientation, out_name):
        fig, ax = plt.subplots(figsize=(9, 6))

        for x, y, style, color in curves:
            add_curve_to_axes(ax, x, y, orientation, style, color)

        style_legend = [
            Line2D([0], [0], marker = 'o', color = 'black', linestyle = 'none', label = 'Paper'),
            Line2D([0], [0], color = 'black', linestyle = '-', label = 'Simulation')
        ]

        reynolds_legend = [
            Line2D([0], [0], color = color, linestyle = '-', label = f'Re{re}')
            for re, color in reynolds_colors.items()
        ]

        legend1 = ax.legend(handles = style_legend, loc = f'{'lower' if orientation == 'x' else 'upper'} left', title = 'Type')
        legend2 = ax.legend(handles = reynolds_legend, loc = f'{'lower' if orientation != 'x' else 'upper'} right', title = 'Reynolds')
        ax.add_artist(legend1)

        ax.set_title(f'Combined {'Horizontal' if orientation == 'x' else 'Vertical'} Profiles')
        plt.savefig(os.path.join(combine_path, out_name), bbox_inches = 'tight', dpi = 250)
        plt.close(fig)

    if combined_x_curves:
        plot_combined(combined_x_curves, 'x', 'x.png')

    if combined_y_curves:
        plot_combined(combined_y_curves, 'y', 'y.png')
