#!/bin/bash
#SBATCH --time=00:20:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
module load Python/3.4.3-goolf-2015a
time mpirun -np 8 python TwitterAnalysis_Parallel.py
