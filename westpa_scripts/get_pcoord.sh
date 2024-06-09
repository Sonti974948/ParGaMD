#!/bin/bash

if [ -n "$SEG_DEBUG" ] ; then
  set -x
  env | sort
fi

cd $WEST_SIM_ROOT

RMSD=$(mktemp)
RG=$(mktemp)

COMMAND="parm $WEST_SIM_ROOT/common_files/chignolin.prmtop \n"
COMMAND="${COMMAND} trajin $WEST_STRUCT_DATA_REF \n"
COMMAND="${COMMAND} reference $WEST_SIM_ROOT/common_files/chignolin.pdb \n"
COMMAND="${COMMAND} rms ca-rmsd @CA reference out $RMSD mass\n"
COMMAND="${COMMAND} radgyr ca-rg @CA  out $RG mass\n"
COMMAND="${COMMAND} go"

echo -e "${COMMAND}" | $CPPTRAJ

#cat $DIST | tail -n +2 | awk '{print $2}' > $WEST_PCOORD_RETURN
paste <(cat $RMSD | tail -n 1 | awk {'print $2'}) <(cat $RG | tail -n 1 | awk {'print $2'})>$WEST_PCOORD_RETURN
#rm $DIST

if [ -n "$SEG_DEBUG" ] ; then
  head -v $WEST_PCOORD_RETURN
fi
