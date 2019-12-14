# [WIP] vv_kuwamai_hanko

## Description
受信、印刷、押印、投稿を繰り返すロボットです。  
まだ開発中で色々散らかってます。  

下記の作業を繰り返し実行します。

1. ハッシュタグ付きTweetを受信
1. Tweetを印刷
1. 印刷した書類に押印
1. 押印した書類をカメラで撮影
1. 撮影した画像をTweet

## Requirements
* Ubuntu18.04
* ROS Melodic

## Installation
下記コマンドで本リポジトリをクローン、ビルドします。
```
$ cd ~/catkin_ws/src
$ git clone https://github.com/Kuwamai/vv_kuwamai_hanko.git
$ cd ~/catkin_ws && catkin_make
$ source ~/catkin_ws/devel/setup.bash
```

## Usage
サーボモータと通信するため、/dev/ttyUSB0へのアクセス権を付与します。

```
$ sudo chmod 666 /dev/ttyUSB0
```

下記コマンドを実行して起動します。

```
$ roslaunch vv_kuwamai_apps vv_control.launch
```

## License
This repository is licensed under the MIT license, see [LICENSE](./LICENSE).
