## S・N班の目標

4色(赤、緑、青、黃)のブロックから指定された２色(赤、緑)をそれぞれ同じ色紙の上に仕分け, 残りの二色(青、黃)は別の色紙(青)に置かれます。 全部で６つのブロックと３つの色紙を使い、ブロックは赤色が２つ、緑色が２つ、青色が１つ、黄色が１つ、色紙は赤色が１つ、緑色が１つ、青色が１つです。物体と色紙の色の位置はそれぞれ入れ替えても仕分けが可能なようにします。また、最終的には色紙３つにそれぞれ２つのブロックが積まれている形となります。


## 使用する物体の詳細について


### 4色のブロック

製造方法：３Dプリンター　材質：　　　　　寸法：４×４×４cm　重量：


### ３色の色紙

製造方法：３Dプリンター　材質：　　　　　寸法：20×10×1cm　重量：



## 参考にしたサイト


### zageboへの色の付け方

　・ROS講座87 Gazebo世界を明るくする [こちら](https://qiita.com/srs/items/49e71932c1ef469b3049)
　・gazeboを使いこなす！ [こちら](https://qiita.com/Karin-Sugi/items/4918168649a8fb9b35d3)

 
### 画像処理について
    
　・色空間の変換 [こちら](http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html)


### README.mの書き方について

　・GitHub – READMEの作成方法と書き方 [こちら](https://howpon.com/8334)

 
## 苦戦した点


#### 自分のリポジトリのmodelをgazeboに表示させる　　　

 解決策⇒

 ~/.bashrcの中を以下のように書き換えることでパスが通り、モデルが表示されるようになる。

 ```
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash
export ROS_MASTER_URI=http://localhost:11311
export ROS_HOSTNAME=localhost
export GAZEBO_MODEL_PATH=$HOME/catkin_ws/src/color_divide_robot_s_n/models:$GAZEBO_MODEL_PATH
```
今回はcolor_divide_robot_s_n/modelsとなっているが、ここの部分は自分が表示させたいファイルに変更する。


### gazeboのmodelに色をつける。　　　

 解決策⇒

 モデルのsdfファイルの中を書き換える。書き換え方は以下の通り。
 
 sdfファイルの<visual>の中の<material>に以下のコードを記述。

 <赤色の場合>

 ```
<visual name="visual">
        <geometry>
          <box>
            <size>0.04 0.04 0.04</size>
          </box>
        </geometry>
        <material>
         <ambient>1 0 0 1</ambient>
         <diffuse>1 0 0 1</diffuse>
	 <specular>0.1 0.1 0.1 1</specular>
	 <emissive>0 0 0 0</emissive>
        </material>
      </visual>
```
 geometryはシュミレーションに表示させる物体の"見える"大きさを、materialはシュミレーションに表示させる物体の材質や見え方を変更できる。

 他の色を使いたい場合は、ambientとdiffuseを変更する。

 <例>

青色　ambientを0 0 1 1、diffuseを0 0 1 1に変更。

緑色　ambientを0 1 0 1、diffuseを0 1 0 1に変更。

黃色　ambientを1 1 0 1、diffuseを1 1 0 1に変更。







 
 
