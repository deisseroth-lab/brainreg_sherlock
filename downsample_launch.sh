#!/bin/bash

dir_scratch="$SCRATCH/tamachad/data"

for res_out in 10; do
#for res_out in 10 25 100; do
    # VGAT brains are DISCO and have z-spacing of 4um
#    for dir_in in $(ls -d "${dir_scratch}"/*vgat*/Ex_488_Em_525_stitched); do
#	sbatch downsample.sh --dir "${dir_in}" --res_in 4 1.794 1.794 --res_out ${res_out}
#    done

    # MCHERRY brains are SHIELD and have z-spacing of 4um
    for dir_in in $(ls -d "${dir_scratch}"/*mcherry*/Ex_488_Em_525_stitched); do
	sbatch downsample.sh --dir "${dir_in}" --res_in 2 1.794 1.794 --res_out ${res_out}
    done
done
