from flask import Flask,render_template, redirect, url_for, request, jsonify
from pinata_python.pinning import Pinning
import settings
import requests
import datetime



app = Flask(__name__)

@app.route("/")
def hello():
    return redirect(url_for("index"))

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/all_daily")
def get_all_daily_pinned_by_ipfs():
    cid = "QmeQsPBWHCQCPRNK16dWFUXNZ2BXqUPWmKoLQDKowMvaNG"
    full_url = settings.PUBLIC_GATEWAY_URL+cid
    response = requests.get(full_url)
    print(response.text)
    return render_template("daily.html")

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/daily_form")
def show_daily_form():
    return render_template("daily_form.html")

@app.route("/update", methods=["POST", "GET"])
def make_new_daily():
    if request.method == "POST":
        # タイトルと中身の設定
        daily_title = request.form["title"]
        daily_content = request.form["daily"]
        now = datetime.datetime.now()
        now_ts = datetime.datetime.timestamp(now)
        date_string = now.strftime("%Y-%m-%d %H:%M:%S")

        # ipfsに送るデータの準備
        daily_content_json = {"title": daily_title, 
                              "daily_content": daily_content, 
                              "date": date_string, 
                              "timestamp": now_ts}
        print(daily_content_json)
        options = {'pinataMetada':{
            'name': str(now_ts)+daily_title
        }}
        # ipfsにデータを送る
        pinata = Pinning(AUTH="jwt", PINATA_JWT_TOKEN=settings.PINATA_JWT)

        try:
            response = pinata.pin_json_to_ipfs(daily_content_json, options=options)
            print(response)
            cid = response["IpfsHash"]

            # fetch data
            full_url = settings.PUBLIC_GATEWAY_URL+cid
            print(full_url)
            response = requests.get(full_url)
            print(response.text)
            return redirect(url_for("index"))
        except:
            return redirect(url_for("error"))
    
    return redirect(url_for("index"))

# @app.route("/update", methods="POST")
# def make_new_daily():

#     try:
#         return redirect(url_for("index"))
#     except:
#         print("Error Uploading")
#         return redirect(url_for("error"))

#     # cid(hash値)の保管
#     filepath = './hello.txt'
#     response = pinata.pin_file_to_ipfs(filepath)
#     cid = response.IpfsHash

if __name__ == "__main__":
    app.run(debug=True)