# MansikiForGimpfu

Mansikiの仕上げ描画部分を担当するGimpの補助プラグイン群です。

##サポート範囲
多分gimp2.8で動くはず。
Ubuntu14.04で動作確認済み。他のプラットフォームは知りません。

## 使い方（全般）
pyファイルを~/.gimp-2.8/plug-ins/にコピーしてください。
実行権限の付与が必要です。
gimpを起動するとpython-fuというメニューが出てくるのでそこから使ってください。
上のimageとdrowableは指定不要です。
### 個別ファイルについて
#### 原稿用紙xcfファイル→印刷用ファイル
##### mansikiFinisherMQ.py
マルチスレッドでxcfファイルから指定の用紙サイズで
png,jpg,pdfを出力します。
メニュー上では以下の名前で表示されます。
MansikiBuildImagesForCopyPrintMQ
##### mansikiFinisherMQBatch.py
mansikiFinisherMQ.pyの本体です。

##### mansikiFinisherPDF.py
PDF出力モジュールです。

#### sh配下
基本こちらにはバッチ実行のためのファイルが記載されています。

## 前提条件
### python
2.7.6で作業を行っています。
#### 追加のモジュール
Reportlab で PDF を出力しているのでReportlabが必要です。
### gimp
2.8.10で作業しています。
Ubuntuでのみ動作確認済みです。WindowsやMacは知りません。

> sudo pip install reportlab
で入手できます。


### license

This software is released under the MIT License, see LICENSE.txt.
