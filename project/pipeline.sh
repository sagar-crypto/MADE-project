#!/bin/bash


if [[ -x "install-dependencies.sh" ]]
then
    echo "File is executable"
else
    chmod +x install-dependencies.sh
fi

./install-dependencies.sh

# download and process data 
python python dataProcessing.py

# visualize data 
python analysis_visualization.py
