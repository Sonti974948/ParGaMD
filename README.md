# Parallelizable Gaussian Accelerated Molecular Dynamics (ParGaMD)
ParGaMD is a hybrid method that leverages the accelerated sampling of Gaussian Accelerated Molecular Dynamics (GaMD) and marries it with the excellent parallelization of the Weighted Ensemble (WE) framework, resulting in a powerful method that can speed up protein simulations. 

Please follow the given steps in order to successfully perform a ParGaMD simulation: 
1. Perform a conventional Gaussian Accelarated Molecular Dynamics (cGaMD) simulation in the ````cMD```` folder by running ````sbatch run_cmd.sh```` to get the GaMD paramters (````gamd-restart.dat````)
2. The ````run_WE.sh```` in the main directory takes care of copying ````gamd-restart.dat```` and ````bstate.rst```` into the required directories in the WE framework.
3. Make sure that ````pcoord_len = nstlim/ntpr + 1```` in west.cfg (nstlim, ntpr are in common_files/md.in).
4. Run the command ````squeue -u username```` to copy the job ID of the cGaMD simulation. This job ID will be used in the next step. 
5. Run the ParGaMD simulation as a dependancy job by running the command ````sbatch --dependency=afterok:jobid run_WE.sh```` . (Please change the ````NODELOC```` in env.sh to the directory from where you're running the simulations)
6. After running the simulation, run the postprocessing to get the ````gamd.log and PC.dat```` (PC --> progress coordinate) files using ````run_data.sh```` (NOTE: Please submit ````run_data.sh```` on to the compute node and not on the login node as there may be memory allocation issues).
7. For reweighting to get the free energy surface (FES):
   1. Get weights.dat from gamd.log using the command ````awk 'NR%1==0' gamd.log | awk '{print ($8+$7)/(0.001987*300)" " $2 " " ($8+$7)}' > weights.dat````
   2. Get output.dat from PC1.dat and PC2.dat (If using 2 PCs for a 2D surface) using the command ````awk 'NR==FNR{a[NR]=$2; next} {print a[FNR], $2}' PC1.dat PC2.dat > output.dat````
   3. Run the command ````./reweight-2d.sh 50 50 0.1 0.1  output.dat 300````, where 50 50 are the cutoffs for both PCs, 0.1 0.1 are the bin spacings for the PCs, and 300 is 300 K. 


