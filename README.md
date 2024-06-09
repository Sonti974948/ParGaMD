# Parallelizable Gaussian Accelerated Molecular Dynamics (ParGaMD)
ParGaMD is a hybrid method that leverages the accelerated sampling of Gaussian Accelerated Molecular Dynamics (GaMD) and marries it with the excellent parallelization of the Weighted Ensemble (WE) framework, resulting in a powerful method that can speed up protein simulations. 

Please follow the given steps in order to successfully perform a ParGaMD simulation: 
1. Perform a conventional Molecular Dynamics (cMD) simulation to get the GaMD paramters (gamd-restart.dat)
2. Store the .prmtop, .pdb and the gamd-restart.dat files in the common_files directory, and save the final trajectory of the cMD as bstate.rst
3. Make sure that pcoord_len in west.cfg = nstlim/ntpr + 1 (nstlim, ntpr are in common_files/md.in) 
4. Run the ParGaMD simulation using run.sh as the submission script. (Please change the NODELOC in env.sh to the directory from where you're running the simulations)
5. After running the simulation, run the postprocessing to get the gamd.log and PC.dat (PC --> progress coordinate) files using run_data.sh (NOTE: Please submit run_data.sh on to the compute node and not on the login node as there may be memory allocation issues).
6. For reweighting to get the free energy surface (FES):
   1. Get weights.dat from gamd.log using the command {awk 'NR%1==0' gamd.log | awk '{print ($8+$7)/(0.001987*300)" " $2 " " ($8+$7)}' > weights.dat}
   2. Get output.dat from PC1.dat and PC2.dat (If using 2 PCs for a 2D surface) using the command {awk 'NR==FNR{a[NR]=$2; next} {print a[FNR], $2}' PC1.dat PC2.dat > output.dat}
   3. Run the command {./reweight-2d.sh 50 50 0.1 0.1  output.dat 300}, where 50 50 are the cutoffs for both PCs, 0.1 0.1 are the bin spacings for the PCs, and 300 is 300 K. 


