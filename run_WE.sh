#!/bin/bash
#
#SBATCH --job-name=mps_check
#SBATCH --account=ahnlab
#SBATCH --partition=gpu-ahn
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1
#SBATCH --time=10:00:00
#SBATCH --output=job.out
#SBATCH --error=job.err

set -x
#export WEST_SIM_ROOT=$PWD
cd $SLURM_SUBMIT_DIR
#cd $WEST_SIM_ROOT
source ~/.bashrc

module load cuda/11.8.0
module load amber/22
module load conda3/4.X
conda activate westpa-2.0
#source env.sh || exit 1
#env | sort

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export WEST_SIM_ROOT=$SLURM_SUBMIT_DIR
cd $WEST_SIM_ROOT
#export PYTHONPATH=/home/ssonti/miniconda3/envs/westpa-2.0/bin/python

#cp cMD/gamd-restart.dat common_files/gamd-restart.dat
#cp cMD/md_cmd.rst bstates/bstate.rst

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
echo$CUDA_VISIBLE_DEVICES
for node in $(cat nodefilelist.txt); do
    bash $PWD/node.sh $SLURM_SUBMIT_DIR $SLURM_JOBID $node $CUDA_VISIBLE_DEVICES --work-manager=zmq --n-workers=$num_gpu_per_node --zmq-mode=client --zmq-read-host-info=$SERVER_INFO --zmq-comm-mode=tcp &
done
wait
