#!/bin/bash
#SBATCH -J AMBER_test                   # Job name
#SBATCH -o job.out            # Name of stdout output file
#SBATCH -e job.err            # Name of stderr error file
#SBATCH -p rtx                   # Queue (partition) name
#SBATCH -N 1                          # Total # of nodes 
#SBATCH -n 1                         # Total # of mpi tasks 
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
conda init
conda activate westpa-2.0

export AMBERHOME=${TACC_AMBER_DIR}
echo $AMBERHOME
source $AMBERHOME/amber.sh

export PATH=$AMBERHOME/bin:$PATH

export WEST_SIM_ROOT=$SLURM_SUBMIT_DIR
cd $WEST_SIM_ROOT
export PYTHONPATH=/home1/10091/ssonti/miniconda3/envs/westpa-2.0/bin/python:/scratch1/projects/tacc/csa/benchpro/apps/csa-amaro/amber/amber22_rtx/lib/python3.7/site-packages

#pmemd.cuda -O -i md.in -o md.out -p chignolin.prmtop -c chignolin.rst -r md.rst -x md.nc

cp cMD/gamd-restart.dat common_files/gamd-restart.dat
cp cMD/md.rst bstates/bstate.rst
echo "Files copied"

./init.sh
echo "init.sh ran"
source env.sh || exit 1
env | sort
SERVER_INFO=$WEST_SIM_ROOT/west_zmq_info.json

#TODO: set num_gpu_per_node
num_gpu_per_node=1
rm -rf nodefilelist.txt
scontrol show hostname $SLURM_JOB_NODELIST > nodefilelist.txt

# start server
#w_truncate -n 11
#rm -rf traj_segs/000011
#rm -rf seg_logs/000011*
w_run --work-manager=zmq --n-workers=0 --zmq-mode=master --zmq-write-host-info=$SERVER_INFO --zmq-comm-mode=tcp &> west-$SLURM_JOBID-local.log &

# wait on host info file up to 1 min
for ((n=0; n<60; n++)); do
    if [ -e $SERVER_INFO ] ; then
        echo "== server info file $SERVER_INFO =="
        cat $SERVER_INFO
        break
    fi
    sleep 1
done

# exit if host info file doesn't appear in one minute
if ! [ -e $SERVER_INFO ] ; then
    echo 'server failed to start'
    exit 1
fi
export CUDA_VISIBLE_DEVICES=0
echo $CUDA_VISIBLE_DEVICES
for node in $(cat nodefilelist.txt); do
    ssh -o StrictHostKeyChecking=no $node $PWD/node.sh $SLURM_SUBMIT_DIR $SLURM_JOBID $node $CUDA_VISIBLE_DEVICES --work-manager=zmq --n-workers=$num_gpu_per_node --zmq-mode=client --zmq-read-host-info=$SERVER_INFO --zmq-comm-mode=tcp &
done
wait


