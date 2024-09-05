#!/bin/bash
#SBATCH -J AMBER_test                   # Job name
#SBATCH -o amber.%j.out            # Name of stdout output file
#SBATCH -e amber.%j.err            # Name of stderr error file
#SBATCH -p rtx                   # Queue (partition) name
#SBATCH -N 1                          # Total # of nodes 
#SBATCH -n 2                          # Total # of mpi tasks 
#SBATCH -t 00:30:00                   # Run time (hh:mm:ss)
#SBATCH -A MCB23037                 # Project/Allocation name

#ml gcc/9.1.0 cuda/11.3

#source /home1/apps/gcc9_1/impi19_0/amber22/amber.sh

set -x
source ~/.bashrc
cd $SLURM_SUBMIT_DIR

export MY_SPECTRUM_OPTIONS="--gpu"
ml purge
module load launcher_gpu/1.1
ml cuda/11.3
export LD_LIBRARY_PATH=/usr/lib64:$LD_LIBRARY_PATH
module load intel/19.1.1
ml impi/19.0.9
module use /scratch1/projects/tacc/csa/benchpro/apps/csa-amaro/amber/modulefiles
ml amber/22_rtx
#module load vmd/1.9.3
#ml hdf5/1.10.4
#conda activate westpa-2.0

export AMBERHOME=${TACC_AMBER_DIR}
echo $AMBERHOME
source $AMBERHOME/amber.sh

export PATH=$AMBERHOME/bin:$PATH

#export PYTHONPATH=/home1/10091/ssonti/miniconda3/envs/westpa-2.0/bin/python
export PYTHONPATH=/scratch1/projects/tacc/csa/benchpro/apps/csa-amaro/amber/amber22_rtx/lib/python3.7/site-packages

pmemd.cuda -O -i md.in -o md.out -p chignolin.prmtop -c chignolin.rst -r md.rst -x md.nc
