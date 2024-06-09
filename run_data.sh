#!/bin/bash
#SBATCH --job-name="chignolin_WE_run"
#SBATCH --output="job.out"
#SBATCH --partition=gpu-shared
#SBATCH --nodes=1
#SBATCH --gpus=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=50G
#SBATCH --account=ucd187
#SBATCH --no-requeue
#SBATCH --mail-user=ssiddharth@ucdavis.edu
#SBATCH --mail-type=ALL
#SBATCH -t 48:00:00



set -x
#export WEST_SIM_ROOT=$PWD
#cd $SLURM_SUBMIT_DIR
#cd $WEST_SIM_ROOT
source ~/.bashrc
module purge
module load shared
module load gpu/0.15.4
module load slurm
module load openmpi/4.0.4
module load cuda/11.0.2
module load amber/20-patch15
#module load conda
#conda activate westpa-2.0
#source env.sh || exit 1
#env | sort

#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
#export WEST_SIM_ROOT=$SLURM_SUBMIT_DIR
#cd $WEST_SIM_ROOT
export PYTHONPATH=/home/ssonti/miniconda3/bin/python
#./init.sh
#source env.sh || exit 1
#env | sort
#SERVER_INFO=$WEST_SIM_ROOT/west_zmq_info.json

#TODO: set num_gpu_per_node
#num_gpu_per_node=4
#rm -rf nodefilelist.txt
#scontrol show hostname $SLURM_JOB_NODELIST > nodefilelist.txt

# start server
#w_truncate -n 11
#rm -rf traj_segs/000011
#rm -rf seg_logs/000011*
python3 data_extract.py
