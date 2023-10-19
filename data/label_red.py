#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import cv2 as cv
import numpy as np

#画像データの読み込み
img = cv.imread("original_sheet_red.jpg")

#BGR色空間からHSV色空間への変換
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

#色検出しきい値の設定
lower = np.array([0,50,50])
upper = np.array([6,255,255])

#色検出しきい値範囲内の色を抽出するマスクを作成
frame_mask1 = cv.inRange(hsv, lower, upper)

#色検出しきい値の設定
lower = np.array([174,50,50])
upper = np.array([180,255,255])

#色検出しきい値範囲内の色を抽出するマスクを作成
frame_mask2 = cv.inRange(hsv, lower, upper)

frame_mask = frame_mask1 + frame_mask2

#論理演算で色検出
dst = cv.bitwise_and(img, img, mask=frame_mask)

# ラベリング結果書き出し用に画像を準備
out_image = dst

# 面積・重心計算付きのラベリング処理を行う
num_labels, label_image, stats, center = cv2.connectedComponentsWithStats(frame_mask)

# 最大のラベルは画面全体を覆う黒なので不要．データを削除
num_labels = num_labels - 1
stats = np.delete(stats, 0, 0)
center = np.delete(center, 0, 0)


if num_labels >= 1:
# 面積最大のインデックスを取得
                max_index = np.argmax(stats[:,4])
                #print max_index

# 面積最大のラベルのx,y,w,h,面積s,重心位置mx,myを得る
                x = stats[max_index][0]
                y = stats[max_index][1]
                w = stats[max_index][2]
                h = stats[max_index][3]
                s = stats[max_index][4]
                mx = int(center[max_index][0])
                my = int(center[max_index][1])
                #print("(x,y)=%d,%d (w,h)=%d,%d s=%d (mx,my)=%d,%d"%(x, y, w, h, s, mx, my) )

                # ラベルを囲うバウンディングボックスを描画
                cv2.rectangle(out_image, (x, y), (x+w, y+h), (255, 0, 255))

                # 重心位置の座標を表示
                # cv2.putText(out_image, "%d,%d"%(mx,my), (x-15, y+h+15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))
                cv2.putText(out_image, "%d"%(s), (x, y+h+15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))
cv.imshow("Image",out_image)
if cv.waitKey(0) & 0xFF == ord('q'):
    cv.destroyAllWindows()

