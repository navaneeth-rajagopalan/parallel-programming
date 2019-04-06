#!/bin/bash
#SBATCH --time=00:15:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
module load Python/3.4.3-goolf-2015a
mpirun -np 1 python TwitterAnalysis_Parallel.py
