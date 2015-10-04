#!/usr/bin/python
# coding: UTF-8

import sys,os,re,gimpfu,math,time,threading
sys.path.insert(1, '/usr/lib/gimp/2.0/python')
from gimpfu import *
from os.path import expanduser
from Queue import Queue
#---------------------------------------------------------------------
first = sys.path[0]
curdir = first + "/" # カレントディレクトリ名を取得
print "curdir:" + curdir
sys.path.insert(1, curdir)
import mansikiFinisherMQBatch
num_worker_threads =2
cmd = "gimp --no-interface --console-messages --no-data --no-splash --batch-interpreter python-fu-eval --batch - < " + curdir + "makeImage.py "
#---------------------------------------------------------------------
# Queue
def mansiki_build_images_for_mq_copyprint(image, drowable, target, works, dpi, size, frontPrefix, mainPrefix, rearPrefix,finalPrefix, direction, isCut, padding, numWorkerThreads):
	msg = mansikiFinisherMQBatch.run(image, drowable, target, works, dpi, size, frontPrefix, mainPrefix, rearPrefix,finalPrefix, direction, isCut, padding, numWorkerThreads)
	pdb.gimp_message("" + msg)
	pass

gimpfu.register(
        # name
        "python-fu-mansiki-build-images-for-mq-copyprint",
        # blurb
        "python-fu mansiki-build-images-for-mq-copyprint\n漫式原稿用紙コンビニ印刷用用紙整形スクリプト\nマルチスレッド対応版",
        # help
        "experiment",
        # author
        "experiment <ryunosinfx2._{at}_.gmail.com>",
        # copyright
        "experiment",
        # date
        "2015",
        # menupath
        "<Image>/Python-Fu/MansikiBuildImagesForCopyPrintMQ",
        # imagetypes
        "",
        # params
        [
         (
            # ディレクトリ選択、 変数名、ラベル、初期値
            gimpfu.PF_DIRNAME, "target","対象格納\nディレクトリ",expanduser("~")
            )
        , (
            # ディレクトリ選択、 変数名、ラベル、初期値
            gimpfu.PF_DIRNAME, "works", "作業、結果格納\nディレクトリ", (expanduser("~")+"/tmp") 
            )
        #ページ数
        , (gimpfu.PF_INT, "dpi", "解像度dpi", 600)
        #ページ数
        , (gimpfu.PF_RADIO, "size", "印刷製本サイズ", "B5", (("A4", "A4"), ("B5", "B5"), ("A5", "A5")))
        #スタイル名
        , (gimpfu.PF_STRING, "frontPrefix", "xcf表紙接頭文字列", "Front_")
        #スタイル名
        , (gimpfu.PF_STRING, "mainPrefix", "xcf本文接頭文字列", "Main_")
        #スタイル名
        , (gimpfu.PF_STRING, "rearPrefix", "xcf裏表紙接頭文字列", "Rear_")
        , (gimpfu.PF_STRING, "finalPrefix", "最終出力品接頭文字列", "U_")
        , (gimpfu.PF_BOOL, "direction",    " ←ページ送り",   True)
        , (gimpfu.PF_BOOL, "isCutMain",    " メインページ切り取り",   True)
        , (gimpfu.PF_FLOAT, "padding",    " 余白mm",   2.64)
        , (gimpfu.PF_INT, "numWorkerThreads",    " 実行スレッド数",   2)
         ],
        # results
        [],
        # function
        mansiki_build_images_for_mq_copyprint)

gimpfu.main()
