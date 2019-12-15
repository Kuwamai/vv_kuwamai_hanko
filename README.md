# [WIP] vv_kuwamai_hanko
![](https://gyazo.com/d4db7bdcbe0a223d929492ad16cb8371/raw)

## Description
受信、印刷、押印、投稿を繰り返すロボットです。  
書類を印刷しては無責任に判子を押します。  
本リポジトリはまだ開発中で下記手順に沿っても実行することはできません。

動作している様子↓  
[押印ロボット_紹介映像](https://youtu.be/dkK9gP4Uo3w)

下記の作業を繰り返し実行します。

1. ハッシュタグ付きTweetを受信
1. Tweetを印刷
1. 印刷した書類に押印
1. 押印した書類をカメラで撮影
1. 撮影した画像をTweet

実際のTweetはこちらから見ることができます↓  
https://twitter.com/vv_kuwamai

## Requirements
* Ubuntu18.04
* ROS Melodic
* ロボット本体

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

実行するデバイスの時間がずれているとTweetの取得に失敗するので、その際は下記コマンドを実行します。

```
$ curl -SsfL https://git.io/set_date | sh
```

下記コマンドを実行して起動します。

```
$ roslaunch vv_kuwamai_apps vv_control.launch
```

## License
This repository is licensed under the MIT license, see [LICENSE](./LICENSE).
