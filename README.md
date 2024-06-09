# Parallelizable Gaussian Accelerated Molecular Dynamics (ParGaMD)
ParGaMD is a hybrid method that leverages the accelerated sampling of Gaussian Accelerated Molecular Dynamics (GaMD) and marries it with the excellent parallelization of the Weighted Ensemble (WE) framework, resulting in a powerful method that can speed up protein simulations. 

Please follow the given steps in order to successfully perform a ParGaMD simulation: 
1. Perform a conventional Molecular Dynamics (cMD) simulation to get the GaMD paramters (gamd-restart.dat)
2. Store the .prmtop, .pdb and the gamd-restart.dat files in the common_files directory, and save the final trajectory of the cMD as bstate.rst
3. Make sure that pcoord_len in west.cfg = nstlim/ntpr + 1 (nstlim, ntpr are in common_files/md.in) 
4. Run the ParGaMD simulation (Please change the NODELOC in env.sh to the directory from where you're running the simulations)
5. After running the simulation


