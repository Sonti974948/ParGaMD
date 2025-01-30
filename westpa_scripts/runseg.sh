#!/bin/bash

if [ -n "$SEG_DEBUG" ] ; then
  set -x
  env | sort
fi

cd $WEST_SIM_ROOT
mkdir -pv $WEST_CURRENT_SEG_DATA_REF
cd $WEST_CURRENT_SEG_DATA_REF

ln -sv $WEST_SIM_ROOT/common_files/system_final.prmtop .
ln -sv $WEST_SIM_ROOT/common_files/system_final.inpcrd .
ln -sv $WEST_SIM_ROOT/common_files/gamd-restart.dat .

if [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_CONTINUES" ]; then
  sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/prod.in > md.in
  ln -sv $WEST_PARENT_DATA_REF/seg.rst ./parent.rst
elif [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_NEWTRAJ" ]; then
  sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/prod.in > md.in
  ln -sv $WEST_PARENT_DATA_REF ./parent.rst
fi

#export CUDA_DEVICES=(`echo $CUDA_VISIBLE_DEVICES_ALLOCATED | tr , ' '`)
#export CUDA_VISIBLE_DEVICES=${CUDA_DEVICES[$WM_PROCESS_INDEX]}

#echo "RUNSEG.SH: CUDA_VISIBLE_DEVICES_ALLOCATED = " $CUDA_VISIBLE_DEVICES_ALLOCATED
#echo "RUNSEG.SH: WM_PROCESS_INDEX = " $WM_PROCESS_INDEX
#echo "RUNSEG.SH: CUDA_VISIBLE_DEVICES = " $CUDA_VISIBLE_DEVICES

while ! grep -q "Final Performance Info" seg.log; do
	$PMEMD -O -i md.in   -p system_final.prmtop  -c parent.rst \
          -r seg.rst -x seg.nc      -o seg.log    -inf seg.nfo -gamd gamd.log
done

RMSD=rmsd.dat
RG=rg.dat
COMMAND="         parm system_final.prmtop\n"
COMMAND="${COMMAND} trajin $WEST_CURRENT_SEG_DATA_REF/parent.rst\n"
COMMAND="${COMMAND} trajin $WEST_CURRENT_SEG_DATA_REF/seg.nc\n"
COMMAND="${COMMAND} reference $WEST_SIM_ROOT/common_files/system_final.inpcrd\n"
COMMAND="${COMMAND} rms ca-rmsd @CA reference out $RMSD mass\n"
COMMAND="${COMMAND} radgyr ca-rg @CA  out $RG  mass\n"
COMMAND="${COMMAND} go\n"

echo -e $COMMAND | $CPPTRAJ
#cat $RMSD > rmsd.dat
#cat $RG > rg.dat
paste <(cat rmsd.dat | tail -n +2 | awk {'print $2'}) <(cat rg.dat | tail -n +2 | awk {'print $2'})>$WEST_PCOORD_RETURN
#cat $TEMP | tail -n +2 | awk '{print $2}' > $WEST_PCOORD_RETURN
#paste <(cat $TEMP | tail -n 1 | awk {'print $2'}) <(cat $RG | tail -n 1 | awk {'print $2'})>$WEST_PCOORD_RETURN
#cat $TEMP >pcoord.dat
# Clean up
rm -f $TEMP md.in seg.nfo seg.pdb
