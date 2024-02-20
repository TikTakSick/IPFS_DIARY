from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from pinata_python.pinning import Pinning
import datetime
import requests
import sys
sys.path.append("../")
import settings


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ipfs_dairy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# データベース定義
class IpfsDiary(db.Model):
    cid = db.Column(db.String(46), primary_key=True)
    timestamp_title= db.Column(db.String(128), nullable=False)

@app.route("/")
def hello():
    return redirect(url_for("index"))

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/get_all_dairy")
def get_all_dairy_pinned_by_ipfs():
    ipfs_diaries = IpfsDiary.query.all()
    return render_template("dairy.html", ipfs_diaries=ipfs_diaries, PUBLIC_CLOUD_GATEWAY_URL=settings.PUBLIC_CLOUD_GATEWAY_URL)

# response = requests.get(full_url)
# print(response.text)

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/dairy_form")
def show_dairy_form():
    return render_template("dairy_form.html")

@app.route("/update", methods=["POST", "GET"])
def make_new_dairy():
    if request.method == "POST":
        # タイトルと中身の設定
        dairy_title = request.form["title"]
        dairy_content = request.form["dairy"]

        # タイムスタンプと日付データを取得
        now = datetime.datetime.now()
        now_ts = datetime.datetime.timestamp(now)
        date_string = now.strftime("%Y-%m-%d %H:%M:%S")

        # ipfsに送るデータの準備
        dairy_content_json = {
            "title": dairy_title, 
            "dairy_content": dairy_content, 
            "date": date_string, 
            "timestamp": now_ts,
        }
        options = {
            'pinataMetada':{
                'name': str(now_ts)+dairy_title
            }
        }
        # ipfsにデータを送る
        pinata = Pinning(AUTH="jwt", PINATA_JWT_TOKEN=settings.PINATA_JWT)
        response = pinata.pin_json_to_ipfs(dairy_content_json, options=options)
        print(response)
            
        # データ送信後，cidを取得する
        cid = response["IpfsHash"]
        print(cid)
        # 日記のメタデータをデータベースに格納する．
        ipfs_diary = IpfsDiary(
            cid=cid,
            timestamp_title=date_string+"_"+dairy_title
        )
        db.session.add(ipfs_diary)
        db.session.commit()
        return redirect(url_for("index"))
        # except:
        #     return redirect(url_for("error"))
    
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)