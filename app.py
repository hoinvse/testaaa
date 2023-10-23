from flask import Flask, request, render_template, send_file
import telebot
from PIL import Image

app = Flask(__name__)

# Khai báo thông tin bot Telegram
bot = telebot.TeleBot('6726069921:AAEckrK1X3xkC20Rq8ZRoxIqhVMgQFhFa1o')
chat_id = '5554945230'  # ID của cuộc trò chuyện Telegram cần gửi thông tin

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    phone = request.form['phone']
    image = request.files['image']

    # Gửi thông tin và ảnh đến chatbot Telegram
    message = f'Tên: {name}, Số điện thoại: {phone}'
    bot.send_message(chat_id, message)

    if image:
        # Lưu tệp ảnh tạm thời trên máy chủ
        image_path = 'temp_image.jpg'
        image.save(image_path)

        # Gửi ảnh đến chatbot Telegram
        with open(image_path, 'rb') as image_file:
            bot.send_photo(chat_id, image_file)

        # Xóa tệp ảnh tạm thời
        os.remove(image_path)

    return "Thông tin và ảnh đã được gửi thành công!"

if __name__ == '__main__':
    app.run(debug=True)
