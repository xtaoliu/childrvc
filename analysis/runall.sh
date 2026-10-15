#!/bin/bash
cd /home/user/childrvc/analysis
for s in m1 m2 prod lopo freq; do Rscript models.R $s > out/log_$s.txt 2>&1; done
echo done > out/ALLDONE
