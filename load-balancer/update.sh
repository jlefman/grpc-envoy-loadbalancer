#!/bin/bash
cd /source/democontroller
PYTHONPATH=$PYTHONPATH:$PWD python3 controller.py
if [ -e /config/new.yaml ]; then
   echo updating eds config
   cd /config
   mv new.yaml eds.yaml
fi
