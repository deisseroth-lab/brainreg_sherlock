#!/bin/bash
#SBATCH -n 4
#SBATCH -p owners
#SBATCH -o ./logs/slurm-%a.out

ml system mpifileutils
srun dsync "$@"
