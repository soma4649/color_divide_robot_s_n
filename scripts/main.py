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

import moveit_commander
import geometry_msgs.msg
from tf.transformations import quaternion_from_euler
import cv2
import os
import numpy as np
import math
import rospy, sys, time, actionlib
import moveit_commander
import geometry_msgs.msg
import rosnode
import math
from std_msgs.msg import Float64
from std_msgs.msg import Int32
from control_msgs.msg import GripperCommandAction, GripperCommandGoal, FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from tf.transformations import quaternion_from_euler
from trajectory_msgs.msg import JointTrajectoryPoint

global Once_flag
n = 0

class ArmJointTrajectoryExample(object):
    def __init__(self):
        self._client = actionlib.SimpleActionClient(
            "/crane_x7/arm_controller/follow_joint_trajectory", FollowJointTrajectoryAction)
        rospy.sleep(0.1)
        if not self._client.wait_for_server(rospy.Duration(secs=5)):
            rospy.logerr("Action Server Not Found")
            rospy.signal_shutdown("Action Server Not Found")
            sys.exit(1)

    def move_arm(self, joint_values, secs):
        
        goal = FollowJointTrajectoryGoal()
        goal.trajectory.joint_names = ["crane_x7_shoulder_fixed_part_pan_joint", "crane_x7_shoulder_revolute_part_tilt_joint",
                                       "crane_x7_upper_arm_revolute_part_twist_joint", "crane_x7_upper_arm_revolute_part_rotate_joint",
                                       "crane_x7_lower_arm_fixed_part_joint", "crane_x7_lower_arm_revolute_part_joint", "crane_x7_wrist_joint"]
        point = JointTrajectoryPoint()
        for p in joint_values:            
            point.positions.append(math.radians(p))           
        point.time_from_start = rospy.Duration(secs)
        goal.trajectory.points.append(point)
        self._client.send_goal(goal)
        
    def wait(self, timeout=0.1):   
        self._client.wait_for_result(timeout=rospy.Duration(timeout))
        return self._client.get_result()
        

class GripperClient(object):
    def __init__(self):
        self._client = actionlib.SimpleActionClient("/crane_x7/gripper_controller/gripper_cmd",GripperCommandAction)
        self.clear()

        if not self._client.wait_for_server(rospy.Duration(10.0)):
            rospy.logerr("Exiting - Gripper Action Server Not Found.")
            rospy.signal_shutdown("Action Server not found.")
            sys.exit(1)

    def command(self, position, effort):
        self._goal.command.position = position
        self._goal.command.max_effort = effort
        self._client.send_goal(self._goal,feedback_cb=self.feedback)
        
    def feedback(self,msg):
        print("feedback callback")
        print(msg)

    def stop(self):
        self._client.cancel_goal()

    def wait(self, timeout=0.1):
        self._client.wait_for_result(timeout=rospy.Duration(timeout))
        return self._client.get_result()

    def clear(self):
        self._goal = GripperCommandGoal()


# 結果の出力
result = [0, 0, 0, 0, 0, 0]

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
            img_0 = frame[0:540, 0:960]
            img_1 = frame[0:540, 960:1920]
            img_2 = frame[540:1080, 0:960]
            img_3 = frame[540:1080, 960:1920]
            cv2.imwrite('{}_{}.{}'.format(base_path, 'original', 'jpg'), frame)
            cv2.imwrite('{}_{}.{}'.format(base_path, 'original_0', 'jpg'), img_0)
            cv2.imwrite('{}_{}.{}'.format(base_path, 'original_1', 'jpg'), img_1)
            cv2.imwrite('{}_{}.{}'.format(base_path, 'original_2', 'jpg'), img_2)
            cv2.imwrite('{}_{}.{}'.format(base_path, 'original_3', 'jpg'), img_3)
            
            detection_collar_red(img_0, base_path, 0)
            detection_collar_red(img_1, base_path, 1)
            detection_collar_red(img_2, base_path, 2)
            detection_collar_red(img_3, base_path, 3)
        
            break
    cv2.destroyWindow(window_name)

# 画像データから色を判定する
def detection_collar_red(frame, base_path, file_num):
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

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

    global n #繰り返し関数
    
    # ブロックの座標
    ball_position = {'x': 0, 'y': 0, 'z': 0}
    box_position = {'x': 0, 'y': 0}
    if ball_num == 0:
        ball_position['x'] = 0.35
        ball_position['y'] = 0.175
        ball_position['z'] = 0.1
    elif ball_num == 1:
        ball_position['x'] = 0.35
        ball_position['y'] = 0.275
        ball_position['z'] = 0.1
    elif ball_num == 2:
        ball_position['x'] = 0.25
        ball_position['y'] = 0.175
        ball_position['z'] = 0.1
    elif ball_num == 3:
        ball_position['x'] = 0.25
        ball_position['y'] = 0.275
        ball_position['z'] = 0.1
    elif ball_num == 4:
        ball_position['x'] = 0.15
        ball_position['y'] = 0.175
        ball_position['z'] = 0.1
    else:
        ball_position['x'] = 0.15
        ball_position['y'] = 0.275
        ball_position['z'] = 0.1
        
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
    
    if n == 0 or n == 3:    #赤色のブロックを投げ入れる
        print("赤")
        print(n)
        jt = ArmJointTrajectoryExample()
        gc = GripperClient()

        joint_values = [25.0, 40.0, 0, 0, 0, 0, 0]
        secs=2.0
        jt.move_arm(joint_values, secs)
        jt.wait(2.0)

        gripper.set_joint_value_target([0.4, 0.4])
        gripper.go()
       
        arm = moveit_commander.MoveGroupCommander("arm")
        # 駆動速度を調整する
        arm.set_max_velocity_scaling_factor(0.7)
        arm.set_max_acceleration_scaling_factor(1.0)

        joint_values = [25.0, -75.0, 0, 0, 0, 0, 0]
        secs=0.5
        jt.move_arm(joint_values, secs)
        jt.wait(0.5)

        n += 1
     
    elif n == 1 or n == 4:   #緑色のブロックを投げ入れる
        print("緑")
        print(n)

        jt = ArmJointTrajectoryExample()
        gc = GripperClient()

        joint_values = [ 0, 40.0, 0, 0, 0, 0, 0]
        secs=2.0
        jt.move_arm(joint_values, secs)
        jt.wait(2.0)

        gripper.set_joint_value_target([0.4, 0.4])
        gripper.go()

        arm = moveit_commander.MoveGroupCommander("arm")
        # 駆動速度を調整する
        arm.set_max_velocity_scaling_factor(0.7)
        arm.set_max_acceleration_scaling_factor(1.0)

        joint_values = [ 0, -75.0, 0, 0, 0, 0, 0]
        secs=0.5
        jt.move_arm(joint_values, secs)
        jt.wait(0.5)

        n += 1

    elif n == 2 or n == 5:   #その他のブロックを投げ入れる
        print("その他")
        print(n)

        jt = ArmJointTrajectoryExample()
        gc = GripperClient()

        joint_values = [ -25.0, 40.0, 0, 0, 0, 0, 0]
        secs=2.0
        jt.move_arm(joint_values, secs)
        jt.wait(2.0)

        gripper.set_joint_value_target([0.4, 0.4])
        gripper.go()

        arm = moveit_commander.MoveGroupCommander("arm")
        # 駆動速度を調整する
        arm.set_max_velocity_scaling_factor(0.7)
        arm.set_max_acceleration_scaling_factor(1.0)

        joint_values = [-25.0,-75.0, 0, 0, 0, 0, 0]
        secs=0.5
        jt.move_arm(joint_values, secs)
        jt.wait(0.5)

        n += 1


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
   
