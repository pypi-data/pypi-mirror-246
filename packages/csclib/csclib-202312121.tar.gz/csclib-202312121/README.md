# csclib
秘密分散に基づく秘匿計算ライブラリ

## 環境
3台のPCで計算を行います（1台でも可）．それぞれを server, party_1, party_2 とします．
server は入力データを平文で受け取って，それをシェアに変換し，party 1, 2 に送ります．また，相関乱数を生成し party 1, 2 に送ります．
現状では，server では答え合わせ用に全ての計算を平文で行っています．
party_１ と party_2 は相互に通信を行いながら計算をします． 

## コンパイル
C言語またはC++で #include "share.h" して使います．(LOUDSを使う場合は #include "LOUDS.h")
party の番号を -1 として実行すると，全ての計算を1台で（平文で）行います．アルゴリズムの確認や，MPCによる速度低下を評価する際に使えます．

## 実行
config.txt に3台のPCのIPアドレスとポートを設定します．
```config.txt
127.0.0.1 9800 # server
127.0.0.1 9810 # party 1
127.0.0.1 9820 # party 2
```
各行がPCのIPアドレスと使用するポートですが，ポートはここに書かれた値から3つ分を使います．
（この例ではサーバの場合，9800, 9801, 9802 を使います）
1台のPCで実行する場合，全てのIPアドレスを localhost (127.0.0.1) にします．ポート番号は全てが異なるようにします．
複数台ある場合にはそれぞれのIPアドレスを指定します．なお，他のPCと通信を行う場合にはPCのファイアーウォールの設定を変える必要があります．

実行ファイル名を share.out とすると，3台のPC（ターミナル）それぞれで実行します．
```
@server:$ ./share.out 0
@party_1:$ ./share.out 1
@party_2:$ ./share.out 2
```

## Python
コンパイルと実行方法．
```
@server:$ python3 -m venv env
@server:$ source env/bin/activate
@server:$ cd python/csclib
@server:$ python3 setup.py build
@server:$ pip3 install .
```

PyPIからのインストール
```
@server:$ sudo apt install gcc python3.10-dev python3.10-venv python3-pip
@server:$ python3 -m venv env
@server:$ source env/bin/activate
(env) @server:$ pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ csclib
```

pythonのソース内では
```
from csclib import *
```
とする．
