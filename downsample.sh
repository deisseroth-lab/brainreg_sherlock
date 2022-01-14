#!/bin/bash
#SBATCH -c 16
#SBATCH -p owners
#SBATCH --mem-per-cpu 8GB
#SBATCH -o ./logs/slurm-%a.out

ml python/3.9
source ${GROUP_HOME}/projects/registration/brainreg/venv/bin/activate
python downsample.py "$@"
