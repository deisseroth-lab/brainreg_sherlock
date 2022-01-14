#!/bin/bash

dir_oak="$OAK/users/tamachad"
dir_scratch="$SCRATCH/tamachad/data"

for dir_oak_full in $(ls -d "${dir_oak}"/*/*stitched*); do
    echo "Submitting: ${dir_oak_full}"
    subdir_wavelength=$(basename "${dir_oak_full}")
    subdir_dataset=$(basename $(dirname "${dir_oak_full}"))

    dir_scratch_full="${dir_scratch}/${subdir_dataset}/${subdir_wavelength}"
    sbatch data_sync.sh "${dir_oak_full}" "${dir_scratch_full}"
done
