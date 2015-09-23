#!/usr/bin/python
# coding: UTF-8

import sys,os,re,gimpfu,math,time
first = sys.path[0]
sys.path.insert(1, '/usr/lib/gimp/2.0/python')
from gimpfu import *
from os.path import expanduser
curdir = first + "/" # カレントディレクトリ名を取得
print "curdir:" + curdir


def mansiki_build_images_for_copyprint(image, drowable, target, works, dpi, size, frontPrefix, mainPrefix, rearPrefix,finalPrefix, direction, isCut, padding):
	first = sys.path[0]
	start_time = time.time()
	print ("elapsed_time:{0}".format(start_time)) + "[sec]"
	#pdb.gimp_message("target:" + target)
	#pdb.gimp_message("works:" + works)
	#pdb.gimp_message("dpi:" + str(dpi))
	#pdb.gimp_message("size:" + size)
	#pdb.gimp_message("frontPrefix:" + frontPrefix)
	#pdb.gimp_message("mainPrefix" + mainPrefix)
	#pdb.gimp_message("rearPrefix" + rearPrefix)
	#pdb.gimp_message("direction" + str(direction))
	curdir = first + "/" # カレントディレクトリ名を取得
	isInputed = True

	#ファイル一覧を取得
	#target = "/home/alfx61/画像/4prints/test"
	if os.path.exists(target) == False :
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
	count = 0
	countall = 0
	for file in sorted(listOfFront):
		count+=1
		name,ext = os.path.splitext( os.path.basename(file) )
		fileName = target + "/" + file
		fileName = doResize(fileName,works,name,False,widthWrapper,heightWrapper,width,height,offsetX,offsetY)
		#break
		pass
	doUnionForPrint(finalPrefix,frontPrefix,listOfFront,works,width,height,offsetX,offsetY, direction)
	count = 0
	for file in sorted(listOfMain):
		count+=1
		name,ext = os.path.splitext( os.path.basename(file) )
		fileName = target + "/" + file
		fileName = doResize(fileName,works,name,isCut,widthWrapper,heightWrapper,width,height,offsetX,offsetY)
		#break
		pass
	doUnionForPrint(finalPrefix,mainPrefix,listOfMain,works,width,height,offsetX,offsetY, direction)
	count = 0
	for file in sorted(listOfRear):
		count+=1
		name,ext = os.path.splitext( os.path.basename(file) )
		fileName = target + "/" + file
		fileName = doResize(fileName,works,name,False,widthWrapper,heightWrapper,width,height,offsetX,offsetY)
		#break
		pass
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
	
def doUnionForPrint(finalPrefix,prefix,listOfFile,works,width,height,offsetX,offsetY, direction):
	count = 0
	lastFileName = ""
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
	pdb.gimp_context_set_background((255,255,255))
	for file in sorted(listOfFile):
		#特定のルールに則って結合画像を作成。
		count += 1
		mod = count % 2
		name,ext = os.path.splitext( os.path.basename(file) )
		pngFileNameSave = works + "/" + name + ".png"
		if mod == 0 :
			#ターゲットサイズの２倍のサイズで画像を用意
			unionImage = pdb.gimp_image_new(width*2, height, RGB)
			topLayer = pdb.gimp_layer_new(unionImage,width*2, height,RGB,"BASE",0,0)
			pdb.gimp_image_add_layer(unionImage,topLayer,0)
			topLayer = pdb.gimp_image_merge_visible_layers(unionImage, gimpfu.CLIP_TO_IMAGE)
			pdb.gimp_image_select_item(unionImage,0,topLayer)
			pdb.gimp_drawable_fill(topLayer, gimpfu.BACKGROUND_FILL)
			
			#左右ペアの画像を読み込み
			pageA = pdb.gimp_file_load_layer(unionImage,lastFileName)
			pageB = pdb.gimp_file_load_layer(unionImage,pngFileNameSave)
			pdb.gimp_image_add_layer(unionImage,pageA,0)
			pdb.gimp_image_add_layer(unionImage,pageB,0)
			pageAoffsetX = 0 if direction == False else width + 1
			pageBoffsetX = 0 if direction == True else width + 1
			pageAoffsetY = 0
			pageBoffsetY = 0
			pdb.gimp_layer_set_offsets(pageA,pageAoffsetX,pageAoffsetY)
			pdb.gimp_layer_set_offsets(pageB,pageBoffsetX,pageBoffsetY)
			#結合画像をpngでエクスポート
			pngLayer = pdb.gimp_image_merge_visible_layers(unionImage, gimpfu.CLIP_TO_IMAGE)
			#切り取ったファイルをpngにエクスポート
			filePrefix = finalPrefix + prefix + str(count+ 99)[1:3]  + "_" + str(count+100)[1:3] 
			#xcfFileName = works + "/" + filePrefix + ".xcf"
			#pdb.gimp_xcf_save(0,unionImage, pngLayer, xcfFileName, xcfFileName)
			pngFileName = works + "/" + filePrefix + ".png"
			jpgFileName = works + "/" + filePrefix + ".jpg"
			pdb.gimp_file_save(unionImage, pngLayer, pngFileName, pngFileName)
			pdb.file_jpeg_save(unionImage, pngLayer, jpgFileName, jpgFileName,quality,smoothing,optimize,progressive,comment,subsmp,baseline,restart,dct)
			pdb.gimp_image_delete(unionImage)
			lastFileName = "";
			pass
		else :
			lastFileName = pngFileNameSave;
			pass
		#break
		pass
	if lastFileName != "":
		#ターゲットサイズの２倍のサイズで画像を用意
		unionImage = pdb.gimp_image_new(width*2, height, RGB)
		topLayer = pdb.gimp_layer_new(unionImage,width*2, height,RGB,"BASE",0,0)
		pdb.gimp_image_add_layer(unionImage,topLayer,0)
		topLayer = pdb.gimp_image_merge_visible_layers(unionImage, gimpfu.CLIP_TO_IMAGE)
		pdb.gimp_image_select_item(unionImage,0,topLayer)
		pdb.gimp_drawable_fill(topLayer, gimpfu.BACKGROUND_FILL)
		#左右ペアの画像を読み込み
		pageA = pdb.gimp_file_load_layer(unionImage,lastFileName)
		pdb.gimp_image_add_layer(unionImage,pageA,0)
		
		pageAoffsetX = 0 if direction == False else width + 1
		pageAoffsetY = 0
		pdb.gimp_layer_set_offsets(pageA,pageAoffsetX,pageAoffsetY)
		#結合画像をpngでエクスポート
		pngLayer = pdb.gimp_image_merge_visible_layers(unionImage, gimpfu.CLIP_TO_IMAGE)
		#切り取ったファイルをpngにエクスポート
		filePrefix = finalPrefix + prefix + str(count+100)[1:3] + "_" + str(count+101)[1:3] 
		#xcfFileName = works + "/" + filePrefix + ".xcf"
		#pdb.gimp_xcf_save(0,unionImage, pngLayer, xcfFileName, xcfFileName)
		pngFileName = works + "/" + filePrefix + ".png"
		jpgFileName = works + "/" + filePrefix + ".jpg"
		pdb.gimp_file_save(unionImage, pngLayer, pngFileName, pngFileName)
		pdb.file_jpeg_save(unionImage, pngLayer, jpgFileName, jpgFileName,quality,smoothing,optimize,progressive,comment,subsmp,baseline,restart,dct)
		pdb.gimp_image_delete(unionImage)
		lastFileName = "";
		pass
	pass

#
#pageSizeTuple = cm.convertMapToRadioTuple({msg.get(consts.MANUAL):"handle","A4":"A4","B5":"B5","A5":"A5"})
#def createHashData():
#    
#    pass
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
