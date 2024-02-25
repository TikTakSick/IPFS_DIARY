# IPFSを用いた日記アプリ

- 開発動機：情報を恒久的に保存する仕組みが作りたい．
  - 昔記録として使われていた木簡が今でも発掘され保管されているように，インターネットの情報を恒久的に保管するシステムを作りたい．
  - ※実際，長らくデータを保存するシステムやサービスが出てきている（例：デジタルアーカイブ）

- IPFS
  - [IPFS](https://ipfs.tech/)は，分散ファイルシステムの一種である．
  - ipfs上に置かれたファイルやフォルダのコンテンツのIDは，それらコンテンツの内容を元に作成されたものである．また，ipfsにおいて対象のコンテンツのIDは，CID(content identifier)と呼ばれている．
  - 例：中身が```HELLO```のファイルを複数ipfsに置いたとしても，それらCIDは全て同一である．

## 各フォルダ説明
### ver1
- flaskとSQLAlchemyを用いる．SQLAlchemyには，日記ファイルのCIDとタイムスタンプ付きのタイトルを保存する．ipfsには，日記の内容を記述したテキストファイルを送信する．

### contract_ipfsDiary
- contract_ipfsDiary：スマートコントラクトのデータ．ver1において，SQLAlchemyで保管した情報をブロックチェーン（テストネット）上のスマートコントラクト，ブロックチェーン上にデプロイするために利用する．下記のver2以降で使用予定．
### ver2（予定）
- スマートコントラクトを用いる．ブロックチェーンおよびスマートコントラクトとの通信には，[Infura](https://www.infura.io/)のAPIサービスを活用し，バックエンド(python)側で処理を行う．
### ver3(予定)
- ブロックチェーンとの通信を，フロントエンド(JavaScript)側で行う．また，日記ファイルの拡張子をjsonに設定し，pythonバックエンド処理をなくす．

### ver4(予定)
- [Spheron Network](https://www.spheron.network/)を用いて，日記ファイルおよび，フロントエンドの静的ファイルデータをipfs上に配置するよう設定する．

## 使用するAPIサービス
- [Pinata](https://www.pinata.cloud/)：IPFSとの通信に使用．
- [Infura](https://www.infura.io/)（利用予定）：ブロックチェーンと通信を行いために利用する．
- [Spheron Network](https://www.spheron.network/)（利用予定）：Pinataでは，ipfs上にhtmlファイルの送信するには有料プランに加入する必要がある．無料でhtmlファイルやjsファイルといった静的ファイルを送信可能な
Spheron Networkを使用する．

## その他
- ver2以降ではブロックチェーンとの通信が発生するため，[Metamask](https://chromewebstore.google.com/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn?hl=ja)(ブロックチェーンの通貨やNFTを一括で補完・管理できるソフトウェアウォレット)等でアカウントを作成する必要がある．

# ver1について

## 準備
- ```.env```ファイルをver1フォルダ下に作成する．
- [Pinata](https://www.pinata.cloud/)に登録およびログイン，API_KEYを作成する．
- その際，**API_KEY**，**API_SECRET**，**JWT**が表示される（これら情報は，二度と表示されないので注意）．全てコピーして，コピーした内容を元に，```.env```で下記のように設定する．```.env```内の**PUBLIC_GATEWAY_URL**に関しては，ログイン後の```Gateways```ページで，**DOMAIN**をコピーし，下記のように設定する．

```
PINATA_API_KEY="<API_KEY>"
PINATA_API_SECRET="<API_SECRET>"
PINATA_JWT="<JWT>"
PUBLIC_GATEWAY_URL="https://<DOMAIN>/ipfs/"

# PUBLIC_GATEWAY_URLの例：https://maroon-geographical-xxx-111.mypinata.cloud/ipfs/
```

## 始め方
```
$ cd ver1/app
$ pip install requirements.txt
$ python3 app.py
```


