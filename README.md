# color_divide_robot_s_n
ロボット製作論3のS・N班による課題です。

## 実装内容
 
4色(赤、緑、青、黃)のブロックをアームが投げて、色を仕分けることが出来るサンプルコードです。全部で６つのブロックと３つの箱を使い、ブロックは赤色が２つ、緑色が２つ、青色が１つ、黄色が１つです。
 
 ---
## 動作環境

OS: Ubuntu 20.04.5 LTS


ROS1


Gazebo11


Rviz1.14.10


crane_x7_ros

---
## 環境構築

1 ROSのインストール

```  
$ git clone https://github.com/ryuichiueda/ros_setup_scripts_Ubuntu18.04_desktop.git
$ cd ros_setup_scripts_Ubuntu18.04_desktop/
$ sudo apt update
$ sudo apt upgrade
$ ./locale.ja.bash
$ ./step0.bash
$ ./step1.bash
```

2 動作確認

```  
$ cd     
$ source ~/.bashrc
$ roscore
```

3 ワークスペースを作成し、~/.bashrcを編集

```  
$ cd
$ mkdir -p catkin_ws/src
$ cd ~/catkin_ws/src/
$ catkin_init_workspace
$ cd ..
$ catkin_make
$ vi ~/.bashrc
source /opt/ros/melodic/setup.bash
source ~/catkin_ws/devel/setup.bash       #この行を追加
export ROS_MASTER_URI=http://localhost:11311
$ source ~/.bashrc
$ cd ~/catkin_ws/
$ catkin_make
```

4 CRANE-X7のROSパッケージのインストール

```  
$ cd ~/catkin_ws/src/  
$ git clone https://github.com/rt-net/crane_x7_ros.git
$ git clone https://github.com/roboticsgroup/roboticsgroup_gazebo_plugins.git
$ rosdep install -r -y --from-paths --ignore-src crane_x7_ros
$ ( cd ~/catkin_ws/ && catkin_make )
```  
詳しくは[こちら](https://github.com/rt-net/crane_x7_ros)を参照。

5 RVIZの動作確認

```  
$ source ~/.bashrc
$ roscore &
$ rviz
```

6 GAZEBOの動作確認

```  
$ mkdir ~/.ignition/fuel
$ vi config.yaml
config.yamlに以下を追加
servers:
-
  name: osrf
  url: https://api.ignitionrobotics.org
$ roslaunch crane_x7_gazebo crane_x7_with_table.launch
```
  
7 本パッケージのインストール

```  
$ cd ~/catkin_ws/src  
$ git clone  git@github.com:soma4649/color_divide_robot_s_n.git
$ cd ~/catkin_ws
$ catkin_make
```  

## 使用方法

### シミュレーター起動用コマンド

- **~/.bashrc**内の一番下のコードが、以下になるようにしてください。
```bash
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash
export ROS_MASTER_URI=http://localhost:11311
export ROS_HOSTNAME=localhost
export GAZEBO_MODEL_PATH=$HOME/catkin_ws/src/color_divide_robot_s_n/models:$GAZEBO_MODEL_PATH
```
- 以上が完了したら、以下のコマンドを使用してビルドしてください。
```bash
$ cd ~/catkin_ws/
$ chmod +x src/color_divide_robot_s_n/scripts/main.py
$ catkin_make
$ source ~/.bashrc
```
- 以下のコードを実行
```
export GAZEBO_MODEL_PATH=$HOME/catkin_ws/src/color_divide_robot_s_n/models:$GAZEBO_MODEL_PATH
```
- gazeboを起動
```
roslaunch color_divide_robot_s_n crane_x7_with_table.launch
```
- main.pyより実行
```
rosrun color_divide_robot_s_n main.py
```
### 実機起動用コマンド
- /dev/ttyUSB0へのアクセス権変更のため、以下を実行。

```
sudo chmod 666 /dev/ttyUSB0
```

- 実機起動コマンド
```
roslaunch crane_x7_bringup demo.launch fake_execution:=false
```

- 実行コマンド
```
roslaunch color_divide_robot_s_n try.launch
```

## 著作権

### 知的財産権について  
CRANE-X7は、アールティが開発した研究用アームロボットです。 このリポジトリのデータ等に関するライセンスについては、[LICENSEファイル](https://github.com/soma4649/color_divide_robot_s_n/blob/main/LICENSE)をご参照ください。 企業による使用については、自社内において研究開発をする目的に限り、本データの使用を許諾します。 本データを使って自作されたい方は、義務ではありませんが弊社ロボットショップで部品をお買い求めいただければ、励みになります。 商業目的をもって本データを使用する場合は、商業用使用許諾の条件等について弊社までお問合せください。

サーボモータのXM540やXM430に関するCADモデルの使用については、ROBOTIS社より使用許諾を受けています。 CRANE-X7に使用されているROBOTIS社の部品類にかかる著作権、商標権、その他の知的財産権は、ROBOTIS社に帰属します。  

### Proprietary Rights  
CRANE-X7 is an arm robot developed by RT Corporation for research purposes. Please read [the license information](https://github.com/soma4649/color_divide_robot_s_n/blob/main/LICENSE) contained in this repository to find out more about licensing. Companies are permitted to use CRANE-X7 and the materials made available here for internal, research and development purposes only. If you are interested in building your own robot for your personal use by utilizing the information made available here, take your time to visit our website and purchase relevant components and parts – that will certainly help us keep going! Otherwise, if you are interested in manufacturing and commercializing products based on the information herein, please contact us to arrange a license and collaboration agreement with us.

We have obtained permission from ROBOTIS Co., Ltd. to use CAD models relating to servo motors XM540 and XM430. The proprietary rights relating to any components or parts manufactured by ROBOTIS and used in this product, including but not limited to copyrights, trademarks, and other intellectual property rights, shall remain vested in ROBOTIS.  

### 使用・参考にしたパッケージについて

* README.mdの内容およびコードは、下記のスライド( CC-BY-SA 4.0 by Ryuichi Ueda)のものを参考にしています。
 
  * ryuichiueda/my_slides/robotdesign3_2021/lesson1.md[[Github Pages](https://ryuichiueda.github.io/my_slides/robotdesign3_2021/lesson1.html#/3)]

* main.pyのコードは、2021-RobotDesign3-team2さんとtakanezawa0829さんのパッケージを参考にしています。
  * 2021-RobotDesign3-team2[[Github Pages](https://github.com/2021-RobotDesign3-team2/crane_x7_ros_test)] ライセンスは[こちら](https://github.com/2021-RobotDesign3-team2/crane_x7_ros_test/blob/main/LICENSE)
  * takanezawa0829[[Github Pages](https://github.com/takanezawa0829/automatic_sorting_machine)] ライセンスは[こちら](https://github.com/takanezawa0829/automatic_sorting_machine/blob/master/LICENSE)

