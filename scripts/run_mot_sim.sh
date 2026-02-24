#!/bin/bash
#BSUB -J mot_sim_100         # Job name
#BSUB -q hpc              # Queue name (change 'normal' to your cluster's specific queue, e.g., 'batch' or 'short')
#BSUB -n 32                  # Number of CPU cores to request
#BSUB -R "span[hosts=1] select[model==XeonGold]"     # IMPORTANT: Forces all cores to be on the SAME node
#BSUB -W 24:00               # Maximum wall time (HH:MM). Here it is 4 hours.
#BSUB -o error/mot_output_%J.txt   # Standard output log (%J is replaced by the Job ID)
#BSUB -e output/mot_error_%J.txt    # Standard error log
#BSUB -M 16GB                # Memory required (adjust as needed)

# Activates the python
source ../.venv/bin/activate

python ../MOT_sims/single_atom_sim.py