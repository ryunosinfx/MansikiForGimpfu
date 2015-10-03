#!/bin/bash

image='None'
drowable='None'
target='"'$HOME'/画像/4prints/test"'
works='"'$HOME'/tmp"'
dpi='600'
size='"B5"'
frontPrefix='"Front_"'
mainPrefix='"Main_"'
rearPrefix='"Rear_"'
finalPrefix='"U_"'
direction='True'
isCut='True'
padding='2.64'
numWorkerThreads='2'
gimpfuKicker='import sys; sys.path.insert(1, '/usr/lib/gimp/2.0/python');import gimpfu;print "aaaaa"+sys.path;gimpfu.pdb.mansiki_build_images_for_mq_copyprint('${image}', '${drowable}', '${target}','${works}','${dpi}','${size}','${frontPrefix}','${mainPrefix}','${rearPrefix}','${finalPrefix}','${direction}','${isCut}','${padding}','${numWorkerThreads}')'
gimpfuTerminate='pdb.gimp_quit(1)'
pwd
cd /home/alfx61/.gimp-2.8/sh
gimpfuKicker="import sys; sys.path.insert(1, \"/usr/lib/gimp/2.0/python\");import gimpfu;print \"aaaaa\"+sys.path;"
gimpfuKicker="print \"aaaaa\""
gimpfuKicker='pdb.mansiki_build_images_for_mq_copyprint()'
#'${image}', '${drowable}', '${target}','${works}','${dpi}','${size}','${frontPrefix}','${mainPrefix}','${rearPrefix}','${finalPrefix}','${direction}','${isCut}','${padding}','${numWorkerThreads}')'

#echo "#!/usr/bin/python" > ./execute.py
#echo "# coding: UTF-8" >> ./execute.py
#echo ${gimpfuKicker} >> ./execute.py
#cat ./execute.py
echo ${gimpfuKicker}
pwd
ls -la ./mansikiFinisherMQkicker.py
#gimp --no-interface --console-messages --no-data --no-splash --batch-interpreter --verbose python-fu-eval -b ${gimpfuKicker} -b ${gimpfuTerminate}
#gimp -idf  --console-messages --no-data --no-splash --batch-interpreter python-fu-eval -b ${gimpfuKicker} -b ${gimpfuTerminate}
gimp -idf  --console-messages --no-data --no-splash --batch-interpreter python-fu-eval -b - < ./mansikiFinisherMQkicker.py
#gimp -idf --batch-interpreter python-fu-eval -b ${gimpfuKicker} -b ${gimpfuTerminate}
#${gimpfuKicker}
#-b ${gimpfuTerminate}

