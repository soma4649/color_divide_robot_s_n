#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import os
import numpy as np

# 画像データを取り出す
def save_frame_camera(device_num, basename, ext='jpg', delay=1, window_name='frame'):
    cap = cv2.VideoCapture(device_num)

    if not cap.isOpened():
        return

    os.makedirs('data/temp', exist_ok=True)
    base_path = os.path.join('data/temp', basename)

    n = 0
    while True:
        ret, frame = cap.read()
        cv2.imshow(window_name, frame)
        n += 1
        if n == 100:
            img_0 = frame[0:540, 0:640]
            img_1 = frame[0:540, 640:1280]
            img_2 = frame[0:540, 1280:1920]
            img_3 = frame[540:1080, 0:640]
            img_4 = frame[540:1080, 640:1280]
            img_5 = frame[540:1080, 1280:1920]

            cv2.imwrite('{}_{}.{}'.format(base_path, 'original', 'jpg'), frame)
            cv2.imwrite('{}_{}.{}'.format(base_path, 'original_0', 'jpg'), img_0)
            cv2.imwrite('{}_{}.{}'.format(base_path, 'original_1', 'jpg'), img_1)
            cv2.imwrite('{}_{}.{}'.format(base_path, 'original_2', 'jpg'), img_2)
            cv2.imwrite('{}_{}.{}'.format(base_path, 'original_3', 'jpg'), img_3)
            cv2.imwrite('{}_{}.{}'.format(base_path, 'original_4', 'jpg'), img_4)
            cv2.imwrite('{}_{}.{}'.format(base_path, 'original_5', 'jpg'), img_5)
            
            detection_collar_red(img_0, base_path, 0)
            detection_collar_red(img_1, base_path, 1)
            detection_collar_red(img_2, base_path, 2)
            detection_collar_red(img_3, base_path, 3)
            detection_collar_red(img_4, base_path, 4)
            detection_collar_red(img_5, base_path, 5)
        
            break
    cv2.destroyWindow(window_name)

# 画像データから色を判定する
def detection_collar_red(frame, base_path, file_num):
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
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

    
    # 検出したラベルの数だけ繰り返す
    for index in range(num_labels):
        if stats[index][4] > 40000:
    
            # ラベルのx,y,w,h,面積s,重心位置mx,myを取り出す
            x = stats[index][0]
            y = stats[index][1]
            w = stats[index][2]
            h = stats[index][3]
            s = stats[index][4]
            mx = int(center[index][0])
            my = int(center[index][1])
            #print("(x,y)=%d,%d (w,h)=%d,%d s=%d (mx,my)=%d,%d"%(x, y, w, h, s, mx, my) )

            # ラベルを囲うバウンディングボックスを描画
            cv2.rectangle(out_image, (x, y), (x+w, y+h), (255, 0, 255))

            # 重心位置の座標と面積を表示
            cv2.putText(out_image, "%d,%d"%(mx,my), (x-15, y+h+15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))
            cv2.putText(out_image, "%d"%(s), (x, y+h+30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))
    
    cv2.imwrite('{}_{}_{}.{}'.format(base_path, 'output', file_num, 'jpg'), out_image)

    
    return

