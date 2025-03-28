from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
import logging
import requests
from utils import generate_id

# 設置日誌
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# 設置上傳文件夾
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# LINE API 設置
CHANNEL_ACCESS_TOKEN = 'YOUR_CHANNEL_ACCESS_TOKEN'  # 替換為您的 Channel Access Token
GROUP_ID = 'YOUR_GROUP_ID'  # 替換為您的群組 ID

# 發送訊息到 LINE 群組
def send_line_message(message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "to": GROUP_ID,
        "messages": [{
            "type": "text",
            "text": message
        }]
    }
    response = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=data)
    return response.json()

@app.route('/')
def index():
    return redirect('/upload')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            # 生成唯一的文件 ID
            file_id = generate_id()
            filename = file_id + '.jpg'
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # 創建圖片查看鏈接
            view_url = f'/view?id={file_id}'

            # 發送圖片查看鏈接到 LINE 群組
            message = f"新圖片已上傳！查看圖片：{view_url}"
            send_line_message(message)

            # 記錄圖片上傳信息
            app.logger.debug(f"Received file: {filename}")
            app.logger.debug(f"File saved at: {file_path}")
            
            return render_template('upload_success.html', view_url=view_url)
        else:
            app.logger.debug("No file received")
    return render_template('upload.html')

@app.route('/view')
def view_image():
    image_id = request.args.get('id')
    if not image_id:
        return "No image ID provided.", 400
    filename = image_id + '.jpg'
    return render_template('view.html', filename=filename)

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # 確保 Flask 接受外部請求
    app.run(host='0.0.0.0', port=5000, debug=True)
