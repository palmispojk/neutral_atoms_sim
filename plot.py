import pickle
import glob
import numpy as np
import matplotlib.pyplot as plt
import MOT_sims.constants as constants


all_results = []

for file_path in glob.glob("mot_simulation_data.pkl"):
    with open(file_path, 'rb') as f:
        node_results = pickle.load(f)
        all_results.extend(node_results) 

print(f"Successfully loaded data for {len(all_results)} atoms!")

final_x, final_y, final_z = [], [], []
unit_to_mm = (1/ constants.kmag_real) * 1000 # to millimeters

for atom in all_results:
    t, r, v = atom  # Unpack the time, position, and velocity arrays
    
    # 'r' is a 3D array where r[0] is X, r[1] is Y, r[2] is Z
    final_x.append(r[0, -1] * unit_to_mm)
    final_y.append(r[1, -1] * unit_to_mm)
    final_z.append(r[2, -1] * unit_to_mm)


fig, ax = plt.subplots(figsize=(7, 7))

ax.scatter(final_x, final_y, color='royalblue', s=12, alpha=0.4)
ax.scatter([0], [0], color='red', marker='+', s=200, label='Trap Center')

ax.set_xlabel('X position (mm)')
ax.set_ylabel('Y position (mm)')
ax.set_title('Strontium-88 MOT Cloud (Real Scale)')
ax.set_aspect('equal')
ax.grid(True, linestyle=':', alpha=0.6)

plt.legend()

plt.savefig('mot_cloud_2d_xy.png', dpi=300, bbox_inches='tight')


# -----------
fig, ax = plt.subplots(3, 2, figsize=(6.25, 5.5))


for atom in all_results:
    t, r, v = atom  # Unpack the time, position, and velocity arrays for this specific atom
    
    for ii in range(3):
        # Left column (0): Plot Velocity vs Time
        ax[ii, 0].plot(t / 1e3, v[ii], linewidth=0.25, color='blue', alpha=0.3)
        
        # Right column (1): Plot Position vs Time
        ax[ii, 1].plot(t / 1e3, r[ii] * constants.alpha, linewidth=0.25, color='red', alpha=0.3)

for ax_i in ax[-1, :]:
    ax_i.set_xlabel(r'$10^3 \Gamma t$')

# Hide the x-tick numbers for the top and middle rows
for jj in range(2):
    for ax_i in ax[jj, :]:
        ax_i.set_xticklabels([])

for ax_i, lbl in zip(ax[:, 0], ['x', 'y', 'z']):
    ax_i.set_ylabel(r'$v_' + lbl + '/(\Gamma/k)$')

for ax_i, lbl in zip(ax[:, 1], ['x', 'y', 'z']):
    ax_i.set_ylabel(r'$\alpha ' + lbl + '$')

fig.subplots_adjust(left=0.1, bottom=0.08, wspace=0.3)

plt.savefig('mot_3x2_trajectories.png', dpi=300, bbox_inches='tight')