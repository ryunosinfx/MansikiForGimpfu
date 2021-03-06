#!/usr/bin/python
# coding: UTF-8

import sys,os,re,math,time,threading
sys.path.insert(1, '/usr/lib/gimp/2.0/python')
import cStringIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A5
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import B5
from reportlab.lib.units import inch
import reportlab.lib.colors as color
import Image
import ImageDraw
import ImageOps
from PIL import Image



def pdfMakeBy3Element(filename, works, dpi, size, frontFileNames,mainFileNames,rearFileNames):
	fileNames = []
	if len(frontFileNames) % 2 > 0 :
		frontFileNames.append("")
	if len(mainFileNames) % 2 > 0 :
		mainFileNames.append("")
	if len(rearFileNames) % 2 > 0 :
		rearFileNames.append("")
	fileNames.extend(frontFileNames)
	fileNames.extend(mainFileNames)
	fileNames.extend(rearFileNames)
	pdfMake(filename, works, dpi, size, fileNames)
	pass

def pdfMake(filename, works, dpi, size, fileNames):
	width=600
	height=600
	padding = 0
	if size == 'B5':
		width = int(math.ceil((182-padding*2)*(dpi/25.4)))
		height = int(math.ceil((257-padding*2)*(dpi/25.4)))
	if size == 'A5':
		width = int(math.ceil((148-padding*2)*(dpi/25.4)))
		height = int(math.ceil((210-padding*2)*(dpi/25.4)))
	if size == 'A4':
		width = int(math.ceil((210-padding*2)*(dpi/25.4)))
		height = int(math.ceil((297-padding*2)*(dpi/25.4)))
	pageSize = (width, height)
	print A5
	print B5
	print A4
	pageRecio = float(width)/height #1:3 1:2
	fpdf = canvas.Canvas(works+"/"+filename+".pdf", pagesize=pageSize, pageCompression=1)
	for file in fileNames:
		print "PDF base file:"+file
		if file == "" :
			fpdf.showPage()
			continue
		baseName,ext = os.path.splitext( os.path.basename(file) )
		pngFileNameSave = works + "/" + baseName + ".png"
		print "PDF base file:"+pngFileNameSave
		try:
			image = Image.open(pngFileNameSave)
		except:
			continue
		w, h = image.size#拡大縮小貼付けします。
		print "w/h:"+str(w)+"/"+str(h)
		recio = float(w)/h #1:2 1:3
		print "w/h:"+str(w)+"/"+str(h)+"/"+str(recio)+"/"+str(width)+"/"+str(height)+"/"+str(pageRecio)
		offsetY = 0
		offsetX = 0
		if pageRecio < recio:
			w = width
			h = width/recio
			offsetY = (height - h) / 2
		if pageRecio > recio:
			w = height*recio
			h = height
			offsetX = (width - w) / 2
		if image.mode != "RGB":
			image = image.convert("RGB")
		recio2 = float(w)/h #1:2 1:3
		print "w/h:"+str(w)+"/"+str(h)+"/"+str(recio)+"/"+str(recio2)+"/offsetX:"+str(offsetX)
		inv_image = ImageOps.invert(image)
		rect = inv_image.getbbox()
		image = image.crop(rect)
		draw = ImageDraw.Draw(image)
		draw.rectangle([(0,0), (w-1,h-1)], outline='#000000')#枠線を引く
		fout = cStringIO.StringIO()
		image.save(fout, "png")
		image = image.convert("P")
		fpdf.drawInlineImage(image, offsetX, offsetY,
			width = w,
			height = h)
		fpdf.showPage()
	fpdf.save()

if __name__ == '__main__':
	pdfMake("testaa", "/home/alfx61/tmp", 600, "B5", ["Front_01.png"])
