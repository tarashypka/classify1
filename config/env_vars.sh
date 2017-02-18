#!/bin/sh

# conda env create --file=./config/ENVIRONMENT
# mkdir -p $ENVPATH/conda/activate.d
# cp env_vars $ENVPATH/etc/conda/activate.d

export PROJNAME=classify1
export ENVPATH=$ANACONDA_HOME/envs/$PROJNAME
export PROJPATH=$HOME/Workspace/python/$PROJNAME
export PYTHONPATH=$ENVPATH/bin:$PROJPATH/src
