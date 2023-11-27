#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2023 TakeruSoma
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rospy
import moveit_commander
import geometry_msgs.msg
import rosnode
from tf.transformations import quaternion_from_euler
import cv2
import os
import numpy as np

import math

# 色判定したボールがゴミか貴重品か（1: 貴重品、0: ゴミ）
result = [0, 0, 0, 0, 0, 0]

# acquisition_image.pyの内容

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
    
# カメラを使わず画像を使用する場合はこちらを使用する
def read_image(image, basename):
    img = cv2.imread(os.getcwd() + '/data/temp/' + image)
    base_path = os.path.join('data/temp', basename)
 
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


# 画像データから色を判定する
def detection_collar_red(frame, base_path, file_num):
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    import rospy
import moveit_commander
import geometry_msgs.msg
import rosnode
from tf.transformations import quaternion_from_euler
import cv2
import os
import numpy as np

import math

# 色判定したボールがゴミか貴重品か（1: 貴重品、0: ゴミ）
result = [0, 0, 0, 0, 0, 0]

# acquisition_image.pyの内容

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
    
# カメラを使わず画像を使用する場合はこちらを使用する
def read_image(image, basename):
    img = cv2.imread(os.getcwd() + '/data/temp/' + image)
    base_path = os.path.join('data/temp', basename)
 
    img_0 = frame[0:540, 0:640]
    img_1 = frame[0:540, 640:1280]
    img_2 = frame[0:540, 1280:1920]
    img_3 = frame[540:1080, 0:640]
    # 色の範囲を指定する
    lower_color = np.array([0, 64, 0])
    upper_color = np.array([5, 255, 255])
    
    # 指定した色に基づいたマスク画像の生成
    mask = cv2.inRange(hsv, lower_color, upper_color)
    masked_image = cv2.bitwise_and(hsv, hsv, mask = mask)
        
    cv2.imwrite('{}_{}_{}.{}'.format(base_path, 'mask', file_num, 'jpg'), masked_image)
    
    # ラベリング結果書き出し用に画像を準備
    out_image = masked_image
    
    num_labels, label_image, stats, center = cv2.connectedComponentsWithStats(mask)

    # 最大のラベルは画面全体を覆う黒なので不要．データを削除
    num_labels = num_labels - 1
    stats = np.delete(stats, 0, 0)
    center = np.delete(center, 0, 0)

    
    # 検出したラベルの数だけ繰り返す
    for index in range(num_labels):
        if stats[index][4] > 40000:
            # resultに判定結果を代入
            result[file_num] = 1
    
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

# acquisition_image.pyの内容 end

# 準備体制に移動する。
def pre_position():
    rospy.init_node("crane_x7_pick_and_place_controller")
    robot = moveit_commander.RobotCommander()
    arm = moveit_commander.MoveGroupCommander("arm")
    arm.set_max_velocity_scaling_factor(0.1)
    arm.set_max_acceleration_scaling_factor(1.0)
    gripper = moveit_commander.MoveGroupCommander("gripper")
    target_pose = geometry_msgs.msg.Pose()
    target_pose.position.x = 0.15
    target_pose.position.y = 0.14
    target_pose.position.z = 0.32
    q = quaternion_from_euler(-3.14, 0.0, -6.28/2.0)
    target_pose.orientation.x = q[0]
    target_pose.orientation.y = q[1]
    target_pose.orientation.z = q[2]
    target_pose.orientation.w = q[3]
    arm.set_pose_target(target_pose)
    arm.go()  # 実行する。

# ボールを掴んでかごに入れる。（box_num: ゴミ->0, 貴重品->1）
def move(ball_num, box_num):
    rospy.init_node("crane_x7_pick_and_place_controller")
    robot = moveit_commander.RobotCommander()
    arm = moveit_commander.MoveGroupCommander("arm")
    arm.set_max_velocity_scaling_factor(0.1)
    arm.set_max_acceleration_scaling_factor(1.0)
    gripper = moveit_commander.MoveGroupCommander("gripper")
    
    # ブロックの座標
    ball_position = {'x': 0, 'y': 0, 'z': 0}
    box_position = {'x': 0, 'y': 0}
    if ball_num == 0:
        ball_position['x'] = 0.35
        ball_position['y'] = 0.175
        ball_position['z'] = 0.12
    elif ball_num == 1:
        ball_position['x'] = 0.35
        ball_position['y'] = 0.275
        ball_position['z'] = 0.12
    elif ball_num == 2:
        ball_position['x'] = 0.25
        ball_position['y'] = 0.175
        ball_position['z'] = 0.12
    elif ball_num == 3:
        ball_position['x'] = 0.25
        ball_position['y'] = 0.275
        ball_position['z'] = 0.12
    elif ball_num == 4:
        ball_position['x'] = 0.15
        ball_position['y'] = 0.175
        ball_position['z'] = 0.12
    else:
        ball_position['x'] = 0.15
        ball_position['y'] = 0.275
        ball_position['z'] = 0.12
        
    # 箱の座標
    if box_num == 0:
        box_position['x'] = 0.4
        box_position['y'] = 0.0
        box_position['z'] = 0.25
    elif box_num == 1:
        box_position['x'] = 0.4
        box_position['y'] = 0.0
        box_position['z'] = 0.25
    
    # ハンドを開く
    gripper.set_joint_value_target([0.8, 0.8])
    gripper.go()

    # 掴む 
    target_pose = geometry_msgs.msg.Pose()
    target_pose.position.x = ball_position['x']
    target_pose.position.y = ball_position['y']
    target_pose.position.z = ball_position['z']
    q = quaternion_from_euler(-3.14, 0.0, -1.14/2.0)  # 上方から掴みに行く場合
    target_pose.orientation.x = q[0]
    target_pose.orientation.y = q[1]
    target_pose.orientation.z = q[2]
    target_pose.orientation.w = q[3]
    arm.set_pose_target(target_pose)  # 目標ポーズ設定
    arm.go()  # 実行

    # ハンドを閉じる
    if box_num == 0:
        gripper.set_joint_value_target([0.2, 0.2])
    else:
        gripper.set_joint_value_target([0.2, 0.2])
    gripper.go()

    # 持ち上げる 
    target_pose = geometry_msgs.msg.Pose()
    target_pose.position.x = ball_position['x']
    target_pose.position.y = ball_position['y']
    target_pose.position.z = ball_position['z']
    q = quaternion_from_euler(-3.14, 0.0, -3.14/2.0)  # 上方から掴みに行く場合
    target_pose.orientation.x = q[0]
    target_pose.orientation.y = q[1]
    target_pose.orientation.z = q[2]
    target_pose.orientation.w = q[3]
    arm.set_pose_target(target_pose)  # 目標ポーズ設定
    arm.go()	

    arm = moveit_commander.MoveGroupCommander("arm")
    # 駆動速度を調整する
    arm.set_max_velocity_scaling_factor(0.1)
    arm.set_max_acceleration_scaling_factor(0.1)

    # SRDFに定義されている"vertical"の姿勢にする
    # すべてのジョイントの目標角度が0度になる
    arm.set_named_target("vertical")
    arm.go()

    gripper.set_joint_value_target([0.4, 0.4])
    gripper.go()

    arm = moveit_commander.MoveGroupCommander("arm")
    # 駆動速度を調整する
    arm.set_max_velocity_scaling_factor(0.7)
    arm.set_max_acceleration_scaling_factor(1.0)

    # 投げる
    target_pose = geometry_msgs.msg.Pose()
    target_pose.position.x = 0.4
    target_pose.position.y = 0
    target_pose.position.z = 0.25
    q = quaternion_from_euler(-3.14, 0.0, -3.14/2.0)  # 上方から掴みに行く場合
    target_pose.orientation.x = q[0]
    target_pose.orientation.y = q[1]
    target_pose.orientation.z = q[2]
    target_pose.orientation.w = q[3]
    arm.set_pose_target(target_pose)  # 目標ポーズ設定
    arm.go()  # 実行

def main():
    rospy.init_node("crane_x7_pick_and_place_controller")
    robot = moveit_commander.RobotCommander()
    arm = moveit_commander.MoveGroupCommander("arm")
    arm.set_max_velocity_scaling_factor(0.1)
    arm.set_max_acceleration_scaling_factor(1.0)
    gripper = moveit_commander.MoveGroupCommander("gripper")

    while len([s for s in rosnode.get_node_names() if 'rviz' in s]) == 0:
        rospy.sleep(1.0)
    rospy.sleep(1.0)

    # アーム初期ポーズを表示
    arm_initial_pose = arm.get_current_pose().pose
    print("Arm initial pose:")
    print(arm_initial_pose)

    # 何かを掴んでいた時のためにハンドを開く
    gripper.set_joint_value_target([0.9, 0.9])
    gripper.go()

    # SRDFに定義されている"home"の姿勢にする
    arm.set_named_target("home")
    arm.go()
    gripper.set_joint_value_target([0.7, 0.7])
    gripper.go()
    
    # bring_arm_above_ball.pyの内容
    pre_position()
    
    # acquisition_image.pyの内容
    save_frame_camera(6, 'camera_capture')
    # read_image('sample_1.jpg', 'camera_capture')
    
    
    # 判定結果を出力する。
    print("判定結果: ")
    print("左上: " + str(result[0]))
    print("中上: " + str(result[1]))
    print("右上: " + str(result[2]))
    print("左下: " + str(result[3]))
    print("中下: " + str(result[4]))
    print("右下: " + str(result[5]))
    
    # 判定結果をもとにボールを移動させる。
    for index, result_one in enumerate(result):
        move(index, result_one)
        pre_position()
            
    # SRDFに定義されている"home"の姿勢にする
    arm.set_named_target("home")
    arm.go()
    gripper.set_joint_value_target([0.7, 0.7])
    gripper.go()
    
    
    
    return

if __name__ == '__main__':

    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass
   
