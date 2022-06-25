from flask import Flask,request,render_template
import PIL
from PIL import Image
import main1
from main1 import ocr
import os


app=Flask(__name__) #name of the application is app

@app.route('/', methods=['POST','GET'])
def upload():
    if request.method=='POST':
        f=request.files['file']        
        f.save(f.filename)
        pr=ocr(f.filename)
        nam=f.filename
        os.remove(f.filename)        
        return render_template('file_upload.html',name=nam)        
    return render_template('file_upload.html')


if __name__=="__main__":
    app.run(host="localhost",port=6400,debug=True)