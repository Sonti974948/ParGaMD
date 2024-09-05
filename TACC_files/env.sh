#!/bin/bash


source ~/.profile
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
conda init
conda activate westpa-2.0



#export PATH=$PATH:$HOME/bin
export PYTHONPATH=/home1/10091/ssonti/miniconda3/envs/westpa-2.0/bin/python:/scratch1/projects/tacc/csa/benchpro/apps/csa-amaro/amber/amber22_rtx/lib/python3.7/site-packages

#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH

# Explicitly name our simulation root directory
if [[ -z "$WEST_SIM_ROOT" ]]; then
    export WEST_SIM_ROOT="$PWD"
fi

export SIM_NAME=$(basename $WEST_SIM_ROOT)
echo "simulation $SIM_NAME root is $WEST_SIM_ROOT"


# Set up environment for dynamics
export AMBERHOME=${TACC_AMBER_DIR}
source $AMBERHOME/amber.sh
export PATH=$AMBERHOME/bin:$PATH



# Set runtime commands (this is said to be easier on the filesystem)
export NODELOC=/scratch1/10091/ssonti/ParGaMD
export USE_LOCAL_SCRATCH=1

export WM_ZMQ_MASTER_HEARTBEAT=100
export WM_ZMQ_WORKER_HEARTBEAT=100
export WM_ZMQ_TIMEOUT_FACTOR=300
export BASH=$SWROOT/bin/bash
export PERL=$SWROOT/usr/bin/perl
export ZSH=$SWROOT/bin/zsh
export IFCONFIG=$SWROOT/bin/ifconfig
export CUT=$SWROOT/usr/bin/cut
export TR=$SWROOT/usr/bin/tr
export LN=$SWROOT/bin/ln
export CP=$SWROOT/bin/cp
export RM=$SWROOT/bin/rm
export SED=$SWROOT/bin/sed
export CAT=$SWROOT/bin/cat
export HEAD=$SWROOT/bin/head
export TAR=$SWROOT/bin/tar
export AWK=$SWROOT/usr/bin/awk
export PASTE=$SWROOT/usr/bin/paste
export GREP=$SWROOT/bin/grep
export SORT=$SWROOT/usr/bin/sort
export UNIQ=$SWROOT/usr/bin/uniq
export HEAD=$SWROOT/usr/bin/head
export MKDIR=$SWROOT/bin/mkdir
export ECHO=$SWROOT/bin/echo
export DATE=$SWROOT/bin/date
export SANDER=$AMBERHOME/bin/sander
export PMEMD=$AMBERHOME/bin/pmemd.cuda
export CPPTRAJ=$AMBERHOME/bin/cpptraj
