import h5py

import numpy as np



simtime = 0.1 # in ns

f = h5py.File('west_now.h5','r')

total_simtime = np.sum(f['summary']['n_particles'])*simtime

total_walltime = np.sum(f['summary']['walltime'])/3600.0 # in hours

speed=total_simtime/total_walltime

print('total simtime = '+str(total_simtime)+' nanoseconds')

print('total walltime = '+str(total_walltime)+' hours')

print('Speed = %.2f ns/hr = %.2f ns/day'%(speed,speed*24))

print(f['summary']['walltime'])
print(f['summary']['n_particles'])
