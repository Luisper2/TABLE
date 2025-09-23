'''
    volume fraction
        f = 2 * pi * r ^ 2 / L ^ 2

        for r = 0.125 * L -> f = pi / 32 ~ 9.82%
    
    porosity = 1 - f (volume fraction)
        for r = 0.125 * L -> 1 - pi / 32
'''

import os
import jax.numpy as jnp
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

os.system('clear')

sides = (10 ** jnp.arange(2, 3.8, 0.1)).astype(int)
porosity = []

aim = 100 * (1 - (jnp.pi / 32))

for l in sides:
    radius = 0.125 * l

    x = jnp.arange(l)
    y = jnp.arange(l)

    X, Y = jnp.meshgrid(x, y, indexing='ij')

    centers = [
        (0, 0),
        (l, 0),
        (l / 2, l / 2),
        (0, l),
        (l, l)
    ]

    mask = jnp.zeros((l, l), dtype=bool)

    for cx, cy in centers:
        dist = (X - cx)**2 + (Y - cy)**2
        mask = jnp.logical_or(mask, dist <= radius**2)

    porosity.append(100 * (1 - jnp.sum(mask) / mask.size))

plt.plot(sides, porosity, 'k')
plt.plot(sides, porosity, 'ko')
plt.axhline(aim, color = 'k', linestyle = '--')
plt.xscale('log')
plt.xlabel('Side length (voxels)')
plt.ylabel('Porosity (%)')
plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
plt.grid(True)
plt.savefig('Voxels.png')