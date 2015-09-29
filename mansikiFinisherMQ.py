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
num_worker_threads =2
cmd = "gimp --no-interface --console-messages --no-data --no-splash --batch-interpreter python-fu-eval --batch - < " + curdir + "makeImage.py "
#---------------------------------------------------------------------
# Queue
class AsyncCallUnionFile(threading.Thread):
    def __init__(self, q, finalPrefix, prefix, listOfFile, works, width, height, offsetX, offsetY, direction):
        threading.Thread.__init__(self)
        self.q = q
        self.target = target
        self.works = works
        self.dpi = dpi
        self.size = size
        self.frontPrefix = frontPrefix
        self.mainPrefix = mainPrefix
        self.rearPrefix = rearPrefix
        self.direction = direction
        self.isCut = isCut
        self.padding = padding

    def run(self):
        while True: 
           item = self.q.get() 
           print item
           os.system(item)
           self.q.task_done() 
class AsyncCallParPage(threading.Thread):
    def __init__(self, q, target, works, dpi, size, frontPrefix, mainPrefix, rearPrefix,finalPrefix, direction, isCut, padding):
        threading.Thread.__init__(self)
        self.q = q
        self.target = target
        self.works = works
        self.dpi = dpi
        self.size = size
        self.frontPrefix = frontPrefix
        self.mainPrefix = mainPrefix
        self.rearPrefix = rearPrefix
        self.direction = direction
        self.isCut = isCut
        self.padding = padding

    def run(self):
        while True: 
           item = self.q.get() 
           print item
           os.system(item)
           self.q.task_done() 
#マルチスレッド実行
def executeMultiProcess(files, target, works, dpi, size, frontPrefix, mainPrefix, rearPrefix,finalPrefix, direction, isCut, padding):
    queueOfFront = Queue(0) 
    queueOfMain = Queue(0) 
    queueOfRear = Queue(0) 
	listOfFront = []
	listOfMain = []
	listOfRear = []
	for file in sorted(files):
		print file
		name,ext = os.path.splitext( os.path.basename(file) )
		if re.search(frontPrefix, name ) != None and re.search('.*\.xcf', file ) != None:
			queueOfFront.append(file)
			listOfFront.append(file)
		if re.search(mainPrefix, name ) != None and re.search('.*\.xcf', file ) != None:
			queueOfMain.append(file)
			listOfMain.append(file)
		if re.search(rearPrefix, name ) != None and re.search('.*\.xcf', file ) != None:
			queueOfRear.append(file)
			listOfRear.append(file)
    for i in range(num_worker_threads): 
        task = AsyncCall(queueOfFront)
        task.start()
    for i in range(num_worker_threads): 
        task = AsyncCall(queueOfMain)
        task.start()
    for i in range(num_worker_threads): 
        task = AsyncCall(queueOfRear)
        task.start()
    queueOfFront.join()       #
    queueOfMain.join()       #
    queueOfRear.join()       #

def mansiki_build_images_for_copyprint(image, drowable, target, works, dpi, size, frontPrefix, mainPrefix, rearPrefix,finalPrefix, direction, isCut, padding):
	first = sys.path[0]
	start_time = time.time()
	print ("elapsed_time:{0}".format(start_time)) + "[sec]"
	curdir = first + "/" # カレントディレクトリ名を取得
	isInputed = True

	#ファイル一覧を取得
	#target = "/home/alfx61/画像/4prints/test"
	if os.path.exists(target) == False :
		pdb.gimp_message("指定のディレクトリが存在しません。[ " + target + " ]")
		return
	#pngの画像サイズをA4@600dpiに変換
	width=600
	height=600
	#padding = 2.64
	if size == 'B5':
		width = int(math.ceil((182-padding*2)*(dpi/25.4)))
		height = int(math.ceil((257-padding*2)*(dpi/25.4))) 
		widthWrapper = int(math.ceil(210*(dpi/25.4)))
		heightWrapper = int(math.ceil(297*(dpi/25.4))) 
	if size == 'A5':
		width = int(math.ceil((148-padding*2)*(dpi/25.4)))
		height = int(math.ceil((210-padding*2)*(dpi/25.4))) 
		widthWrapper = int(math.ceil(182*(dpi/25.4)))
		heightWrapper = int(math.ceil(257*(dpi/25.4))) 
	if size == 'A4':
		width = int(math.ceil((210-padding*2)*(dpi/25.4)))
		height = int(math.ceil((297-padding*2)*(dpi/25.4))) 
		widthWrapper = int(math.ceil(257*(dpi/25.4)))
		heightWrapper = int(math.ceil(364*(dpi/25.4))) 
	offsetX = int(math.ceil((widthWrapper-width)/2))*-1
	offsetY = int(math.ceil((heightWrapper-height)/2))*-1
	pdb.gimp_message("START!!/size:" + size +"/width:" + str(width)+"/height:" + str(height)+"/widthWrapper:" + str(widthWrapper)+"/heightWrapper:" + str(heightWrapper)+"/offsetX:" + str(offsetX)+"/offsetY:" + str(offsetY))
	files = os.listdir(target)
	#一旦中でスケジュール表を作成する。
	listOfFront = []
	listOfMain = []
	listOfRear = []
	for file in files:
		print file
		name,ext = os.path.splitext( os.path.basename(file) )
		if re.search(frontPrefix, name ) != None and re.search('.*\.xcf', file ) != None:
			listOfFront.append(file)
			pass
		if re.search(mainPrefix, name ) != None and re.search('.*\.xcf', file ) != None:
			listOfMain.append(file)
			pass
		if re.search(rearPrefix, name ) != None and re.search('.*\.xcf', file ) != None:
			listOfRear.append(file)
			pass
		pass
	# 3種類のファイル名について順番に取得し、配列に入れる。
	#
	#ファイル単位で処理
	isCut = True
	for file in sorted(listOfFront):
		name,ext = os.path.splitext( os.path.basename(file) )
		fileName = target + "/" + file
		fileName = doResize(fileName,works,name,False,widthWrapper,heightWrapper,width,height,offsetX,offsetY)
		pass
	for file in sorted(listOfMain):
		name,ext = os.path.splitext( os.path.basename(file) )
		fileName = target + "/" + file
		fileName = doResize(fileName,works,name,isCut,widthWrapper,heightWrapper,width,height,offsetX,offsetY)
		pass
	for file in sorted(listOfRear):
		name,ext = os.path.splitext( os.path.basename(file) )
		fileName = target + "/" + file
		fileName = doResize(fileName,works,name,False,widthWrapper,heightWrapper,width,height,offsetX,offsetY)
		pass
	doUnionForPrint(finalPrefix,frontPrefix,listOfFront,works,width,height,offsetX,offsetY, direction)
	doUnionForPrint(finalPrefix,mainPrefix,listOfMain,works,width,height,offsetX,offsetY, direction)
	doUnionForPrint(finalPrefix,rearPrefix,listOfRear,works,width,height,offsetX,offsetY, direction)
	#上記のファイル名を記憶。
	#上記を繰り替えす。
	#---------------------------------------------------
	curdir = sys.path[0] + "/" # カレントディレクトリ名を取得
	#pdb.gimp_message("" + curdir)
	elapsed_time = time.time() - start_time
	pageNum = len(listOfFront)+len(listOfMain)+len(listOfRear)
	paperNum = math.floor(len(listOfFront)/2)+math.floor(len(listOfMain)/2)+math.floor(len(listOfRear)/2)
	pdb.gimp_message("完了しました！処理時間：" + str(math.floor(elapsed_time/60))+"分/処理枚数："+str(pageNum)+"/紙："+str(paperNum))
	pass
def doResize(filename,works,baseName,isCut,widthWrapper,heightWrapper,width,height,offsetX,offsetY):
	pngFileName = works + "/" + baseName + "B.png"
	pngFileNameSave = works + "/" + baseName + ".png"
	jpgFileName = works + "/" + baseName + ".jpg"
	#pdb.gimp_message("pngFileName：" + pngFileName)
	#pdb.gimp_message("/width:" + str(width)+"/height:" + str(height)+"/widthWrapper:" + str(widthWrapper)+"/heightWrapper:" + str(heightWrapper)+"/offsetX:" + str(offsetX)+"/offsetY:" + str(offsetY))
	img = pdb.gimp_file_load(filename, filename)
	img.flatten()
	layer = pdb.gimp_image_merge_visible_layers(img, gimpfu.CLIP_TO_IMAGE)
	#pngにエクスポート
	# 問題はオプションどうやって設定するのか。
	pdb.gimp_file_save(img, layer, pngFileName, pngFileName)
	#画像を閉じる。
	pdb.gimp_image_delete(img)
	#####################################################
	if isCut == False:
		widthWrapper = width
		heightWrapper = height
		offsetX = 0
		offsetY = 0
		pass	
	#再度pngを開く
	pngImg = pdb.gimp_file_load(pngFileName, pngFileName)
	#目標のサイズに拡大縮小する。
	pdb.gimp_image_scale(pngImg,widthWrapper,heightWrapper)
	#8354 4177 5907
	#内側を4907で中央から切り取り//
	pdb.gimp_image_resize(pngImg,width,height,offsetX,offsetY)
	pngLayer = pdb.gimp_image_merge_visible_layers(pngImg, gimpfu.CLIP_TO_IMAGE)
	#切り取ったファイルをpngにエクスポート
	pdb.gimp_file_save(pngImg, pngLayer, pngFileName, pngFileName)
	NONINTERACTIVE=1
	quality=1.00
	smoothing=0.00
	optimize=1
	progressive=0
	comment=""
	subsmp=0
	baseline=1
	restart=0
	dct=0
	pdb.file_jpeg_save(pngImg, pngLayer, jpgFileName, jpgFileName,quality,smoothing,optimize,progressive,comment,subsmp,baseline,restart,dct)
	#大きいpngは削除
	pdb.gimp_file_save(pngImg, pngLayer, pngFileNameSave, pngFileNameSave)
	
	pdb.gimp_image_delete(pngImg)
	return pngFileName
	
def makeUnionQueue(listOfFile):
    queue = Queue(0) 
	count = 0
	lastFileName = ""
	for file in sorted(listOfFile):
		#特定のルールに則って結合画像を作成。
		count += 1
		mod = count % 2
		name,ext = os.path.splitext( os.path.basename(file) )
		pngFileNameSave = works + "/" + name + ".png"
		if mod == 0 :
			filNames = (lastFileName,pngFileNameSave)
			queue.append(filNames)
			lastFileName = ""
		else :
			lastFileName = pngFileNameSave
		#break
		pass
	if lastFileName != "":
		filNames = (lastFileName,"")
		queue.append(filNames)
		lastFileName = "";
		pass
	pass
def doUnionForPrintDo(finalPrefix, prefix, fileNames,works,width,height,offsetX,offsetY, direction):
	(lastFileName, pngFileNameSave) = fileNames
	RGB=0
	WHITEFILL=2
	NONINTERACTIVE=1
	quality=1.00
	smoothing=0.00
	optimize=1
	progressive=0
	comment=""
	subsmp=0
	baseline=1
	restart=0
	dct=0
	#ターゲットサイズの２倍のサイズで画像を用意
	unionImage = pdb.gimp_image_new(width*2, height, RGB)
	topLayer = pdb.gimp_layer_new(unionImage, width*2, height, RGB, "BASE", 0, 0)
	pdb.gimp_image_add_layer(unionImage, topLayer, 0)
	topLayer = pdb.gimp_image_merge_visible_layers(unionImage, gimpfu.CLIP_TO_IMAGE)
	pdb.gimp_image_select_item(unionImage, 0, topLayer)
	pdb.gimp_drawable_fill(topLayer, gimpfu.BACKGROUND_FILL)
	
	#左右ペアの画像を読み込み
	pageA = pdb.gimp_file_load_layer(unionImage, lastFileName)
	pdb.gimp_image_add_layer(unionImage, pageA, 0)
	pageAoffsetX = 0 if direction == False else width + 1
	pageAoffsetY = 0
	pdb.gimp_layer_set_offsets(pageA, pageAoffsetX, pageAoffsetY)
	filePrefix = finalPrefix + prefix + str(count+100)[1:3] + "_" + str(count+101)[1:3] 
	if pngFileNameSave != "":
		pageB = pdb.gimp_file_load_layer(unionImage, pngFileNameSave)
		pdb.gimp_image_add_layer(unionImage, pageB, 0)
		pageBoffsetX = 0 if direction == True else width + 1
		pageBoffsetY = 0
		pdb.gimp_layer_set_offsets(pageB, pageBoffsetX, pageBoffsetY)
		filePrefix = finalPrefix + prefix + str(count+ 99)[1:3]  + "_" + str(count+100)[1:3] 
	#結合画像をpngでエクスポート
	pngLayer = pdb.gimp_image_merge_visible_layers(unionImage, gimpfu.CLIP_TO_IMAGE)
	#切り取ったファイルをpngにエクスポート
	pngFileName = works + "/" + filePrefix + ".png"
	jpgFileName = works + "/" + filePrefix + ".jpg"
	pdb.gimp_file_save(unionImage, pngLayer, pngFileName, pngFileName)
	pdb.file_jpeg_save(unionImage, pngLayer, jpgFileName, jpgFileName,quality,smoothing,optimize,progressive,comment,subsmp,baseline,restart,dct)
	pdb.gimp_image_delete(unionImage)
	lastFileName = "";
	pass

gimpfu.register(
        # name
        "python-fu-mansiki-build-images-for-copyprint",
        # blurb
        "python-fu mansiki-build-images-for-copyprint\n漫式原稿用紙コンビニ印刷用用紙整形スクリプト",
        # help
        "experiment",
        # author
        "experiment <ryunosinfx2._{at}_.gmail.com>",
        # copyright
        "experiment",
        # date
        "2015",
        # menupath
        "<Image>/Python-Fu/MansikiBuildImagesForCopyPrint",
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
         ],
        # results
        [],
        # function
        mansiki_build_images_for_copyprint)

gimpfu.main()
