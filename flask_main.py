from flask import Flask,  render_template, request, redirect, url_for,jsonify
from werkzeug.utils import secure_filename
import os
from datetime import timedelta
from PIL import Image

from inference import inference_and_save_mask

app = Flask(__name__)
app.config['UPLOAD_POLDER'] = 'static/images/'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

# 进入主页
@app.route('/index',methods=['GET','POST'])
def index():
    return render_template('index.html')

# 上传图片后立即显示
@app.route('/load_uploaded_image',methods=['POST'])
def load_and_show_image():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(
        app.config['UPLOAD_POLDER'], filename)
    )
    img = Image.open(os.path.join(
        app.config['UPLOAD_POLDER'], filename))
    if(img.size[0] > 1000):
        width = 1000
        height = width * img.size[1]/img.size[0]
        img = img.resize((int(width), int(height)), resample=Image.BILINEAR)

    if (img.size[1] > 1000):
        height = 1000
        width = height * img.size[0] / img.size[1]
        img = img.resize((int(width), int(height)), resample=Image.BILINEAR)
    img.save(os.path.join(
        app.config['UPLOAD_POLDER'], filename))

    url = app.config['UPLOAD_POLDER'] + filename
    return jsonify({
        "image_url": url
    })

# 接收ajax发送的图片进行推理，返回mask的路径
@app.route('/infer',methods=['POST'])
def infer():
    filename = secure_filename(request.values.get("image_name"))
    inference_and_save_mask(filename)
    mask_name = filename.split('.')[0]
    url2 = 'static/masks/' + mask_name + '.png'
    url3 = 'static/objects/' + mask_name + '.png'
    return jsonify({
        "mask_url":url2,
        "object_url":url3
    })

if __name__ == '__main__':
    app.run(debug=True)