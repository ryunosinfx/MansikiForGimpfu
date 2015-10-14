#!/bin/bash

cd $HOME/.gimp-2.8/plug-ins/sh
gimp -idf  --console-messages --no-data --no-splash --batch-interpreter python-fu-eval -b - < ./mansikiFinisherMQkicker.py
