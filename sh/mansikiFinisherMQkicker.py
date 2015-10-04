#!/usr/bin/python
# coding: UTF-8

import sys
sys.path.insert(1, '/usr/lib/gimp/2.0/python')
sys.path.insert(1, '/home/alfx61/.gimp-2.8/plug-ins')
from gimpfu import *
sys.path=[".",".."]+sys.path

import mansikiFinisherMQBatch
image=None
drowable=None
target="/home/alfx61/画像/4prints/test"
works="/home/alfx61/tmp"
dpi=600
size="B5"
frontPrefix="Front_"
mainPrefix="Main_"
rearPrefix="Rear_"
finalPrefix="U_"
direction=True
isCut=True
padding=2.64
numWorkerThreads=2
mansikiFinisherMQBatch.run(image, drowable, target, works, dpi, size, frontPrefix, mainPrefix, rearPrefix,finalPrefix, direction, isCut, padding, numWorkerThreads)
gimpfu.pdb.gimp_quit(1)
