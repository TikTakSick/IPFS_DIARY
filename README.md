# ipfsを用いた日記アプリ
- ipfsとの通信には，pinataを使用

# 前提
- ```.env```ファイルをフォルダ下に作成する．
- pinataに登録し，API_KEYを作成する．
- その際，**PINATA_API_KEY**，**PINATA_API_SECRET**，**PINATA_JWT**が表示されるので，全てコピーして，```.env```ファイルではコピーした内容を元に，以下のように設定する．**PUBLIC_GATEWAY_URL**に関しても，pinataから参照する．


```
PINATA_API_KEY="..."
PINATA_API_SECRET="..."
PINATA_JWT="..."
PUBLIC_GATEWAY_URL="..."
```

# 始め方
```
$ python3 run.py
```

- デバッグモードの場合
```
$ cd app
$ python3 app.py
```

