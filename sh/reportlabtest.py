# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import reportlab.lib.colors as color


def make(filename="pdftest"):
    pdf_canvas = set_info(filename)
    print_string(pdf_canvas)
    print_figure(pdf_canvas)
    print_line(pdf_canvas)
    pdf_canvas.save()


# 初期設定
def set_info(filename):
    pdf_canvas = canvas.Canvas("./{0}.pdf".format(filename), bottomup=False)  # 原点は左上
        
    pdf_canvas.setAuthor("ともっくす")
    pdf_canvas.setTitle("pythonを使ってpdf_canvasを生成する")
    pdf_canvas.setSubject("reportlab")

    return pdf_canvas


# 文字
def print_string(pdf_canvas):
    # フォントを登録する
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))

    # ゴシック体をサイズ15で
    pdf_canvas.setFont("HeiseiKakuGo-W5", 15)
    pdf_canvas.drawString(50, 50, "ゴシック体をサイズ15で")

    # 明朝体をサイズ30で
    pdf_canvas.setFont("HeiseiMin-W3", 30)
    pdf_canvas.drawString(300, 100, "明朝体をサイズ30で")


# 図形
def print_figure(pdf_canvas):
    # 枠線のみの四角
    pdf_canvas.rect(50, 150, 200, 250)

    # 青色の円
    pdf_canvas.setFillColor(color.blue)
    pdf_canvas.circle(400, 350, 50, stroke=False, fill=True)


# 線
def print_line(pdf_canvas):
    # 普通の線
    pdf_canvas.line(50, 450, 500, 450)

    # 赤い太い線
    pdf_canvas.setStrokeColor(color.red)
    pdf_canvas.setLineWidth(10)
    pdf_canvas.line(100, 500, 550, 500)

    # 破線
    pdf_canvas.setStrokeColor(color.black)
    pdf_canvas.setLineWidth(5)
    pdf_canvas.setDash([2, 8, 5, 10])
    pdf_canvas.line(150, 550, 600, 550)

    # 複数の線
    pdf_canvas.setLineWidth(1)
    pdf_canvas.setDash([])
    lines = [(100, 650, 200, 750), (200, 750, 300, 650), (300, 650, 300, 750), (100, 700, 400, 700)]
    pdf_canvas.lines(lines)


if __name__ == '__main__':
    make()

