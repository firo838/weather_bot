#!/bin/bash
if [ -e "~/output_log" ]; then
    :
else
    mkdir -p ~/output_log
fi
nohup python run.py > ~/output_log/out.log &