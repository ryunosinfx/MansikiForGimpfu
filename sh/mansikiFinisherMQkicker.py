#!/usr/bin/python
# coding: UTF-8

import sys
sys.path.insert(1, '/usr/lib/gimp/2.0/python')
first = sys.path[0]
curdir = first + "/../" # カレントディレクトリ名を取得
print "curdir:" + curdir
sys.path.insert(1, curdir)
from gimpfu import *
sys.path=[".",".."]+sys.path

import json
import mansikiFinisherMQBatch
f = open('mansikiFinisherSetting.json', 'r')
jsonData = json.load(f)
image=None
drowable=None
###############################################
target = jsonData["target"]
works = jsonData["works"]
dpi = int(jsonData["dpi"])
size = jsonData["size"]
frontPrefix = jsonData["frontPrefix"]
mainPrefix = jsonData["mainPrefix"]
rearPrefix = jsonData["rearPrefix"]
finalPrefix = jsonData["finalPrefix"]
direction= False if "False".lower() == jsonData["direction"].lower() else True
isCut= False if "False".lower() == jsonData["isCut"].lower() else True
padding=float(jsonData["padding"])
numWorkerThreads=int(jsonData["numWorkerThreads"])
###############################################
mansikiFinisherMQBatch.run(image, drowable, target, works, dpi, size, frontPrefix, mainPrefix, rearPrefix,finalPrefix, direction, isCut, padding, numWorkerThreads)
gimpfu.pdb.gimp_quit(1)
