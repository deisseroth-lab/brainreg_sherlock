#!/bin/bash
#SBATCH -t 480
#SBATCH -c 16
#SBATCH -p owners
#SBATCH --mem-per-cpu 8GB
#SBATCH -o ./logs/slurm-%j.out

ml python/3.9 gcc
source ${GROUP_HOME}/projects/registration/brainreg/venv/bin/activate
echo "======"
echo "Params"
echo "$@"
echo "======"
brainreg "$@"
