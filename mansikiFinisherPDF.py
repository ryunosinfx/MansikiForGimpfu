#!/usr/bin/python
# coding: UTF-8

import sys,os,re,gimpfu,math,time,threading
sys.path.insert(1, '/usr/lib/gimp/2.0/python')
import cStringIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A5
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import A5
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
		w, h = image.size
		if image.mode != "RGB":
			image = image.convert("RGB")
		inv_image = ImageOps.invert(image)
		rect = inv_image.getbbox()
		image = image.crop(rect)
		draw = ImageDraw.Draw(image)
		draw.rectangle([(0,0), (w-1,h-1)], outline='#000000')
		fout = cStringIO.StringIO()
		image.save(fout, "JPEG", quality=100)
		image = image.convert("P")
		locx = (pageSize[0] - w) / 2
		locy = (pageSize[1] - h) / 2
		fpdf.drawInlineImage(image, locx, locy,
			width = w,
			height = h)
		fpdf.showPage()
	fpdf.save()
