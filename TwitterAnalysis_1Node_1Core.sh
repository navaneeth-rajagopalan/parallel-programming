#!/bin/bash
#SBATCH --time=00:01:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
module load Python/3.4.3-goolf-2015a
mpirun -np 1 python TwitterAnalysis_Parallel.py
