#!/usr/bin/env python3

import os
import subprocess
from pathlib import Path
from os.path import basename, dirname

scratch = Path(os.environ["SCRATCH"])
oak = Path(os.environ["OAK"])

dir_data = scratch / "tamachad" / "data"
dir_output = oak / "users" / "croat" / "tamachad" / "output"

atlas_steps_list = [
    (100, 4),
    (50, 5),
    (25, 6),
    (10, 7),
]
bending_energy_list = [0.7, 0.85, 0.95, 1]
grid_spacing_list = [-5, -10, -20]
sigma_list = [0, -1, -4]
hist_bins_list = [64, 128, 256]

for at, st in atlas_steps_list:
    for tiff in dir_data.glob(f"*/Ex_488_Em_525_stitched.br.{at}um.tif"):
        dataset, base = tiff.parts[-2:]
        for be in bending_energy_list:
            for gs in grid_spacing_list:
                for si in sigma_list:
                    for hb in hist_bins_list:
                        name = f"at{at}_st{st}_be{be}_gs{gs}_si{si}_hb{hb}"
                        output = dir_output / dataset / base / name
                        if output.exists():
                            continue
                        output.mkdir(parents=True, exist_ok=True)
                        command = [
                            "sbatch",
                            "brainreg.sh",
                            tiff,
                            output,
                            "-v", str(at), str(at), str(at),
                            "--orientation", "ial",
                            "--save-original-orientation",
                            "--debug",
                            "--n-free-cpus", "1",
                            "--atlas", f"allen_mouse_{at}um",
                            "--affine-n-steps", st,
                            "--affine-use-n-steps", st,
                            "--freeform-n-steps", st,
                            "--freeform-use-n-steps", st,
                            "--bending-energy-weight", be,
                            "--grid-spacing", gs,
                            "--smoothing-sigma-reference", si,
                            "--smoothing-sigma-floating", si,
                            "--histogram-n-bins-reference", hb,
                            "--histogram-n-bins-floating", hb,
                        ]
                        subprocess.run([str(c) for c in command], check=True)
