# brainreg_sherlock

Some simple applications to run brainreg on Stanford's Sherlock SLURM cluster.

1. The `data_sync` utility copies files to scratch space for faster data
   access.  This runs commands from `mpifileutils`.

2. The `downsample` utility downsamples the input data to 10/25/50um for
   registration to atlases at those resolutions.  The `brainreg` app
   can do downsampling, but it is more efficient to do it once up front
   if `brainreg` is being called many times.  This is a python utility
   that mimicks what `brainreg` does for downsampling.

3. The `brainreg` utility runs registration with a given set of
   parameters.  It is run from a virtual environment housed in
   `GROUP_HOME`.

The files with `_launch` in their name are the top-level programs to
run many `sbatch` commands, each of which starts a SLURM job.  These
can be modified for the location of your data. The actual `sbatch`
scripts with the command lines are the `{app}.sh` files.
