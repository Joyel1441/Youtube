from flask import Flask,render_template,request,send_from_directory
from pytube import YouTube
import os
import glob

app = Flask(__name__)

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/form",methods=["POST"])
def form():
 if request.method == "POST":
     #get url and resolution
     url = request.form["url"]
     res = request.form["res"]
     try:
        # get video
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, mime_type = "video/mp4")
        title = yt.title
        # download video 
        if res == "high_res":
           video[-1].download("./videos")
        elif res == "low_res":
           video[0].download("./videos")
           
        @app.after_request
        def remove_file(response):
            # clear downloaded video after sending it
            if os.path.exists("./videos/"+title+".mp4"):
                os.remove("./videos/"+title+".mp4")
            return response
        # send the downloaded video to the user
        return send_from_directory(directory="./videos", filename=title+".mp4", as_attachment=True)
     except:
        return render_template("index.html",error="Error")
     return render_template("index.html",error="Error") 
    
if __name__ == "__main__":
  app.run()