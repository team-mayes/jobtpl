#!/bin/bash

for job in `ls *.job`; do
	qsub $job
	rm $job
done