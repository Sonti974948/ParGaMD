import os 
import numpy as np


path='/expanse/lustre/scratch/ssonti/temp_project/amber_learn/chignolin_tutorial/westpa_tutorials/tutorial7.3-chignolin/ParGaMD_finer'
os.chdir(path)

iters=len(next(os.walk('traj_segs'))[1])
iter_iters=[]
print(iters)
os.chdir('traj_segs')

for i in range(iters):

    #os.chdir('C:\\Users\\svdnr\\Desktop\\test1\\traj_segs')

    iters_sub=len(next(os.walk('0000{:02d}'.format(i+1)))[1])

    iter_iters.append(iters_sub)
print(iter_iters)
gamd_all=[]
rmsd_all=[]
rg_all=[]
#os.chdir(path)

for i in range(iters):
    os.chdir(path)
    os.chdir('traj_segs/00{:04d}'.format(i+1))

    for j in range(iter_iters[i]):

        try:
            os.chdir(path)
            os.chdir('traj_segs/00{:04d}/00{:04d}'.format(i+1,j))

            gamd=np.genfromtxt('gamd.log')
            rmsd=np.genfromtxt('rmsd.dat')
            rg=np.genfromtxt('rg.dat')
            gamd_all.append(gamd)
            rmsd_all.append(np.delete(rmsd,0,0))
            rg_all.append(np.delete(rg,0,0))
            #os.chdir(path)

            print(j)

            print(j,i)

        except:

            continue

dims1=np.shape(gamd_all)
print(dims1)
dims2=np.shape(rmsd_all)
dims3=np.shape(rg_all)

gamd_write=np.reshape(gamd_all,(dims1[0]*dims1[1],dims1[2]))
rmsd_write=np.reshape(rmsd_all,(dims2[0]*dims2[1],dims2[2]))
rg_write=np.reshape(rg_all,(dims3[0]*dims3[1],dims3[2]))

os.chdir(path)
log_gamd=np.savetxt('gamd.log',gamd_write)
log_rmsd=np.savetxt('rmsd.dat',rmsd_write)
log_rg=np.savetxt('rg.dat',rg_write)
