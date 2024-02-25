from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from pinata_python.pinning import Pinning
import datetime
import requests
import sys, os
import json
sys.path.append("../")
import settings


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ipfs_dairy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

# データベース定義
class IpfsDiary(db.Model):
    cid = db.Column(db.String(46), primary_key=True)
    timestamp_title= db.Column(db.String(128), nullable=False)
    
    def __repr__(self):
        params =  {
                "cid" : self.cid,
                "timestamp_title" : self.timestamp_title

            }
        json_str = json.dumps(params)
        return json_str

@app.route("/")
def hello():
    return redirect(url_for("index"))

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/get_all_dairy")
def get_all_dairy_pinned_by_ipfs():
    ipfs_diaries = IpfsDiary.query.order_by(desc(IpfsDiary.timestamp_title))
    return render_template("dairy.html", ipfs_diaries=ipfs_diaries, PUBLIC_CLOUD_GATEWAY_URL=settings.PUBLIC_GATEWAY_URL)

@app.route("/error")
def error():
    return render_template("error.html")


@app.route("/dairy_form")
def show_dairy_form():
    return render_template("dairy_form.html")

@app.route("/create", methods=["POST", "GET"])
def create_new_dairy():
    if request.method == "POST":
        # タイトルと日記内容を受け取る．
        dairy_title = request.form["title"]
        dairy_content = request.form["dairy"]

        # タイムスタンプと日付データを取得
        now = datetime.datetime.now()
        now_ts = datetime.datetime.timestamp(now)
        date_string = now.strftime("%Y-%m-%d %H:%M:%S")

        # ipfsに送るファイルの作成
        timestamp_title = date_string + "__" + dairy_title
        tmp_save_folder = "dairy_txts/"
        os.makedirs(tmp_save_folder, exist_ok=True)
        dairy_filepath = tmp_save_folder + timestamp_title + ".txt"
        with open(dairy_filepath, "w") as f:
            f.write(dairy_content)

        # ipfsにデータを送る
        pinata = Pinning(PINATA_API_KEY=settings.PINATA_API_KEY, PINATA_API_SECRET=settings.PINATA_API_SECRET)
        response = pinata.pin_file_to_ipfs(dairy_filepath)
        print(response)
            
        # データ送信後，cidを取得する
        cid = response["IpfsHash"]
        # 日記のメタデータをデータベースに格納する．
        ipfs_diary = IpfsDiary(
            cid=cid,
            timestamp_title=timestamp_title
        )
        db.session.add(ipfs_diary)
        db.session.commit()

        # データベース作成までできれば，対象ファイルを削除する．
        os.remove(dairy_filepath)
        return redirect(url_for("index"))
        # except:
        #     return redirect(url_for("error"))
    
    return redirect(url_for("index"))

@app.route("/delete/<string:cid>", methods=["GET"])
def delete_diary_of(cid):
    # 対象ファイルをunpinする．
    pinata = Pinning(AUTH="jwt", PINATA_JWT_TOKEN=settings.PINATA_JWT)
    response = pinata.unpin(cid)
    print(response)
    if response==200:
        # 対象テーブルを削除
        target_diary = IpfsDiary.query.get(cid)
        db.session.delete(target_diary)
        db.session.commit()
        return redirect(url_for("get_all_dairy_pinned_by_ipfs"))
    return redirect(url_for("error"))

if __name__ == "__main__":
    with app.app_context():
        db.session.query(IpfsDiary).delete()
        db.session.commit()
        db.create_all()
    app.run(debug=True)