#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np

#画像データの読み込み
img = cv.imread("original_cube_yellow.jpg")

#BGR色空間からHSV色空間への変換
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

#色検出しきい値の設定
lower = np.array([20,150,0])
upper = np.array([30,255,255])

#色検出しきい値範囲内の色を抽出するマスクを作成
frame_mask1 = cv.inRange(hsv, lower, upper)

#色検出しきい値の設定
lower = np.array([174,150,0])
upper = np.array([255,255,255])

#色検出しきい値範囲内の色を抽出するマスクを作成
frame_mask2 = cv.inRange(hsv, lower, upper)

frame_mask = frame_mask1 + frame_mask2

#論理演算で色検出
dst = cv.bitwise_and(img, img, mask=frame_mask)

cv.imshow("Image",dst)

if cv.waitKey(0) & 0xFF == ord('q'):
    cv.destroyAllWindows()

