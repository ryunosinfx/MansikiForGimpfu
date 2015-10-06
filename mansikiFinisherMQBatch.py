#!/usr/bin/python
# coding: UTF-8

import sys,os,re,math,time,threading
sys.path.insert(1, '/usr/lib/gimp/2.0/python')
import gimpfu
from gimpfu import *
from os.path import expanduser
from Queue import Queue
import mansikiFinisherPDF

#---------------------------------------------------------------------
first = sys.path[0]
curdir = first + "/" # カレントディレクトリ名を取得
sys.path.insert(1, curdir)
#---------------------------------------------------------------------
# Queue
class ForceThreadEndingError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
class AsyncCallUnionFile(threading.Thread):
    def __init__(self, q, finalPrefix, prefix, works, width, height, direction):
        threading.Thread.__init__(self)
        self.q = q
        self.finalPrefix = finalPrefix
        self.prefix = prefix
        self.works = works
        self.width = width
        self.height = height
        self.direction = direction
        self.daemon = True
        self.stop_event = threading.Event() #停止させるかのフラグ
    def run(self):
        while True: 
			fileNames = self.q.get() 
			(lastFileName, pngFileNameSave,count) = fileNames
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
			unionImage = pdb.gimp_image_new(self.width*2, self.height, RGB)
			topLayer = pdb.gimp_layer_new(unionImage, self.width*2, self.height, RGB, "BASE", 0, 0)
			pdb.gimp_image_add_layer(unionImage, topLayer, 0)
			topLayer = pdb.gimp_image_merge_visible_layers(unionImage, gimpfu.CLIP_TO_IMAGE)
			pdb.gimp_image_select_item(unionImage, 0, topLayer)
			pdb.gimp_drawable_fill(topLayer, gimpfu.BACKGROUND_FILL)
	
			#左右ペアの画像を読み込み
			pageA = pdb.gimp_file_load_layer(unionImage, lastFileName)
			pdb.gimp_image_add_layer(unionImage, pageA, 0)
			pageAoffsetX = 0 if self.direction == False else self.width + 1
			pageAoffsetY = 0
			pdb.gimp_layer_set_offsets(pageA, pageAoffsetX, pageAoffsetY)
			filePrefix = self.finalPrefix + self.prefix + str(count+100)[1:3] + "_" + str(count+101)[1:3] 
			if pngFileNameSave != "":
				pageB = pdb.gimp_file_load_layer(unionImage, pngFileNameSave)
				pdb.gimp_image_add_layer(unionImage, pageB, 0)
				pageBoffsetX = 0 if self.direction == True else self.width + 1
				pageBoffsetY = 0
				pdb.gimp_layer_set_offsets(pageB, pageBoffsetX, pageBoffsetY)
				filePrefix = self.finalPrefix + self.prefix + str(count+ 99)[1:3]  + "_" + str(count+100)[1:3] 
			#結合画像をpngでエクスポート
			pngLayer = pdb.gimp_image_merge_visible_layers(unionImage, gimpfu.CLIP_TO_IMAGE)
			#切り取ったファイルをpngにエクスポート
			pngFileName = self.works + "/" + filePrefix + ".png"
			jpgFileName = self.works + "/" + filePrefix + ".jpg"
			pdb.gimp_file_save(unionImage, pngLayer, pngFileName, pngFileName)
			pdb.file_jpeg_save(unionImage, pngLayer, jpgFileName, jpgFileName,quality,smoothing,optimize,progressive,comment,subsmp,baseline,restart,dct)
			pdb.gimp_image_delete(unionImage)
			lastFileName = "";
			self.q.task_done() 
    def stop(self): #スレッドを停止させる
        self.stop_event.set()
        raise ForceThreadEndingError('AsyncCallUnionFile')
class AsyncCallParPage(threading.Thread):
    def __init__(self, q, target, works, isCut, widthWrapper, heightWrapper, width, height, offsetX, offsetY):
        threading.Thread.__init__(self)
        self.q = q
        self.target = target
        self.works = works
        self.isCut = isCut
        self.widthWrapper = widthWrapper
        self.heightWrapper = heightWrapper
        self.width = width
        self.height = height
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.daemon = True
        self.stop_event = threading.Event() #停止させるかのフラグ
    def run(self):
        while True: 
			file = self.q.get() 
			print "processing file:"+file
			baseName,ext = os.path.splitext( os.path.basename(file) )
			#print baseName
			filename = self.target + "/" + file
			pngFileName = self.works + "/" + baseName + "B.png"
			pngFileNameSave = self.works + "/" + baseName + ".png"
			jpgFileName = self.works + "/" + baseName + ".jpg"
			img = pdb.gimp_file_load(filename, filename)
			img.flatten()
			layer = pdb.gimp_image_merge_visible_layers(img, gimpfu.CLIP_TO_IMAGE)
			#pngにエクスポート
			# 問題はオプションどうやって設定するのか。
			pdb.gimp_file_save(img, layer, pngFileName, pngFileName)
			#画像を閉じる。
			pdb.gimp_image_delete(img)
			#####################################################
			widthWrapper = self.widthWrapper
			heightWrapper = self.heightWrapper
			offsetX = self.offsetX
			offsetY = self.offsetY
			if self.isCut == False:
				widthWrapper = self.width
				heightWrapper = self.height
				offsetX = 0
				offsetY = 0
				pass	
			#再度pngを開く
			pngImg = pdb.gimp_file_load(pngFileName, pngFileName)
			#目標のサイズに拡大縮小する。
			pdb.gimp_image_scale(pngImg, widthWrapper, heightWrapper)
			#8354 4177 5907
			#内側を4907で中央から切り取り//
			pdb.gimp_image_resize(pngImg, self.width, self.height, offsetX, offsetY)
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
			self.q.task_done() 
    def stop(self): #スレッドを停止させる
        self.stop_event.set()
        raise ForceThreadEndingError('AsyncCallParPage')
#マルチスレッド実行
def executeMultiProcess(target, works, frontPrefix, mainPrefix, rearPrefix,finalPrefix, direction, isCut, widthWrapper, heightWrapper, width, height, offsetX, offsetY, numWorkerThreads, dpi, size):
	queueOfFront = Queue(0) 
	queueOfMain = Queue(0) 
	queueOfRear = Queue(0) 
	listOfFront = []
	listOfMain = []
	listOfRear = []
	files = os.listdir(target)
	for file in sorted(files):
		#print file
		name,ext = os.path.splitext( os.path.basename(file) )
		if re.search(frontPrefix, name ) != None and re.search('.*\.xcf', file ) != None:
			queueOfFront.put(file)
			listOfFront.append(file)
		if re.search(mainPrefix, name ) != None and re.search('.*\.xcf', file ) != None:
			queueOfMain.put(file)
			listOfMain.append(file)
		if re.search(rearPrefix, name ) != None and re.search('.*\.xcf', file ) != None:
			queueOfRear.put(file)
			listOfRear.append(file)
	for i in range(numWorkerThreads):
		task = AsyncCallParPage(queueOfFront, target, works, False, widthWrapper, heightWrapper, width, height, offsetX, offsetY)
		task.start()
	for i in range(numWorkerThreads):
		task = AsyncCallParPage(queueOfMain, target, works, isCut, widthWrapper, heightWrapper, width, height, offsetX, offsetY)
		task.start()
	for i in range(numWorkerThreads):
		task = AsyncCallParPage(queueOfRear, target, works, False, widthWrapper, heightWrapper, width, height, offsetX, offsetY)
		task.start()
	###################################################
	mansikiFinisherPDF.pdfMakeBy3Element("pdftest", works, dpi, size, listOfFront,listOfMain,listOfRear)
	###################################################
	queueOfFront.join()       #
	queueUnionFront = makeUnionQueue(works, listOfFront)
	for i in range(numWorkerThreads): 
		task = AsyncCallUnionFile(queueUnionFront, finalPrefix, frontPrefix, works, width, height, direction)
		task.start()
	queueOfMain.join()       #
	queueUnionMain = makeUnionQueue(works, listOfMain)
	for i in range(numWorkerThreads): 
		task = AsyncCallUnionFile(queueUnionMain, finalPrefix, mainPrefix, works, width, height, direction)
		task.start()
	queueOfRear.join()       #
	queueUnionRear = makeUnionQueue(works, listOfRear)
	for i in range(numWorkerThreads): 
		task = AsyncCallUnionFile(queueUnionRear, finalPrefix, rearPrefix, works, width, height, direction)
		task.start()
	queueUnionFront.join()       #
	queueUnionMain.join()       #
	queueUnionRear.join()       #
	threadsTerminate()
	pageNum = len(listOfFront)+len(listOfMain)+len(listOfRear)
	paperNum = math.floor(len(listOfFront)/2)+math.floor(len(listOfMain)/2)+math.floor(len(listOfRear)/2)
	endMessage = "/処理枚数："+str(pageNum)+"/紙："+str(paperNum)
	print endMessage
	return endMessage
def threadsTerminate():
	#####スレッドを例外経由でぶっ殺す######################################
	tlist=threading.enumerate()
	print "threadsTerminate!---START---ThreadNum:"+str(len(tlist))
	main_thread=threading.currentThread()
	for t in tlist:
		if t is main_thread: continue
		try:
			#print t
			t.stop()
			t.join(10)
		except ForceThreadEndingError,exp:
			print "ForceThreadEndingError:", exp
		except:
			print "expected error:", sys.exc_info()[0]
		else:
			print "end!"
	time.sleep(10)
	tlist=threading.enumerate()
	print "threadsTerminate!---END---ThreadNum:"+str(len(tlist))
	for t in tlist:
		if t is main_thread: continue
		print t
	###########################################
def run(image, drowable, target, works, dpi, size, frontPrefix, mainPrefix, rearPrefix,finalPrefix, direction, isCut, padding, numWorkerThreads):
	first = sys.path[0]
	start_time = time.time()
	print ("elapsed_time:{0}".format(start_time)) + "[sec]"
	curdir = first + "/" # カレントディレクトリ名を取得
	isInputed = True

	#ファイル一覧を取得
	#target = "/home/alfx61/画像/4prints/test"
	if os.path.exists(target) == False :
		print "指定のディレクトリが存在しません。[ " + target + " ]"
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
	print "START!!/size:" + size +"/width:" + str(width)+"/height:" + str(height)+"/widthWrapper:" + str(widthWrapper)+"/heightWrapper:" + str(heightWrapper)+"/offsetX:" + str(offsetX)+"/offsetY:" + str(offsetY)+"/numWorkerThreads:"+str(numWorkerThreads)
	result = executeMultiProcess(target, works, frontPrefix, mainPrefix, rearPrefix,finalPrefix, direction, isCut, widthWrapper, heightWrapper, width, height, offsetX, offsetY, numWorkerThreads, dpi, size)
	#上記のファイル名を記憶。
	#上記を繰り替えす。
	#---------------------------------------------------
	curdir = sys.path[0] + "/" # カレントディレクトリ名を取得
	#pdb.gimp_message("" + curdir)
	elapsed_time = time.time() - start_time
	msg = "完了しました！処理時間：" + str(math.floor(elapsed_time/60))+"分"+result
	print msg
	return msg

def makeUnionQueue(works, listOfFile):
	queue = Queue(0) 
	count = 0
	lastFileName = ""
	for file in sorted(listOfFile):
		#特定のルールに則って結合画像を作成。
		count += 1
		mod = count % 2
		name,ext = os.path.splitext( os.path.basename(file) )
		if name == "" :
			break
		pngFileNameSave = works + "/" + name + ".png"
		if mod == 0 :
			filNames = (lastFileName,pngFileNameSave,count)
			queue.put(filNames)
			lastFileName = ""
		else :
			lastFileName = pngFileNameSave
	if lastFileName != "":
		filNames = (lastFileName,"",count)
		queue.put(filNames)
		lastFileName = "";
	return queue
    
    
    
