#!/usr/bin/python3

import numpy as np
import cv2
from cv2 import aruco
import matplotlib.pyplot as plt

# マーカー種類を定義
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
# マーカー種類に応じて画像を
ar_id = 4
img_size = 150
ar_img = aruco.drawMarker(aruco_dict, ar_id, img_size)
print("画像サイズ", ar_img.shape)
# 画像表示
plt.imshow(ar_img, cmap = "gray")
# 画像保存
cv2.imwrite(f'{ar_id:02}.png', ar_img)
