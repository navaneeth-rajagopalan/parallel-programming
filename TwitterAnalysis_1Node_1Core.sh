#!/bin/bash
#SBATCH --time=00:20:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
module load Python/3.4.3-goolf-2015a
time mpirun -np 1 python TwitterAnalysis_Parallel.py
