# [WIP] vv_kuwamai_hanko
![](https://gyazo.com/d4db7bdcbe0a223d929492ad16cb8371/raw)

## Description
* 書類を印刷しては無責任に判子を押すロボットです
  1. ハッシュタグ付きTweetを受信すると書類っぽい形式にして印刷
  2. 印刷された書類にロボットが押印し、その書類を撮影してTweet
* 動作している様子↓   
  * [押印ロボット_紹介映像](https://youtu.be/dkK9gP4Uo3w) 
* 実際のTweetはこちらで見ることができます↓
  * https://twitter.com/vv_kuwamai

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
